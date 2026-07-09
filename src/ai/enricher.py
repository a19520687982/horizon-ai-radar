"""Content enrichment using AI (second-pass analysis).

For items that pass the score threshold, this module:
1. Searches the web for relevant context (via DuckDuckGo)
2. Feeds search results + item content to AI to generate grounded background knowledge
"""

import asyncio
import json
import re
import sys
import os
from typing import List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn
from ddgs import DDGS

from .client import AIClient
from .prompts import (
    CONCEPT_EXTRACTION_SYSTEM, CONCEPT_EXTRACTION_USER,
    CONTENT_ENRICHMENT_SYSTEM, CONTENT_ENRICHMENT_USER,
)
from .utils import parse_json_response
from ..models import ContentItem


class ContentEnricher:
    """Enriches high-scoring content items with background knowledge."""

    def __init__(self, ai_client: AIClient):
        self.client = ai_client

    def _get_concurrency(self) -> int:
        """Return the configured enrichment concurrency, clamped to 1 or above."""
        config = getattr(self.client, "config", None)
        concurrency = getattr(config, "enrichment_concurrency", 1)
        return max(concurrency, 1)

    async def enrich_batch(self, items: List[ContentItem]) -> None:
        """Enrich items in-place with background knowledge.

        Args:
            items: Content items to enrich (modified in-place)
        """
        concurrency = self._get_concurrency()
        semaphore = asyncio.Semaphore(concurrency)

        async def _process(item: ContentItem, progress_task) -> None:
            async with semaphore:
                try:
                    await self._enrich_item(item)
                except Exception as e:
                    print(f"Error enriching item {item.id}: {e}, falling back to translation")
                    await self._translate_item(item)
            progress.advance(progress_task)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Enriching", total=len(items))
            coros = [
                _process(item, task) for item in items
            ]
            await asyncio.gather(*coros)

    async def _web_search(self, query: str, max_results: int = 3) -> list:
        """Search the web for context via DuckDuckGo.

        Returns:
            List of dicts with keys: title, url, body
        """
        try:
            # Suppress primp "Impersonate ... does not exist" stderr warning
            stderr = sys.stderr
            sys.stderr = open(os.devnull, "w")
            try:
                ddgs = DDGS()
                results = await asyncio.to_thread(ddgs.text, query, max_results=max_results)
            finally:
                sys.stderr.close()
                sys.stderr = stderr
        except Exception:
            return []

        return [
            {"title": r.get("title", ""), "url": r.get("href", ""), "body": r.get("body", "")}
            for r in (results or [])
        ]

    @staticmethod
    def _parse_json_response(response: str) -> Optional[dict]:
        """Try multiple strategies to extract a JSON object from an AI response.

        Returns the parsed dict, or None if all strategies fail.
        """
        return parse_json_response(response)

    @staticmethod
    def _as_text(value) -> str:
        """Normalize AI-returned scalar/dict/list values into displayable text."""
        if value is None:
            return ""
        if isinstance(value, dict):
            value = value.get("text") or value.get("content") or value.get("value") or ""
        if isinstance(value, list):
            return "；".join(str(v).strip() for v in value if str(v).strip())
        return str(value).strip()

    @classmethod
    def _as_list(cls, value) -> List[str]:
        """Normalize AI-returned arrays into a list of non-empty strings."""
        if value is None:
            return []
        if isinstance(value, list):
            return [cls._as_text(v) for v in value if cls._as_text(v)]
        text = cls._as_text(value)
        return [text] if text else []

    @staticmethod
    def _is_ad_url(url: str) -> bool:
        """Return True for known ad redirect URLs that should not be cited."""
        lowered = str(url or "").lower()
        return any(
            marker in lowered
            for marker in (
                "bing.com/aclick",
                "googleadservices.com",
                "doubleclick.net",
            )
        )

    async def _extract_concepts(self, item: ContentItem, content_text: str) -> List[str]:
        """Ask AI to identify concepts that need explanation.

        Args:
            item: Content item
            content_text: Extracted content text

        Returns:
            List of search queries for concepts that need explanation
        """
        user_prompt = CONCEPT_EXTRACTION_USER.format(
            title=item.title,
            summary=item.ai_summary or item.title,
            tags=", ".join(item.ai_tags) if item.ai_tags else "",
            content=content_text[:1000],
        )

        try:
            response = await self.client.complete(
                system=CONCEPT_EXTRACTION_SYSTEM,
                user=user_prompt,
            )
            result = self._parse_json_response(response)
            if result is None:
                return []
            queries = result.get("queries", [])
            return queries[:3]
        except Exception:
            return []

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=2, max=10)
    )
    async def _enrich_item(self, item: ContentItem) -> None:
        """Enrich a single item with background knowledge.

        Steps:
        1. Ask AI which concepts in the news need explanation
        2. Search the web for those concepts
        3. Ask AI to generate background based on search results

        Args:
            item: Content item to enrich (modified in-place via metadata)
        """
        # Extract content text and comments separately
        content_text = ""
        comments_text = ""
        if item.content:
            if "--- Top Comments ---" in item.content:
                main, comments_part = item.content.split("--- Top Comments ---", 1)
                content_text = main.strip()[:4000]
                comments_text = comments_part.strip()[:2000]
            else:
                content_text = item.content[:4000]

        # Step 1: AI identifies concepts to explain
        queries = await self._extract_concepts(item, content_text)

        # Step 2: Search web for each concept
        all_results = []
        web_sections = []
        for query in queries:
            results = await self._web_search(query)
            all_results.extend(results)
            if results:
                lines = [f"- [{r['title']}]({r['url']}): {r['body']}" for r in results]
                web_sections.append(f"**{query}:**\n" + "\n".join(lines))
        web_context = "\n\n".join(web_sections) if web_sections else ""

        # Index of available URLs for citation validation
        available_urls = {r["url"]: r["title"] for r in all_results if r.get("url")}

        # Step 3: AI generates background grounded in search results
        user_prompt = CONTENT_ENRICHMENT_USER.format(
            title=item.title,
            url=str(item.url),
            summary=item.ai_summary or item.title,
            score=item.ai_score or 0,
            reason=item.ai_reason or "",
            tags=", ".join(item.ai_tags) if item.ai_tags else "",
            content=content_text,
            comments_section=f"\n**Community Comments:**\n{comments_text}" if comments_text else "",
            web_context=web_context or "No web search results available.",
        )

        response = await self.client.complete(
            system=CONTENT_ENRICHMENT_SYSTEM,
            user=user_prompt,
        )

        # Parse JSON response with robust fallback
        result = self._parse_json_response(response)
        if result is None:
            # Gracefully degrade: fall back to a lightweight translation
            # instead of dropping the item untranslated.
            print(f"Warning: could not parse enrichment response for {item.id}, falling back to translation")
            await self._translate_item(item)
            return

        # New opportunity-radar fields. Keep them additive so older renderers
        # and webhook paths can still fall back to the previous summary fields.
        opportunity_fields = {
            "title_zh": result.get("title_zh"),
            "opportunity_content_type": result.get("content_type_zh"),
            "opportunity_one_sentence_takeaway": result.get("one_sentence_zh")
            or result.get("one_sentence_takeaway"),
            "opportunity_special_point": result.get("special_point_zh")
            or result.get("why_it_matters"),
            "opportunity_user_value": result.get("user_value_zh")
            or result.get("relevance_to_ordinary_people"),
            "opportunity_self_media": result.get("self_media_opportunity_zh"),
            "opportunity_ecommerce_money": result.get("ecommerce_money_opportunity_zh"),
            "opportunity_learning_advice": result.get("learning_advice_zh"),
            "opportunity_action": result.get("action_zh"),
            "opportunity_risk_warning": result.get("risk_warning_zh")
            or result.get("risks"),
            "opportunity_plain_explanation": result.get("plain_explanation"),
            "opportunity_why_it_matters": result.get("why_it_matters"),
            "opportunity_relevance": result.get("relevance_to_ordinary_people"),
            "opportunity_ai_judgement": result.get("ai_judgement"),
        }
        for key, value in opportunity_fields.items():
            text = self._as_text(value)
            if text:
                item.metadata[key] = text

        opportunities = self._as_list(result.get("opportunities"))
        if opportunities:
            item.metadata["opportunity_opportunities"] = opportunities

        content_ideas = self._as_list(result.get("content_ideas"))
        if content_ideas:
            item.metadata["opportunity_content_ideas"] = content_ideas

        # Combine old structured sub-fields into per-language detailed_summary
        for lang in ("en", "zh"):
            title_text = self._as_text(result.get(f"title_{lang}"))
            if title_text:
                item.metadata[f"title_{lang}"] = title_text

            parts = []
            for field in ("whats_new", "why_it_matters", "key_details"):
                text = self._as_text(result.get(f"{field}_{lang}"))
                if text:
                    parts.append(text)
            if parts:
                item.metadata[f"detailed_summary_{lang}"] = " ".join(parts)

            background_text = self._as_text(result.get(f"background_{lang}"))
            if background_text:
                item.metadata[f"background_{lang}"] = background_text

            discussion_text = self._as_text(result.get(f"community_discussion_{lang}"))
            if discussion_text:
                item.metadata[f"community_discussion_{lang}"] = discussion_text

        if not item.metadata.get("detailed_summary_zh"):
            fallback_parts = [
                item.metadata.get("opportunity_one_sentence_takeaway", ""),
                item.metadata.get("opportunity_special_point", ""),
                item.metadata.get("opportunity_user_value", ""),
            ]
            fallback_summary = " ".join(part for part in fallback_parts if part)
            if fallback_summary:
                item.metadata["detailed_summary_zh"] = fallback_summary

        if not item.metadata.get("background_zh") and item.metadata.get("opportunity_user_value"):
            item.metadata["background_zh"] = item.metadata["opportunity_user_value"]

        # Store citation sources — only URLs that actually came from our search results
        if result.get("sources") and available_urls:
            valid = [
                {"url": u, "title": available_urls[u]}
                for u in result["sources"]
                if u in available_urls and not self._is_ad_url(u)
            ]
            if valid:
                item.metadata["sources"] = valid

        # Backward-compatible fallback fields (English as default)
        item.metadata["detailed_summary"] = item.metadata.get("detailed_summary_en", "")
        item.metadata["background"] = item.metadata.get("background_en", "")
        item.metadata["community_discussion"] = item.metadata.get("community_discussion_en", "")

    async def _translate_item(self, item: ContentItem) -> None:
        """Lightweight translation fallback: when full enrichment fails, at least
        translate the title and summary to Chinese so the item is not dropped."""
        try:
            response = await self.client.complete(
                system="You are a translator. Translate to Simplified Chinese. Return only valid JSON, no other text.",
                user=(
                    f'Title: {item.title}\n'
                    f'Summary: {item.ai_summary or item.title}\n\n'
                    'Return JSON:\n'
                    '{"title_zh": "<中文标题>", "summary_zh": "<用中文写1-2句摘要>"}'
                ),
            )
            result = self._parse_json_response(response)
            if result:
                if result.get("title_zh"):
                    item.metadata["title_zh"] = result["title_zh"]
                if result.get("summary_zh"):
                    item.metadata["detailed_summary_zh"] = result["summary_zh"]
        except Exception:
            pass

        summary = (
            item.metadata.get("detailed_summary_zh")
            or item.ai_summary
            or item.title
            or "这条内容目前只有基础信息，详细机会分析生成失败。"
        )
        item.metadata.setdefault("opportunity_content_type", self._fallback_content_type(item))
        item.metadata.setdefault("opportunity_one_sentence_takeaway", summary)
        item.metadata.setdefault(
            "opportunity_special_point",
            "这条内容的详细分析没有成功生成，建议先看标题和原文判断是否值得继续了解。",
        )
        item.metadata.setdefault(
            "opportunity_user_value",
            "对普通人的直接价值暂时不明确，可以先作为素材收藏，等有更多可靠信息再判断。",
        )
        item.metadata.setdefault("opportunity_self_media", "暂无明显机会")
        item.metadata.setdefault("opportunity_ecommerce_money", "暂无明显机会")
        item.metadata.setdefault("opportunity_learning_advice", "可以了解。先收藏，不需要马上投入时间深入学习。")
        item.metadata.setdefault("opportunity_action", "收藏。后续有更多案例或官方说明时再决定是否深挖。")
        item.metadata.setdefault("opportunity_risk_warning", self._fallback_risk_warning(item))

    @staticmethod
    def _fallback_content_type(item: ContentItem) -> str:
        """Infer a beginner-facing content type when enrichment fails."""
        haystack = " ".join(
            [
                item.title or "",
                item.ai_summary or "",
                " ".join(item.ai_tags or []),
                item.source_type.value or "",
                str(item.url or ""),
            ]
        ).lower()
        if "github" in haystack or "repo" in haystack or "open source" in haystack:
            return "GitHub 新项目"
        if "learn" in haystack or "tutorial" in haystack or "course" in haystack or "学习" in haystack:
            return "AI 学习机会"
        if "ai" in haystack or "llm" in haystack or "gpt" in haystack or "claude" in haystack:
            return "新 AI 工具"
        return "AI 行业趋势"

    @staticmethod
    def _fallback_risk_warning(item: ContentItem) -> str:
        """Provide a safe default warning for tools that might execute code or handle data."""
        haystack = " ".join(
            [
                item.title or "",
                item.ai_summary or "",
                " ".join(item.ai_tags or []),
                item.source_type.value or "",
                str(item.url or ""),
            ]
        ).lower()
        markers = (
            "github",
            "repo",
            "open source",
            "开源",
            "local ai",
            "本地 ai",
            "automation",
            "自动化",
            "agent",
            "plugin",
            "插件",
            "cli",
            "命令",
        )
        if any(marker in haystack for marker in markers):
            return "新手不要随便运行陌生命令，不要安装不可信插件，也不要输入 API Key、账号密码、客户资料等敏感信息。"
        return "暂无明显风险"
