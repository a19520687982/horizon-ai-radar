"""Daily summary generation — pure programmatic rendering."""

import re
from typing import List

from ..models import ContentItem


_CJK = r"[\u4e00-\u9fff\u3400-\u4dbf]"
_ASCII = r"[A-Za-z0-9]"


def _pangu(text: str) -> str:
    """Insert a space between CJK and ASCII letters/digits (Pangu spacing)."""
    text = re.sub(rf"({_CJK})({_ASCII})", r"\1 \2", text)
    text = re.sub(rf"({_ASCII})({_CJK})", r"\1 \2", text)
    return text


LABELS = {
    "en": {
        "header": "Horizon Daily",
        "source": "Source",
        "background": "Background",
        "discussion": "Discussion",
        "references": "References",
        "tags": "Tags",
        "content_type": "Type",
        "one_sentence": "One-Sentence Summary",
        "special_point": "What Makes It Special",
        "user_value": "What It Means For You",
        "self_media": "Self-Media Opportunity",
        "ecommerce_money": "Ecommerce / Money Opportunity",
        "learning_advice": "Should You Learn It",
        "action": "Suggested Action",
        "risk_warning": "Risk Warning",
        "source_links": "Source and References",
        "selected_items": "From {total} items, {selected} important content pieces were selected",
        "empty_analyzed": "Analyzed {total} items, but none met the importance threshold.",
        "empty_body": (
            "No significant developments today. This might indicate:\n"
            "- A quiet day in your tracked sources\n"
            "- The AI score threshold is too high\n"
            "- Your information sources need expansion\n\n"
            "Consider:\n"
            "1. Lowering the `ai_score_threshold` in config.json\n"
            "2. Adding more diverse information sources\n"
            "3. Checking if the AI model is working correctly\n"
        ),
    },
    "zh": {
        "header": "Horizon 每日速递",
        "source": "来源",
        "background": "背景",
        "discussion": "社区讨论",
        "references": "参考链接",
        "tags": "标签",
        "content_type": "类型",
        "one_sentence": "一句话总结",
        "special_point": "它特别在哪里",
        "user_value": "对我有什么用",
        "self_media": "自媒体机会",
        "ecommerce_money": "电商/赚钱机会",
        "learning_advice": "我该不该学",
        "action": "建议动作",
        "risk_warning": "风险提醒",
        "source_links": "来源和参考链接",
        "selected_items": "从 {total} 条内容中筛选出 {selected} 条重要资讯。",
        "empty_analyzed": "已分析 {total} 条内容，但没有达到重要性阈值的条目。",
        "empty_body": (
            "今日暂无重要动态，可能原因：\n"
            "- 今天关注的信息源较平静\n"
            "- AI 评分阈值设置过高\n"
            "- 信息源种类有待扩充\n\n"
            "建议：\n"
            "1. 在 config.json 中降低 `ai_score_threshold`\n"
            "2. 添加更多多样化的信息源\n"
            "3. 检查 AI 模型是否正常工作\n"
        ),
    },
}


class DailySummarizer:
    """Generates daily Markdown summaries from pre-analyzed content items."""

    def __init__(self):
        pass

    async def generate_summary(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate daily summary in Markdown format.

        Items are rendered in score-descending order (already sorted by orchestrator).

        Args:
            items: High-scoring content items (already enriched)
            date: Date string (YYYY-MM-DD)
            total_fetched: Total number of items fetched before filtering
            language: Output language, either "en" or "zh"

        Returns:
            str: Markdown formatted summary
        """
        labels = LABELS.get(language, LABELS["en"])

        if not items:
            return self._generate_empty_summary(date, total_fetched, labels)

        main_items = [item for item in items if not self._is_noise_item(item)]
        noise_items = [item for item in items if self._is_noise_item(item)]
        display_items = main_items + noise_items

        header = (
            f"# {labels['header']} - {date}\n\n"
            f"> {labels['selected_items'].format(total=total_fetched, selected=len(items))}\n\n"
            "> 排序按“机会优先”展示，不完全按分数。能马上试用、能做内容/自动化/电商提效的内容会排在更前面。\n\n"
            "---\n\n"
        )

        # TOC
        toc_entries = []
        for i, item in enumerate(display_items):
            _t = item.metadata.get(f"title_{language}") or item.title
            t = str(_t).replace("[", "(").replace("]", ")")
            t = self._tone_down_title(t)
            if language == "zh":
                t = _pangu(t)
            score = item.ai_score or "?"
            toc_entries.append(f"{i + 1}. [{t}](#item-{i + 1}) \u2b50\ufe0f {score}/10")
        toc = "\n".join(toc_entries) + "\n\n---\n\n"

        parts = self._format_grouped_items(main_items, noise_items, labels, language)

        return header + toc + "".join(parts)

    def generate_webhook_overview(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate a compact overview for multi-message webhook delivery."""
        labels = LABELS.get(language, LABELS["en"])
        if not items:
            return self._generate_empty_summary(date, total_fetched, labels)

        if language == "zh":
            header = (
                f"# {labels['header']} - {date}\n\n"
                f"> 从 {total_fetched} 条内容中筛选出 {len(items)} 条重要资讯。\n\n"
                "下面会按新闻逐条发送详情，你可以只看感兴趣的标题。\n\n"
            )
        else:
            header = (
                f"# {labels['header']} - {date}\n\n"
                f"> Selected {len(items)} important items from {total_fetched} fetched items.\n\n"
                "Details will be sent item by item so you can read only the topics you care about.\n\n"
            )

        entries = []
        for i, item in enumerate(items, start=1):
            title = str(item.metadata.get(f"title_{language}") or item.title).replace("[", "(").replace("]", ")")
            title = self._tone_down_title(title)
            if language == "zh":
                title = _pangu(title)
            score = item.ai_score or "?"
            entries.append(f"{i}. [{title}]({item.url}) \u2b50\ufe0f {score}/10")

        return header + "\n".join(entries)

    def generate_webhook_item(
        self,
        item: ContentItem,
        language: str,
        index: int,
        total: int,
    ) -> str:
        """Generate one item message for multi-message webhook delivery."""
        labels = LABELS.get(language, LABELS["en"])
        prefix = f"第 {index}/{total} 条\n\n" if language == "zh" else f"Item {index}/{total}\n\n"
        return prefix + self._format_item(item, labels, language, index, heading_level=2).rstrip("-\n ")

    def _format_grouped_items(
        self,
        main_items: List[ContentItem],
        noise_items: List[ContentItem],
        labels: dict,
        language: str,
    ) -> str:
        """Render main items under topic headings, then low-value noise separately."""
        sections: List[str] = []
        index = 1
        for topic, topic_items in self._group_by_topic(main_items):
            sections.append(f"## 专题：{topic}\n\n")
            for item in topic_items:
                sections.append(self._format_item(item, labels, language, index, heading_level=3))
                index += 1

        if noise_items:
            sections.append("## 可忽略噪音（简略）\n\n")
            sections.append("这些内容不放进重点正文，只保留标题方便回看。\n\n")
            for item in noise_items:
                sections.append(self._format_noise_item(item, labels, language, index))
                index += 1

        return "".join(sections)

    def _group_by_topic(self, items: List[ContentItem]) -> List[tuple[str, List[ContentItem]]]:
        """Group related items into stable beginner-facing topics."""
        groups: dict[str, List[ContentItem]] = {}
        order: List[str] = []
        for item in items:
            topic = self._topic_label(item)
            if topic not in groups:
                groups[topic] = []
                order.append(topic)
            groups[topic].append(item)
        return [(topic, groups[topic]) for topic in order]

    def _format_item(
        self,
        item: ContentItem,
        labels: dict,
        language: str,
        index: int,
        heading_level: int = 2,
    ) -> str:
        """Format a single ContentItem into Markdown."""
        _title = item.metadata.get(f"title_{language}") or item.title
        title = str(_title).replace("[", "(").replace("]", ")")
        title = self._tone_down_title(title)
        score = item.ai_score or "?"
        meta = item.metadata

        fallback_summary = (
            meta.get(f"detailed_summary_{language}")
            or meta.get("detailed_summary")
            or item.ai_summary
            or ""
        )
        fallback_background = meta.get(f"background_{language}") or meta.get("background") or ""

        content_type = (
            meta.get("opportunity_content_type")
            or meta.get("content_type_zh")
            or self._fallback_content_type(item)
        )
        one_sentence = (
            meta.get("opportunity_one_sentence_takeaway")
            or meta.get("one_sentence_zh")
            or item.ai_summary
            or fallback_summary
        )
        special_point = (
            meta.get("opportunity_special_point")
            or meta.get("special_point_zh")
            or meta.get("opportunity_why_it_matters")
            or fallback_background
            or item.ai_reason
            or fallback_summary
        )
        user_value = (
            meta.get("opportunity_user_value")
            or meta.get("user_value_zh")
            or meta.get("opportunity_relevance")
            or fallback_background
            or "这条内容和普通人的直接关系还不明确，可以先当作趋势观察。"
        )
        content_ideas = self._listify(meta.get("opportunity_content_ideas"))
        self_media = (
            meta.get("opportunity_self_media")
            or meta.get("self_media_opportunity_zh")
            or self._format_list_or_default(content_ideas, "暂无明显机会")
        )
        ecommerce_money = (
            meta.get("opportunity_ecommerce_money")
            or meta.get("ecommerce_money_opportunity_zh")
            or "暂无明显机会"
        )
        learning_advice = (
            meta.get("opportunity_learning_advice")
            or meta.get("learning_advice_zh")
            or self._fallback_learning_advice(item.ai_score)
        )
        action = (
            meta.get("opportunity_action")
            or meta.get("action_zh")
            or self._fallback_action(item.ai_score)
        )
        risk_warning = (
            meta.get("opportunity_risk_warning")
            or meta.get("risk_warning_zh")
            or self._fallback_risk_warning(item, str(content_type))
        )
        risk_warning = self._complete_risk_warning(item, str(content_type), str(risk_warning))

        if language == "zh":
            title = _pangu(title)
            content_type = _pangu(self._tone_down_text(str(content_type)))
            one_sentence = _pangu(self._tone_down_text(str(one_sentence)))
            special_point = _pangu(self._tone_down_text(str(special_point)))
            user_value = _pangu(self._tone_down_text(str(user_value)))
            self_media = _pangu(self._tone_down_text(str(self_media)))
            ecommerce_money = _pangu(self._tone_down_text(str(ecommerce_money)))
            learning_advice = _pangu(self._tone_down_text(str(learning_advice)))
            action = _pangu(self._tone_down_text(str(action)))
            risk_warning = _pangu(self._tone_down_text(str(risk_warning)))

        source_info = self._source_info(item, language)
        reference_lines = self._reference_lines(item, labels)
        verification_lines = self._verification_lines(item)
        heading = "#" * heading_level

        lines = [
            f'<a id="item-{index}"></a>',
            f"{heading} {title} \u2b50\ufe0f {score}/10",  # ⭐️
            "",
            f"**{labels['content_type']}：**",
            str(content_type),
            "",
            f"**{labels['one_sentence']}：**",
            str(one_sentence),
            "",
            f"**{labels['special_point']}：**",
            str(special_point),
            "",
            f"**{labels['user_value']}：**",
            str(user_value),
            "",
            f"**{labels['self_media']}：**",
            str(self_media),
            "",
            f"**{labels['ecommerce_money']}：**",
            str(ecommerce_money),
            "",
            f"**{labels['learning_advice']}：**",
            str(learning_advice),
            "",
            f"**{labels['action']}：**",
            str(action),
            "",
            f"**{labels['source_links']}：**",
            source_info,
            "\n".join(reference_lines),
            "",
        ]

        if self._should_show_risk_warning(str(risk_warning)):
            insert_at = lines.index(f"**{labels['source_links']}：**")
            lines[insert_at:insert_at] = [
                f"**{labels['risk_warning']}：**",
                str(risk_warning),
                "",
            ]

        if verification_lines:
            lines.extend(verification_lines)
            lines.append("")

        lines.append("")
        lines.append("---")

        return "\n".join(lines) + "\n\n"

    def _format_noise_item(self, item: ContentItem, labels: dict, language: str, index: int) -> str:
        """Render low-value noise as a compact entry instead of a full item."""
        _title = item.metadata.get(f"title_{language}") or item.title
        title = self._tone_down_title(str(_title).replace("[", "(").replace("]", ")"))
        if language == "zh":
            title = _pangu(title)
        summary = (
            item.metadata.get("opportunity_one_sentence_takeaway")
            or item.metadata.get("one_sentence_zh")
            or item.ai_summary
            or "暂无更多摘要"
        )
        if language == "zh":
            summary = _pangu(self._tone_down_text(str(summary)))
        score = item.ai_score or "?"
        source_info = self._source_info(item, language)
        verification = (
            "\n".join(self._verification_lines(item)) + "\n\n"
            if self._verification_lines(item)
            else ""
        )
        return (
            f'<a id="item-{index}"></a>\n'
            f"### {title} \u2b50\ufe0f {score}/10\n\n"
            f"{summary}\n\n"
            f"{source_info}\n\n"
            f"{verification}"
            "---\n\n"
        )

    @staticmethod
    def _listify(value) -> List[str]:
        """Return a clean list from metadata values that may be list or text."""
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        text = str(value).strip()
        return [text] if text else []

    @staticmethod
    def _format_list_or_default(values: List[str], default: str) -> str:
        """Render a short list as Markdown bullets, or return a default sentence."""
        cleaned = [str(value).strip() for value in values if str(value).strip()]
        if not cleaned:
            return default
        return "\n".join(f"- {value}" for value in cleaned[:2])

    @staticmethod
    def _is_ad_url(url: str) -> bool:
        """Return True for known ad redirect URLs that should not be shown."""
        lowered = str(url or "").lower()
        return any(
            marker in lowered
            for marker in (
                "bing.com/aclick",
                "googleadservices.com",
                "doubleclick.net",
            )
        )

    def _source_info(self, item: ContentItem, language: str) -> str:
        """Build a compact source/date line without making it the main content."""
        meta = item.metadata
        source_parts = [item.source_type.value]
        if meta.get("subreddit"):
            source_parts.append(f"r/{meta['subreddit']}")
        if meta.get("feed_name"):
            source_parts.append(str(meta["feed_name"]))
        else:
            source_parts.append(item.author or "unknown")
        if item.published_at:
            if language == "zh":
                source_parts.append(
                    f"{item.published_at.month}月{item.published_at.day}日 "
                    f"{item.published_at:%H:%M}"
                )
            else:
                day = item.published_at.strftime("%d").lstrip("0")
                source_parts.append(item.published_at.strftime(f"%b {day}, %H:%M"))
        return " \u00b7 ".join(source_parts)

    def _reference_lines(self, item: ContentItem, labels: dict) -> List[str]:
        """Build de-duplicated, non-ad reference links for the bottom of an item."""
        links = []

        def add_link(label: str, url: str) -> None:
            url = str(url or "").strip()
            if not url or self._is_ad_url(url):
                return
            if any(existing_url == url for _, existing_url in links):
                return
            links.append((label, url))

        add_link("原文", str(item.url))
        discussion_url = item.metadata.get("discussion_url")
        if discussion_url and str(discussion_url) != str(item.url):
            add_link(labels["discussion"], str(discussion_url))

        for source in item.metadata.get("sources") or []:
            if isinstance(source, dict):
                add_link(str(source.get("title") or "参考链接"), str(source.get("url") or ""))
            else:
                add_link("参考链接", str(source))

        if not links:
            return ["暂无可展示链接"]
        return [f"- [{label}]({url})" for label, url in links]

    def _item_text(self, item: ContentItem) -> str:
        """Build a small text blob for rendering-time classification."""
        meta = item.metadata or {}
        return " ".join(
            [
                item.title or "",
                item.ai_summary or "",
                item.ai_reason or "",
                " ".join(item.ai_tags or []),
                str(meta.get("opportunity_content_type") or ""),
                str(meta.get("content_type_zh") or ""),
                str(meta.get("opportunity_one_sentence_takeaway") or ""),
                str(meta.get("opportunity_user_value") or ""),
                str(meta.get("subreddit") or ""),
                item.source_type.value or "",
                str(item.url or ""),
            ]
        ).lower()

    def _topic_label(self, item: ContentItem) -> str:
        """Return a concise topic label for grouping similar items."""
        text = self._item_text(item)
        if self._has_any(text, ("cursor", "claude code", "codex", "copilot", "zcode", "coding", "代码", "编程")):
            return "AI 编程工具"
        if self._has_any(text, ("local ai", "local llm", "ollama", "lm studio", "本地 ai", "本地模型", "本地大模型")):
            return "本地 AI"
        if self._has_any(text, ("agent", "automation", "workflow", "智能体", "自动化", "工作流")):
            return "AI 自动化和智能体"
        if self._has_any(text, ("image", "video", "voice", "audio", "speech", "图像", "视频", "语音", "音频")):
            return "AI 图像/视频/语音"
        if self._has_any(text, ("github", "repo", "repository", "open source", "开源", "ossinsight")):
            return "GitHub 可用项目"
        if self._has_any(text, ("learn", "tutorial", "course", "guide", "学习", "教程", "课程", "指南")):
            return "AI 学习机会"
        if self._has_any(text, ("creator", "content", "ecommerce", "shopify", "小红书", "自媒体", "电商", "营销", "文案")):
            return "自媒体/电商机会"
        return "AI 趋势观察"

    def _is_noise_item(self, item: ContentItem) -> bool:
        """Return True when an item should be moved out of the main digest body."""
        text = self._item_text(item)
        content_type = str(
            item.metadata.get("opportunity_content_type")
            or item.metadata.get("content_type_zh")
            or ""
        )
        if "可忽略噪音" in content_type:
            return True
        if (item.ai_score or 0) < 4:
            return True
        ai_markers = (
            "ai",
            "llm",
            "gpt",
            "claude",
            "gemini",
            "openai",
            "大模型",
            "人工智能",
            "智能体",
            "copilot",
            "cursor",
            "codex",
            "ollama",
        )
        non_ai_noise_markers = (
            "payment gateway",
            "x402",
            "stablecoin",
            "usdc",
            "coinbase",
            "按次收费",
            "付费网关",
            "稳定币",
            "微支付",
            "cooperative product",
            "合作社产品",
            "产品目录",
            "robot vacuum",
            "机器人吸尘器",
            "游戏光盘",
            "实体游戏",
            "数字游戏",
        )
        if self._has_any(text, non_ai_noise_markers) and not self._has_any(text, ai_markers):
            return True
        if self._has_any(text, ("x402", "stablecoin", "usdc", "coinbase", "稳定币")):
            return True
        noise_markers = (
            "crypto",
            "blockchain",
            "trading",
            "kubernetes",
            "security patch",
            "cve",
            "加密货币",
            "币圈",
            "交易",
            "安全补丁",
        )
        opportunity_markers = (
            "ai",
            "llm",
            "gpt",
            "claude",
            "github",
            "automation",
            "agent",
            "ollama",
            "cursor",
            "copilot",
            "人工智能",
            "大模型",
            "自动化",
            "智能体",
            "自媒体",
            "电商",
        )
        return self._has_any(text, noise_markers) and not self._has_any(text, opportunity_markers)

    def _verification_lines(self, item: ContentItem) -> List[str]:
        """Add explicit verification warning for Reddit/community rumor items."""
        text = self._item_text(item)
        is_reddit = item.source_type.value == "reddit" or "reddit.com" in str(item.url).lower() or bool(
            item.metadata.get("subreddit")
        )
        is_rumor = self._has_any(text, ("rumor", "leak", "爆料", "传闻", "被曝", "争议", "指控"))
        if is_reddit or is_rumor:
            return ["**核实状态：**", "社区来源/爆料内容，未核实，需要二次核实。"]
        return []

    @staticmethod
    def _has_any(text: str, keywords: tuple[str, ...]) -> bool:
        """Return True if any keyword appears in text."""
        return any(keyword in text for keyword in keywords)

    @staticmethod
    def _should_show_risk_warning(risk_warning: str) -> bool:
        """Only show risk warnings when there is a concrete warning."""
        text = str(risk_warning or "").strip()
        if not text:
            return False
        return text not in {"暂无明显风险", "暂无明显风险。"}

    @staticmethod
    def _tone_down_title(title: str) -> str:
        """Reduce clickbait phrasing in AI-generated or source-provided titles."""
        return DailySummarizer._tone_down_text(title)

    @staticmethod
    def _tone_down_text(text: str) -> str:
        """Reduce clickbait phrasing in generated display text."""
        replacements = {
            "只用“动嘴”": "用自然语言协助开发",
            "只用动嘴": "用自然语言协助开发",
            "应该害怕": "需要关注的影响",
            "一夜暴富": "商业机会",
            "神器": "工具",
            "太香了": "值得关注",
            "程序员效率工具": "编程效率工具",
            "彻底关闭：找到替代方案了吗？": "关闭：需要准备替代方案",
        }
        cleaned = str(text)
        for noisy, calmer in replacements.items():
            cleaned = cleaned.replace(noisy, calmer)
        return cleaned.strip()

    @staticmethod
    def _is_risky_tool_item(item: ContentItem, content_type: str) -> bool:
        """Return True for items where beginners need operational safety advice."""
        haystack = " ".join(
            [
                content_type or "",
                item.title or "",
                item.ai_summary or "",
                " ".join(item.ai_tags or []),
                item.source_type.value or "",
            ]
        ).lower()
        risky_markers = (
            "github",
            "open source",
            "开源",
            "本地 ai",
            "local ai",
            "automation",
            "自动化",
            "agent",
            "插件",
            "plugin",
            "cli",
            "命令",
            "repo",
        )
        return any(marker in haystack for marker in risky_markers)

    def _complete_risk_warning(self, item: ContentItem, content_type: str, risk_warning: str) -> str:
        """Ensure risky tool items include concrete beginner safety advice."""
        text = str(risk_warning or "").strip() or "暂无明显风险"
        if not self._is_risky_tool_item(item, content_type):
            return text
        required = "新手不要随便运行陌生命令，不要安装不可信插件，也不要输入 API Key、账号密码、客户资料等敏感信息。"
        if "陌生命令" in text and "不可信插件" in text and "敏感信息" in text:
            return text
        if text == "暂无明显风险":
            return required
        return f"{text} {required}"

    @staticmethod
    def _fallback_content_type(item: ContentItem) -> str:
        """Infer one of the Chinese digest content types when enrichment is missing."""
        haystack = " ".join(
            [
                item.title or "",
                item.ai_summary or "",
                " ".join(item.ai_tags or []),
                item.source_type.value or "",
            ]
        ).lower()
        try:
            score_value = float(item.ai_score or 0)
        except (TypeError, ValueError):
            score_value = 0
        if score_value < 3:
            return "可忽略噪音"
        if "github" in haystack or "repo" in haystack or "open source" in haystack:
            return "GitHub 新项目"
        if "course" in haystack or "learn" in haystack or "tutorial" in haystack or "学习" in haystack:
            return "AI 学习机会"
        if "ai" in haystack or "gpt" in haystack or "claude" in haystack or "agent" in haystack:
            return "新 AI 工具"
        return "AI 行业趋势"

    @staticmethod
    def _fallback_learning_advice(score) -> str:
        """Map score to beginner-friendly learning advice."""
        try:
            score_value = float(score or 0)
        except (TypeError, ValueError):
            score_value = 0
        if score_value >= 8:
            return "值得学。先学它能解决什么问题，再找一个低成本场景试用，不需要先学复杂代码。"
        if score_value >= 6:
            return "可以了解。先收藏，等它和你的内容、电商或自动化需求有关时再深入。"
        return "暂时不用学。普通人现在投入时间的回报不明显。"

    @staticmethod
    def _fallback_action(score) -> str:
        """Map score to a practical next action."""
        try:
            score_value = float(score or 0)
        except (TypeError, ValueError):
            score_value = 0
        if score_value >= 9:
            return "深挖。今天可以花十分钟看原文，判断能不能做成内容或小服务。"
        if score_value >= 7:
            return "试用。先看有没有现成 Demo、教程或案例，别急着投入钱。"
        if score_value >= 5:
            return "收藏。先放进素材库，后续有更多案例再判断。"
        return "忽略。暂时不值得占用你的学习时间。"

    @staticmethod
    def _fallback_risk_warning(item: ContentItem, content_type: str) -> str:
        """Return a beginner-safe warning for tools that may execute code or handle data."""
        if DailySummarizer._is_risky_tool_item(item, content_type):
            return "新手不要随便运行陌生命令，不要安装不可信插件，也不要输入 API Key、账号密码、客户资料等敏感信息。"
        return "暂无明显风险"

    def _generate_empty_summary(self, date: str, total_fetched: int, labels: dict) -> str:
        """Generate summary when no high-scoring items were found."""
        return (
            f"# {labels['header']} - {date}\n\n"
            f"> {labels['empty_analyzed'].format(total=total_fetched)}\n\n"
            + labels["empty_body"]
        )
