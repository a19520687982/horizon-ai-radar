---
layout: default
title: "Horizon Summary: 2026-07-23 (ZH)"
date: 2026-07-23
lang: zh
---

> 从 65 条内容中筛选出 12 条重要资讯。

> 排序按“机会优先”展示，不完全按分数。能马上试用、能做内容/自动化/电商提效的内容会排在更前面。

---

1. [微软开源 Fara1.5 浏览器 AI 代理：能自动点网页、填表单，但普通人还需等待](#item-1) ⭐️ 8.0/10
2. [单 HTML 文件制作 PPT：Bento，无需安装离线可用](#item-2) ⭐️ 8.0/10
3. [OpenAI 推出企业级 AI 代理平台 Presence：了解 AI 客服与流程自动化的新趋势](#item-3) ⭐️ 7.0/10
4. [MindControl：引导本地 AI 模型推理的开源工具，适合技术爱好者](#item-4) ⭐️ 5.0/10
5. [阿里千问 Qwen-Image-3.0 图像模型升级：支持更长文字描述，生成更精准图片](#item-5) ⭐️ 7.0/10
6. [有人用 AI 建了一个获奖非虚构书籍索引网站，这是 AI 好用的例子](#item-6) ⭐️ 6.0/10
7. [AI 生成菜单和标牌越来越常见，但可能让顾客觉得没诚意](#item-7) ⭐️ 6.0/10
8. [数学家陶哲轩用 ChatGPT 探索数学猜想：这告诉我们如何向 AI 提出好问题](#item-8) ⭐️ 7.0/10
9. [奥地利政府为 18 万员工部署 AI 助手：Mistral 模型+开放界面，普通人能学到什么？](#item-9) ⭐️ 6.0/10
10. [新闻机构用 AI 做什么？从事实核查到内容推荐，这些案例值得内容创作者参考](#item-10) ⭐️ 7.0/10
11. [付费搜索引擎 Kagi 是什么？适合隐私敏感的用户吗？](#item-11) ⭐️ 5.0/10
12. [AI 模型是否被刻意训练画'骑自行车的鹈鹕'？一项趣味调查给出答案](#item-12) ⭐️ 6.0/10

---

## 专题：AI 编程工具

<a id="item-1"></a>
### 微软开源 Fara1.5 浏览器 AI 代理：能自动点网页、填表单，但普通人还需等待 ⭐️ 8.0/10

**类型：**
新 AI 工具

**一句话总结：**
微软发布 Fara1.5-27B 模型，能通过看截图自动操作浏览器，完成填表、搜索、预订等网页任务。

**它特别在哪里：**
它不依赖网页底层代码（DOM），只通过屏幕截图理解页面，然后模拟点击、输入、滚动等动作，实现端到端自动化。模型开源免费，性能优于 OpenAI Operator。

**对我有什么用：**
对技术团队：可用它搭建网页自动化工具，节省重复劳动。对普通人：概念有用，但目前需要编程能力才能部署使用。自媒体创作者可以介绍这类 AI 代理如何改变工作方式。

**自媒体机会：**
1. 选题：《微软开源“眼睛+手”AI：自己看网页截图，帮你填表下单》
2. 选题：《网页自动化新工具：Fara1.5 vs OpenAI Operator，谁更强？》

**电商/赚钱机会：**
间接机会：技术团队可接入该模型，开发自动化服务（如自动比价、批量商品上架）。普通人暂无明显直接赚钱机会。

**我该不该学：**
可以了解。了解 AI 代理如何通过视觉理解屏幕并操作，无需深究代码。想深入的可学习多模态模型和浏览器自动化概念。

**建议动作：**
收藏。关注后续有没有简化版的工具，等待更易用的封装产品出现。

**风险提醒：**
开源模型，自行部署需要技术背景，不建议新手直接运行。使用模型时注意不要输入敏感账号密码，避免被恶意利用。 新手不要随便运行陌生命令，不要安装不可信插件，也不要输入 API Key、账号密码、客户资料等敏感信息。

**来源和参考链接：**
reddit · r/LocalLLaMA · /u/pmttyji · 7月22日 18:04
- [原文](https://www.reddit.com/r/LocalLLaMA/comments/1v3ny84/microsoftfara1527b_hugging_face/)
- [Fara1.5 - A family of frontier computer use agent models - Microsoft Research](https://www.microsoft.com/en-us/research/articles/fara1-5-computer-use-agent/)
- [Microsoft Releases Fara1.5: A Family of Browser Computer-Use Agents (4B/9B/27B) That Outperform OpenAI Operator and Gemini 2.5 Computer Use on Online-Mind2Web - MarkTechPost](https://www.marktechpost.com/2026/05/22/microsoft-releases-fara1-5-a-family-of-browser-computer-use-agents-4b-9b-27b-that-outperform-openai-operator-and-gemini-2-5-computer-use-on-online-mind2web/)

**核实状态：**
社区来源/爆料内容，未核实，需要二次核实。


---

<a id="item-2"></a>
### MindControl：引导本地 AI 模型推理的开源工具，适合技术爱好者 ⭐️ 5.0/10

**类型：**
GitHub 新项目

**一句话总结：**
通过给 AI 模型推理过程“加提示”，防止它钻进死胡同或胡言乱语。

**它特别在哪里：**
它直接在模型思考时插入“提醒语句”，比如“你还有多少思考预算，快点总结”，从而改善推理质量。

**对我有什么用：**
对普通用户来说，直接使用门槛较高，需要懂编程和本地部署；但如果你是 AI 爱好者或开发者，可以试试优化本地小模型的推理表现。

**自媒体机会：**
适合制作科普或教程视频，比如“如何让 AI 不犯傻？这个开源项目教你引导模型思考”，或者“本地模型为什么不听话？一招改善推理”。

**电商/赚钱机会：**
间接机会：可作为技术咨询或定制服务卖给需要稳定推理的企业；直接卖工具或商品暂不明显。

**我该不该学：**
可以了解。如果想深入，推荐学习 llama.cpp 的使用和 AI 推理原理。

**建议动作：**
收藏。如果你有本地模型部署经验，可以尝试 fork 并测试效果。

**风险提醒：**
开源项目，不要随意运行不明代码；本地部署需注意安全，避免泄露隐私。 新手不要随便运行陌生命令，不要安装不可信插件，也不要输入 API Key、账号密码、客户资料等敏感信息。

**来源和参考链接：**
reddit · r/LocalLLaMA · /u/hellajacked · 7月22日 17:24
- [原文](https://www.reddit.com/r/LocalLLaMA/comments/1v3ms3c/mindcontrol_llamacpp_fork_to_guide_the_reasoning/)
- [llama . cpp - Wikipedia](https://en.wikipedia.org/wiki/Llama.cpp)
- [GitHub - ggml-org/ llama . cpp at xavier-geerinck · GitHub](https://github.com/ggml-org/llama.cpp?ref=xavier-geerinck)
- [How to Use llama . cpp to Run LLaMA Models Locally | Codecademy](https://www.codecademy.com/article/llama-cpp)
- [#LINKED0030 Large Language Models (LLMs): A Deep Dive into...](https://www.linkedin.com/pulse/linked0030-large-language-models-llms-deep-dive-tokens-sonawane-mry8f)
- [Exploring token sampling controls in large language models ...](https://ondiversity.cloud/blog/exploring-token-sampling-controls-in-large-language-models-a-comprehensive-guide)
- [Mechanism Design for Large Language Models](https://arxiv.org/pdf/2310.10826)
- [Do Think Tags Really Help LLMs Plan?](https://openreview.net/pdf?id=s3myOqKfhg)
- [The Ultimate Guide to LLM Reasoning (2025)](https://kili-technology.com/blog/llm-reasoning-guide)
- [GitHub - atfortes/Awesome- LLM - Reasoning : From Chain-of- Thought ...](https://github.com/atfortes/Awesome-LLM-Reasoning)

**核实状态：**
社区来源/爆料内容，未核实，需要二次核实。


---

<a id="item-3"></a>
### 有人用 AI 建了一个获奖非虚构书籍索引网站，这是 AI 好用的例子 ⭐️ 6.0/10

**类型：**
新 AI 工具

**一句话总结：**
一位非技术背景的人利用 AI 辅助编程，创建了一个收录获奖非虚构书籍的索引网站，证明 AI 可以用于制作高质量实用工具，而非只生成垃圾内容。

**它特别在哪里：**
创建者并非专业程序员，而是借助 AI（如 Cursor、Claude）完成数据收集和编码，展示了 AI 降低编程门槛、让有领域知识的人能快速构建有用工具的能力。

**对我有什么用：**
对普通人：可以用该网站发现获奖书籍，节省选书时间。对小团队/自媒体：可以借鉴思路，用 AI 创建小众领域的聚合工具（如获奖电影、优质播客等），吸引垂直流量。对创业者：验证了“AI 辅助编程+领域知识=轻量级工具”的可行性，可用于快速原型验证。

**自媒体机会：**
机会明显。选题 1：『用 AI 做了个获奖书籍网站，过程比你想的简单』，分享 AI 辅助编程的实操经验。选题 2：『AI 能帮你做这些正经事，不只是聊天写诗』，讨论 AI 的正面应用场景。

**电商/赚钱机会：**
间接机会。可以基于类似思路开发付费订阅的“优质资源索引”网站（如精选书单、工具集），或为垂直领域定制索引工具并收取服务费。直接电商机会暂不明显。

**我该不该学：**
可以了解。重点学习“如何用 AI 辅助编程（如 Cursor、Claude）快速实现一个简单的网站或工具”，无需先精通编程语言。

**建议动作：**
试用。访问 book-prize-index.vercel.app 体验网站功能，感受 AI 工具的实际产出。

**风险提醒：**
暂无明显风险。使用 AI 编程时注意不要直接复制运行不明代码，尤其是涉及网络请求的部分。

**来源和参考链接：**
hackernews · benbreen · 7月22日 14:18
- [原文](https://resobscura.substack.com/p/quality-non-fiction-books-are-the)
- [社区讨论](https://news.ycombinator.com/item?id=49007247)


---

<a id="item-4"></a>
### AI 生成菜单和标牌越来越常见，但可能让顾客觉得没诚意 ⭐️ 6.0/10

**类型：**
AI 行业趋势

**一句话总结：**
AI 设计的菜单和海报虽然方便，但消费者可能觉得缺乏个性、不可信，小商家需要注意。

**它特别在哪里：**
文章和讨论指出 AI 设计在低成本的同时，可能带来信任危机，尤其影响餐饮和小店的品牌形象。

**对我有什么用：**
提醒小商家和内容创作者：使用 AI 设计时要考虑顾客感受，避免千篇一律；自媒体可借此讨论 AI 设计的利弊。

**自媒体机会：**
可以制作短视频或图文，如：“为什么你家 AI 菜单看起来那么廉价？”、“AI 设计的三个坑：如何不让顾客觉得你敷衍”

**电商/赚钱机会：**
间接机会：提供人工菜单/标牌设计服务、AI 设计调优咨询、或者教商家如何让 AI 生成更有特色的设计（课程或模板）。

**我该不该学：**
可以了解：这不是技术学习，而是了解市场对 AI 设计的真实反馈，对经营或创作有帮助。

**建议动作：**
收藏：如果你经营实体店或用 AI 做设计，注意避免文中的负面效果；自媒体可准备选题。

**来源和参考链接：**
hackernews · speckx · 7月22日 12:49
- [原文](https://blog.fiddery.com/businesses-with-ugly-ai-menu-redesigns/)
- [社区讨论](https://news.ycombinator.com/item?id=49005973)


---

<a id="item-5"></a>
### 数学家陶哲轩用 ChatGPT 探索数学猜想：这告诉我们如何向 AI 提出好问题 ⭐️ 7.0/10

**类型：**
AI 行业趋势

**一句话总结：**
著名数学家陶哲轩分享了他与 ChatGPT 讨论雅可比猜想反例的对话，展示了专家如何通过精准提问让 AI 发挥深度推理能力。

**它特别在哪里：**
它特别在于不是普通的问答，而是专家通过连续、有策略的提问引导 AI 一步步深入数学问题，最终辅助发现反例，体现了 AI 在高度专业化领域的辅助价值。

**对我有什么用：**
对普通人：它教你提问比答案更重要，即使不懂数学，也能学习如何结构化、分步骤地向 AI 提出问题，从而获得更有用的答案。对自媒体和内容创作者：可以制作关于“提问技巧”、“AI 深度使用案例”的内容。

**自媒体机会：**
适合做短视频或图文讲解，选题如：“如何像数学家一样向 ChatGPT 提问？”、“陶哲轩的 GPT 对话教会我们什么？”

**电商/赚钱机会：**
暂无明显直接赚钱机会，但可以作为 AI 咨询服务或付费内容（如课程）的素材，间接提升专业形象。

**我该不该学：**
值得学：学习提问技巧，特别是如何分步骤、使用专业术语、让 AI 逐步深入分析。即使没有数学背景，也能提升与 AI 互动的效率。

**建议动作：**
收藏案例，研究陶哲轩的提问方式，尝试在自己的专业领域复制类似的深度对话。

**风险提醒：**
暂无明显风险，但注意 AI 回答可能出错，需要专业判断。

**来源和参考链接：**
hackernews · gmays · 7月22日 17:30
- [原文](https://chatgpt.com/share/6a5fdc7a-d6f8-83e8-bbea-8deb42cfed56)
- [社区讨论](https://news.ycombinator.com/item?id=49010345)
- [Jacobian conjecture](https://en.wikipedia.org/wiki/Jacobian_conjecture)


---

<a id="item-6"></a>
### 新闻机构用 AI 做什么？从事实核查到内容推荐，这些案例值得内容创作者参考 ⭐️ 7.0/10

**类型：**
AI 行业趋势

**一句话总结：**
OpenAI 分享新闻机构如何用 AI 提升报道质量、扩大受众和优化运营，展示了 AI 在内容行业中的实用价值。

**它特别在哪里：**
这不是技术介绍，而是新闻机构的真实应用案例，涵盖事实核查、摘要生成、个性化推荐等场景，说明 AI 已深入新闻生产全流程。

**对我有什么用：**
对于自媒体、内容创业者和小团队，可以借鉴这些思路：用 AI 辅助写稿、自动生成摘要、分析读者偏好、提高内容生产效率。不需要懂代码，只需要了解工具的使用场景。

**自媒体机会：**
适合做成“新闻机构用 AI 的 5 个真实案例”类短视频或图文，标题示例：“原来新闻编辑部这样用 AI？小白也能学会的创作提效技巧”

**电商/赚钱机会：**
间接机会：可以围绕“AI+内容”提供咨询服务或课程，教其他内容创作者如何用 AI 工具优化文案、生成配图、分析数据。直接机会不明显。

**我该不该学：**
可以了解。重点学习新闻机构使用 AI 的具体场景（如事实核查、摘要、推荐），以及对应的 AI 工具（如 ChatGPT、Claude 等）如何辅助内容创作。

**建议动作：**
收藏。阅读文章中的案例，思考哪些可以应用到自己的内容生产中。

**风险提醒：**
暂无明显风险。但注意 AI 生成内容需人工审核，避免传播不实信息。

**来源和参考链接：**
rss · OpenAI Blog · 7月22日 13:00
- [原文](https://openai.com/index/how-news-organizations-are-using-ai)
- [How news organizations are using AI to advance their vital... | OpenAI](https://openai.com/index/how-news-organizations-are-using-ai/)
- [Top OpenAI Tools , Examples & Use Cases - Flatlogic Blog](https://flatlogic.com/blog/top-openai-tools-examples-use-cases/)


---

## 专题：AI 学习机会

<a id="item-7"></a>
### 单 HTML 文件制作 PPT：Bento，无需安装离线可用 ⭐️ 8.0/10

**类型：**
新 AI 工具

**一句话总结：**
Bento 是一个单 HTML 文件，能直接制作、编辑、演示和协作 PPT，无需安装或联网，还支持用 AI 将 pptx 文件转换进来。

**它特别在哪里：**
所有内容（编辑、查看、协作）都在一个 560KB 左右的 HTML 文件里，完全离线运行，无需任何安装或登录，还能通过加密盲中继实现实时协作。

**对我有什么用：**
对普通人来说，不用安装软件、不用登录账号，拿到一个 HTML 文件就能打开做演示，方便快捷；小团队可以把它当作轻量级协作工具，无需搭建服务器；自媒体可用来制作在线教程或分享材料。

**自媒体机会：**
可以制作“如何用 Bento 快速搞定演示文稿”“比 PPT 更轻量的在线工具”等教程或对比视频。

**电商/赚钱机会：**
暂无明显赚钱机会，但可以销售定制模板或提供将 pptx 转换为 Bento 格式的服务。

**我该不该学：**
可以了解，无需学习编程，直接下载使用即可。

**建议动作：**
试用：访问 bento.page/slides/ 体验在线编辑，或下载 HTML 文件离线使用。

**风险提醒：**
暂无明显风险，但注意该工具是开源项目，使用时不要随意修改核心代码，以免损坏文件。

**来源和参考链接：**
hackernews · starfallg · 7月22日 15:19
- [原文](https://bento.page/slides/)
- [社区讨论](https://news.ycombinator.com/item?id=49008211)


---

## 专题：AI 自动化和智能体

<a id="item-8"></a>
### OpenAI 推出企业级 AI 代理平台 Presence：了解 AI 客服与流程自动化的新趋势 ⭐️ 7.0/10

**类型：**
新 AI 工具

**一句话总结：**
OpenAI 发布了一个名为 Presence 的企业级 AI 代理平台，帮助企业部署语音和聊天机器人，用于客户服务和内部流程。

**它特别在哪里：**
这是 OpenAI 官方推出的企业级 AI 代理平台，已经用于 OpenAI 自己的客服热线（1-888-GPT-0090），能处理开放式问题、验证来电者身份、使用账户上下文并执行授权操作，说明其成熟度较高。

**对我有什么用：**
对普通人：了解 AI 代理如何应用于客服和内部流程，可能启发你所在公司或服务的使用。对小团队或创业者：可以学习这一模式，考虑是否能为中小企业提供类似的 AI 客服解决方案（但需要技术合作）。

**自媒体机会：**
可以做科普类内容：例如“企业 AI 代理是什么？OpenAI Presence 能做什么？”或“AI 客服会取代人工吗？从 OpenAI Presence 看未来”。

**电商/赚钱机会：**
间接机会：如果你有技术资源，可以为企业提供基于类似平台的 AI 客服部署服务。对于个人电商卖家，暂无明显直接机会，但可关注后续是否有面向中小企业的简化版本。

**我该不该学：**
可以了解：学习 AI 代理（AI Agent）的基本概念、客服自动化的工作流，以及如何评估企业级 AI 工具的优劣。暂时不必学具体开发细节。

**建议动作：**
收藏：先了解概念，观察是否有国内类似产品或 OpenAI 后续是否推出更平民化的版本。

**风险提醒：**
暂无明显风险。但需注意企业级工具通常有使用成本和数据安全要求，个人用户不要直接尝试部署到生产环境。 新手不要随便运行陌生命令，不要安装不可信插件，也不要输入 API Key、账号密码、客户资料等敏感信息。

**来源和参考链接：**
rss · OpenAI Blog · 7月22日 05:30
- [原文](https://openai.com/index/introducing-openai-presence)
- [Introducing OpenAI Presence | OpenAI](https://openai.com/index/introducing-openai-presence/)
- [OpenAI .fm](https://www.openai.fm/?ref=devmandan.com)
- [OpenAI establishes presence in Singapore to support international...](https://www.edb.gov.sg/en/about-edb/media-releases-publications/openai-establishes-presence-in-singapore-to-support-international-expansion.html)


---

<a id="item-9"></a>
### 奥地利政府为 18 万员工部署 AI 助手：Mistral 模型+开放界面，普通人能学到什么？ ⭐️ 6.0/10

**类型：**
AI 行业趋势

**一句话总结：**
奥地利政府用开源 AI 模型（Mistral）和免费界面（Open WebUI）搭建了内部 AI 平台，供 18 万公务员处理文档分析、知识库等工作。

**它特别在哪里：**
这是目前已知最大规模的政府级开源 AI 部署案例，使用了可本地部署的模型和界面，强调主权和可控性。

**对我有什么用：**
对普通人来说，这不是一个可以直接使用的工具，但它展示了 AI 在政府/企业中的真实落地场景。自媒体创作者可以借此案例讲解 AI 如何提高办公效率，或分析开源模型的安全性优势。创业者可以思考为中小企业或机构提供类似本地化 AI 部署服务的商机。

**自媒体机会：**
适合做短视频或图文分析，选题如：
1. "国家级 AI 落地：奥地利政府用开源模型办公，中国公务员能用吗？"
2. "别只知道 ChatGPT，看看政府怎么用 AI 处理公文"

**电商/赚钱机会：**
间接机会：可围绕“企业级 AI 部署”提供咨询、方案设计或培训服务。直接机会暂不明显。

**我该不该学：**
可以了解。如果你对企业级 AI 落地或开源模型感兴趣，可以学习 Mistral 模型的特点和 Open WebUI 的部署方式，但无需深入代码。

**建议动作：**
收藏。关注更多政府/企业 AI 落地案例，作为内容素材或商机储备。

**风险提醒：**
暂无明显风险。但若计划模仿部署开源模型，需注意数据安全与合规。 新手不要随便运行陌生命令，不要安装不可信插件，也不要输入 API Key、账号密码、客户资料等敏感信息。

**来源和参考链接：**
reddit · r/LocalLLaMA · /u/ClassicMain · 7月22日 14:28
- [原文](https://www.reddit.com/r/LocalLLaMA/comments/1v3hra4/austria_is_rolling_out_a_government_aiplatform/)
- [Models - from cloud to edge | Mistral](https://mistral.ai/models/)
- [Open WebUI : Self-Hosted AI Platform](https://openwebui.com/)

**核实状态：**
社区来源/爆料内容，未核实，需要二次核实。


---

## 专题：AI 图像/视频/语音

<a id="item-10"></a>
### 阿里千问 Qwen-Image-3.0 图像模型升级：支持更长文字描述，生成更精准图片 ⭐️ 7.0/10

**类型：**
新 AI 工具

**一句话总结：**
阿里千问发布新图像模型，支持更多文字输入（4500 个词），可生成带文字、公式、多语言的复杂图片，适合做海报、知识图解等。

**它特别在哪里：**
文本输入长度提升 4.5 倍，支持 12 种语言和 20 多种字体原生渲染，可以一次生成包含公式、图表、UI 界面等元素的图片，文字清晰可读。

**对我有什么用：**
自媒体创作者、电商卖家、设计师可以用更详细的描述快速生成配图、海报、产品展示图，减少反复修改，节省时间。非技术用户也能上手。

**自媒体机会：**
适合做教程内容，例如：“如何用千问写长描述生成完美海报”“实测 Qwen-Image-3.0：写 200 字描述能生成多复杂的图？”

**电商/赚钱机会：**
直接机会：用该工具生成电商产品主图、详情页配图、多语言海报，低成本制作商业素材。间接机会：提供代做图片服务或批量设计服务。

**我该不该学：**
可以了解。主要学习如何撰写详细的文字描述来引导 AI 生成理想图片，不需要掌握代码。

**建议动作：**
试用。去千问官方平台或 API 尝试 Qwen-Image-3.0，测试长文本描述的效果，熟悉其能力边界。

**风险提醒：**
暂无明显风险。注意：如果通过 API 调用，需关注计费规则；生成图片可能涉及版权，商用前请确认授权条款。

**来源和参考链接：**
rss · InfoQ 中文站 · 7月22日 17:42
- [原文](https://www.infoq.cn/article/jXQ5oQeOcEjLkuq2Qc0y?utm_source=rss&utm_medium=article)
- [阿里千问发布 Qwen-Image-3.0 图像生成基础模型：落字成画，字字如印 - 行业动态 - 资讯 - AI 中文社区](https://www.aizws.net/news/detail/10851)
- [I tried out the image generation AI 'Qwen-Image-3.0,' but how does it perform in rendering illustrations and Japanese text? - GIGAZINE](https://gigazine.net/gsc_news/en/20260722-qwen-image-3/)
- [阿里发布Qwen-Image-3.0图像模型，支持超长指令复杂图文生成_新浪财经_新浪网](https://finance.sina.com.cn/tech/shenji/2026-07-21/doc-iniipxxk4931252.shtml)


---

## 可忽略噪音（简略）

这些内容不放进重点正文，只保留标题方便回看。

<a id="item-11"></a>
### 付费搜索引擎 Kagi 是什么？适合隐私敏感的用户吗？ ⭐️ 5.0/10

Kagi 是一款无广告、注重隐私的付费搜索引擎，用户可自定义搜索结果并选择是否使用 AI，但月费较高且网络内容质量下降影响体验。

hackernews · speckx · 7月22日 13:08

---

<a id="item-12"></a>
### AI 模型是否被刻意训练画'骑自行车的鹈鹕'？一项趣味调查给出答案 ⭐️ 6.0/10

有人用 48 组提示词测试多个 AI 模型，发现并没有证据表明模型被刻意训练生成'骑自行车的鹈鹕'图像，这只是一个有趣的网络梗。

rss · Simon Willison · 7月22日 23:01

---