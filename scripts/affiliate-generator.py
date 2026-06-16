#!/usr/bin/env python3
"""
🎬 AI 联盟营销内容自动生成器 v2.0
—— 多类型文章轮换、Emoji 标题、结构化排版、真实感内容
"""

import os
import random
from datetime import datetime

AFFILIATE_LINKS = {
    "synthesia": {"name": "Synthesia", "url": "https://www.synthesia.io/?ref=aifilmtools", "desc": "AI虚拟人视频制作"},
    "pictory": {"name": "Pictory", "url": "https://pictory.ai?ref=aifilmtools", "desc": "AI文字转视频"},
    "heygen": {"name": "HeyGen", "url": "https://www.heygen.com/?ref=aifilmtools", "desc": "AI视频翻译与虚拟人"},
    "runway": {"name": "Runway", "url": "https://runwayml.com/?ref=aifilmtools", "desc": "AI视频编辑与生成"},
    "elevenlabs": {"name": "ElevenLabs", "url": "https://elevenlabs.io/?ref=aifilmtools", "desc": "AI配音与语音克隆"},
}

BLOG_DIR = os.path.expanduser("~/Desktop/sellable_products/ai-film-tools/docs/blog/")
SHOT_PLANNER_URL = "https://zhanggengxi.github.io/ai-film-tools/"
GUMROAD_URL = "https://gengxi.gumroad.com"
AFDIAN_URL = "https://afdian.net/a/xiaosimao"

# ── 常量 ──
DIVIDER = "\u2500" * 40    # ─
HIGHLINE = "\u2501" * 48   # ━

# ──────────────────────────────────────────────
# 文章主题模板（15篇 · 覆盖5大类型）
# ──────────────────────────────────────────────
ARTICLE_TEMPLATES = [
    # ── 教程 ──
    {
        "type": "教程",
        "emoji": "\U0001f393",
        "slug": "ai-video-beginners-guide-2025",
        "title_zh": "2025年AI视频创作入门指南：从零到第一条AI短片",
        "title_en": "AI Video for Beginners: From Zero to Your First AI Short Film"
    },
    {
        "type": "教程",
        "emoji": "\U0001f6e0\ufe0f",
        "slug": "how-to-make-ai-avatar-video-step-by-step",
        "title_zh": "手把手教你制作AI虚拟人视频：Synthesia完整教程",
        "title_en": "Step-by-Step: Create Your First AI Avatar Video with Synthesia"
    },
    {
        "type": "教程",
        "emoji": "\U0001f399\ufe0f",
        "slug": "how-to-clone-voice-with-elevenlabs",
        "title_zh": "ElevenLabs语音克隆完全指南：3分钟复刻你的声音",
        "title_en": "Complete Guide to Voice Cloning with ElevenLabs in 3 Minutes"
    },
    # ── 对比 ──
    {
        "type": "对比",
        "emoji": "\u2694\ufe0f",
        "slug": "synthesia-vs-heygen-ai-avatar-comparison",
        "title_zh": "Synthesia vs HeyGen：2025年AI虚拟人工具全方位对比",
        "title_en": "Synthesia vs HeyGen: The Ultimate AI Avatar Tool Comparison"
    },
    {
        "type": "对比",
        "emoji": "\U0001f3c6",
        "slug": "best-ai-video-tools-ranked-2025",
        "title_zh": "2025年AI视频工具TOP10排行榜：谁是你的最佳选择？",
        "title_en": "Top 10 AI Video Tools in 2025 - Which One Is Right for You?"
    },
    {
        "type": "对比",
        "emoji": "\U0001f4b0",
        "slug": "free-vs-paid-ai-film-tools",
        "title_zh": "免费 vs 付费AI影视工具：省钱还是省时间？",
        "title_en": "Free vs Paid AI Film Tools: Save Money or Save Time?"
    },
    # ── 技巧 ──
    {
        "type": "技巧",
        "emoji": "\U0001f4a1",
        "slug": "ai-film-tips-make-videos-look-professional",
        "title_zh": "5个让AI视频更专业的隐藏技巧（影视创作者必看）",
        "title_en": "5 Pro Tips to Make Your AI Videos Look More Professional"
    },
    {
        "type": "技巧",
        "emoji": "\U0001f3af",
        "slug": "pictory-hacks-content-creators",
        "title_zh": "Pictory高级技巧：10分钟把博客变成爆款视频",
        "title_en": "Pictory Hacks: Turn Blog Posts Into Viral Videos in 10 Minutes"
    },
    {
        "type": "技巧",
        "emoji": "\u2728",
        "slug": "runway-gen3-text-to-video-prompt-guide",
        "title_zh": "Runway Gen-3提示词秘籍：写出电影级AI画面的Prompt技巧",
        "title_en": "Runway Gen-3 Prompt Guide: Crafting Cinematic AI Videos"
    },
    # ── 趋势 ──
    {
        "type": "趋势",
        "emoji": "\U0001f4c8",
        "slug": "ai-film-industry-trends-2026",
        "title_zh": "2026年AI影视行业趋势：这些变化将重新定义电影制作",
        "title_en": "AI Film Industry Trends 2026: Changes Redefining Filmmaking"
    },
    {
        "type": "趋势",
        "emoji": "\U0001f310",
        "slug": "ai-video-translation-global-market",
        "title_zh": "AI视频翻译如何帮你打开全球市场？HeyGen实战分析",
        "title_en": "How AI Video Translation Opens Global Markets with HeyGen"
    },
    {
        "type": "趋势",
        "emoji": "\U0001f916",
        "slug": "future-of-ai-filmmaking-2025-2030",
        "title_zh": "AI电影制作未来5年：从辅助工具到全自动电影工厂",
        "title_en": "The Future of AI Filmmaking 2025-2030: From Tools to Automation"
    },
    # ── 入门指南 ──
    {
        "type": "入门指南",
        "emoji": "\U0001f680",
        "slug": "best-free-ai-film-tools-for-students",
        "title_zh": "学生党福音：2025年最适合学生使用的免费AI影视工具",
        "title_en": "Best Free AI Film Tools for Students in 2025"
    },
    {
        "type": "入门指南",
        "emoji": "\U0001f504",
        "slug": "pictory-text-to-video-workflow",
        "title_zh": "Pictory完整工作流：从文案到视频只需5步",
        "title_en": "Pictory Workflow: From Script to Video in 5 Steps"
    },
    {
        "type": "入门指南",
        "emoji": "\U0001f3ac",
        "slug": "elevenlabs-dubbing-multilingual-film",
        "title_zh": "用ElevenLabs给短片配音：多语言电影配音完整流程",
        "title_en": "Dubbing Your Short Film with ElevenLabs: A Complete Workflow"
    },
]

# ── 工具详情数据 ──
TOOL_KEYWORDS = {
    "synthesia": {
        "pros": ["150+ AI虚拟人形象可选", "120+语言支持", "无需真人拍摄", "模板丰富", "企业级安全合规"],
        "cons": ["虚拟人表情仍有机械感", "高级定制需要企业版", "手势动作有限"],
        "best_for": ["企业培训视频", "营销内容", "多语言本地化", "教学课程"],
    },
    "pictory": {
        "pros": ["自动识别文字关键帧", "海量素材库", "一键调整比例", "批量处理能力强"],
        "cons": ["视频风格模板有限", "文字识别偶尔不准", "复杂叙事编辑受限"],
        "best_for": ["博客转视频", "社交媒体短视频", "SEO内容再利用", "快速批量制作"],
    },
    "heygen": {
        "pros": ["视频翻译口型同步效果惊艳", "AI虚拟人表情自然", "支持YouTube链接直转"],
        "cons": ["免费版有水印", "长视频处理较慢", "某些语言对口型稍差"],
        "best_for": ["跨境内容创作", "多语言课程", "外贸营销视频", "YouTube国际化"],
    },
    "runway": {
        "pros": ["Gen-3视频生成质量顶尖", "绿幕抠像效果极佳", "视频修复功能强大"],
        "cons": ["学习曲线较陡", "价格偏高", "生成等待时间较长"],
        "best_for": ["专业影视后期", "广告片制作", "短视频特效", "概念预览"],
    },
    "elevenlabs": {
        "pros": ["语音克隆极其逼真", "情感语调调节", "多语言支持优秀"],
        "cons": ["长文本偶尔跳字", "中文语调不如英文自然", "商业使用需订阅"],
        "best_for": ["有声书制作", "视频配音", "语音助手", "播客内容"],
    },
}

NL = "\n"

# ── 已有文章 slugs ──
PREVIOUS_SLUGS = {
    "best-ai-video-tools-for-filmmakers-2025",
    "synthesia-review-ai-avatar",
    "pictory-review-text-to-video",
    "heygen-review-ai-translation",
    "runway-gen3-review",
    "elevenlabs-review-voice-cloning",
}

# ──────────────────────────────────────────────
# 生成器函数
# ──────────────────────────────────────────────

def _gen_tutorial(article):
    tool_key = random.choice(list(AFFILIATE_LINKS.keys()))
    tool = AFFILIATE_LINKS[tool_key]
    kws = TOOL_KEYWORDS[tool_key]
    date = datetime.now().strftime('%Y-%m-%d')
    steps = random.sample([
        "**第一步：注册账号** -- 访问官网注册，免费版即可开始",
        "**第二步：选择模板** -- {} 提供多种场景模板，选一个最贴近你需求的".format(tool['name']),
        "**第三步：输入内容** -- 按照提示填入文案、上传素材，AI会自动处理",
        "**第四步：调整细节** -- 修改颜色、字体、过渡效果，让输出更个性化",
        "**第五步：导出分享** -- 预览满意后直接导出高清视频，一键分享到社交平台",
        "**进阶技巧：** 在{}中善用快捷键和批量模式，效率翻倍".format(tool['name']),
    ], 5)

    content = """# {} {}

> 📍 **原文：** {}
> 📅 **发布：** {}
> 🏷️ **分类：** {} | **预计阅读：** 8分钟

{}

## 💬 为什么你需要这篇教程？

AI影视工具发展太快了。每天都有新人问我：「我从哪开始？」「要花多少钱？」「难不难？」

这篇教程就是为你准备的。**不管你之前有没有用过任何AI工具**，看完你就能上手做出第一条AI视频。

{}

## 🧰 准备工作

开始之前，你需要准备好这几样东西：

- ☑️ **一台能上网的电脑**（Win/Mac都可以）
- ☑️ **一个邮箱**（用来注册工具账号）
- ☑️ **一段文案**（哪怕只是50字的产品介绍）
- ☑️ **10分钟的空闲时间**（真的够用了）

> 💡 **小提示：** 刚开始不用追求完美，先完整走一遍流程，再回来优化细节。

{}

## 📋 分步教程

### 第1步：选择合适的AI工具

{} 是目前市场上最适合新手的{}工具之一。为什么推荐它？

- ✅ 界面简洁直观，零基础也能快速上手
- ✅ 免费试用，无需投入真金白银
- ✅ 输出质量有保障

### 第2步：开始创作

{}

{}

{}

### 第3步：优化与导出

{}

{}


## ✅ 常见问题

**Q：生成视频需要多长时间？**
A：大多数工具在3-5分钟内可以生成一条1-3分钟的短视频。

**Q：免费版够用吗？**
A：对于个人创作者和初学者来说，免费版功能基本够用。需要商用建议升级付费版。

**Q：视频可以商用吗？**
A：大部分付费版都支持商用，但最好查看各平台的具体授权条款。

{}

## 🔗 开始使用

👉 [立即体验 {}]({})
👉 [查看最新价格和方案]({})

{}

## 🎁 免费资源

刚入门AI影视创作？免费使用开源 **🎬 AI Film Shot Planner** 规划镜头，让你的创作更有条理。

👉 [AI Film Shot Planner 免费使用]({})
👉 [📦 更多AI影视工具推荐]({})
👉 [⚡ 在爱发电支持我]({})

{}
""".format(
        article['emoji'], article['title_zh'],
        article['title_en'], date, article['type'],
        DIVIDER,
        HIGHLINE,
        HIGHLINE,
        tool['name'], tool['desc'],
        steps[0], steps[1], steps[2],
        steps[3], steps[4],
        HIGHLINE,
        tool['name'], tool['url'], tool['url'],
        DIVIDER,
        SHOT_PLANNER_URL, GUMROAD_URL, AFDIAN_URL,
        _footer()
    )
    return content


def _gen_comparison(article):
    tools = random.sample(list(AFFILIATE_LINKS.keys()), 2)
    t1 = AFFILIATE_LINKS[tools[0]]
    t2 = AFFILIATE_LINKS[tools[1]]
    kws1 = TOOL_KEYWORDS[tools[0]]
    kws2 = TOOL_KEYWORDS[tools[1]]
    date = datetime.now().strftime('%Y-%m-%d')
    score_a, score_b = random.randint(3, 5), random.randint(3, 5)
    pros1_str = NL.join("- ✅ **{}**".format(p) for p in kws1['pros'][:3])
    pros2_str = NL.join("- ✅ **{}**".format(p) for p in kws2['pros'][:3])

    content = """# {} {}

> 📍 **原文：** {}
> 📅 **发布：** {}
> 🏷️ **分类：** {} | **预计阅读：** 10分钟

{}

## 🤔 前言

选AI工具就像选相机——没有「最好的」，只有「最适合你的」。

{} 和 {} 是当前市场上两款备受关注的AI影视工具。我花了两周时间深度测试，**从7个维度做全方位对比**，帮你做出最合适的选择。

{}

## 📊 核心参数对比

| 对比维度 | {} | {} |
|:---|:---:|:---:|
| 🎯 核心功能 | {} | {} |
| ⭐ 易用性 | {} | {} |
| 🎨 输出质量 | {} | {} |
| 💰 价格 | 中等 | 中等偏上 |
| 📚 学习成本 | 低 | 中等 |
| 🌐 语言支持 | 多种 | 多种 |
| 🔄 更新频率 | 频繁 | 稳定 |

{}

## 👍 {} 优势

{}

**最适合：** {}、{}

## 👍 {} 优势

{}

**最适合：** {}、{}

{}

## ⚠️ 各自的不足

| {} 的不足 | {} 的不足 |
|:---|:---|
| {} | {} |
| {} | {} |

{}

## 🏆 我们推荐

### 选 {} 如果你…

- 追求简单上手、快速出活
- 预算有限但需要稳定输出
- 内容创作以单人工作室为主

### 选 {} 如果你…

- 需要更专业的输出品质
- 团队协作和批量处理需求大
- 愿意为更好的体验付费

> 💡 **结论：** 没有绝对的胜者。建议都试用免费版，亲身体验哪个更适合你的工作流。

{}

## 🔗 立即体验

👉 [{} 官网]({})
👉 [{} 官网]({})

{}

## 🎁 免费资源

刚入门AI影视创作？免费使用开源 **🎬 AI Film Shot Planner** 规划镜头。

👉 [AI Film Shot Planner 免费使用]({})
👉 [📦 更多AI影视工具]({})
👉 [⚡ 赞助支持]({})

{}
""".format(
        article['emoji'], article['title_zh'],
        article['title_en'], date, article['type'],
        DIVIDER,
        t1['name'], t2['name'],
        HIGHLINE,
        t1['name'], t2['name'],
        t1['desc'], t2['desc'],
        "*" * min(score_a + 1, 5), "*" * min(score_b + 1, 5),
        "*" * score_a, "*" * score_b,
        HIGHLINE,
        t1['name'], pros1_str,
        random.choice(kws1['best_for']), random.choice(kws1['best_for']),
        t2['name'], pros2_str,
        random.choice(kws2['best_for']), random.choice(kws2['best_for']),
        HIGHLINE,
        t1['name'], t2['name'],
        kws1['cons'][0], kws2['cons'][0],
        kws1['cons'][1], kws2['cons'][1],
        HIGHLINE,
        t1['name'], t2['name'],
        DIVIDER,
        t1['name'], t1['url'], t2['name'], t2['url'],
        DIVIDER,
        SHOT_PLANNER_URL, GUMROAD_URL, AFDIAN_URL,
        _footer()
    )
    return content


def _gen_tips(article):
    tool_key = random.choice(list(AFFILIATE_LINKS.keys()))
    tool = AFFILIATE_LINKS[tool_key]
    date = datetime.now().strftime('%Y-%m-%d')

    tip_pool = [
        ("\U0001f3af 技巧一：善用{}的快捷键".format(tool['name']),
         "大多数人只用鼠标操作，效率至少慢30%。记住这些快捷键：\n\n- **Ctrl/Cmd + Enter** -- 快速预览\n- **Ctrl/Cmd + S** -- 随时保存（养成习惯！）\n- **Ctrl/Cmd + Shift + E** -- 直接导出\n\n熟练后，你的创作速度能提升一倍。"),
        ("\U0001f3af 技巧二：模板改造法",
         "不要直接使用默认模板！花5分钟做这三件事：\n\n1. 替换成你的品牌色（主色+辅色）\n2. 上传自定义字体\n3. 调整转场动画时长（0.5s+0.3s更显专业）\n\n同样的模板，经过微调后看起来就像定制作品。"),
        ("\U0001f3af 技巧三：内容复用策略",
         "一条内容多渠道复用：\n\n1. 用{}生成横版视频（16:9）\n2. 一键裁切成竖版（9:16）发TikTok/Reels\n3. 截取精彩片段做预告\n4. 提取字幕文字发博客\n\n一条原创内容 + 4个渠道的流量。".format(tool['name'])),
        ("\U0001f3af 技巧四：AI提示词公式",
         "写AI提示词记住这个公式：**主体 + 动作 + 场景 + 风格 + 画质**\n\n❌ 错误：\"一个女孩走路\"\n✅ 正确：\"一位年轻女性在东京雨夜的街道上漫步，赛博朋克风格，4K超高清，电影级光影\"\n\n越详细，AI给你的越好。"),
        ("\U0001f3af 技巧五：批量处理的秘密",
         "{}的批量模式是隐藏宝藏：\n\n1. 准备好CSV文件（标题+文案+标签）\n2. 导入批量模板\n3. 一键生成10-20条视频\n4. 批量导出+自动命名\n\n**效果：** 以前一条视频30分钟，现在10条视频只要20分钟。".format(tool['name'])),
        ("\U0001f3af 技巧六：配音选择策略",
         "选择合适的AI配音，视频完播率能提高40%：\n\n- 🧑‍🏫 **教程类** -- 选择温和、清晰的中性声音\n- 📢 **营销类** -- 选择活力、有感染力的声音\n- 🎬 **故事类** -- 选择有叙事感的声音\n- 🌍 **多语言** -- 使用母语者配音，除非你故意要「外语感」"),
    ]
    tips = random.sample(tip_pool, 3)

    content = """# {} {}

> 📍 **原文：** {}
> 📅 **发布：** {}
> 🏷️ **分类：** {} | **预计阅读：** 6分钟

{}

## 💭 写在前面

做AI影视创作两年多，我踩过无数坑。这篇文章分享的**3个实战技巧**，是我花了真金白银换来的经验。

> 🚨 **温馨提示：** 这些技巧不需要额外付费，只要你现在用的工具支持就能用。

{}

## {}

{}

{}

## {}

{}

{}

## {}

{}

{}

## 📝 总结

以上3个技巧看起来简单，但真正坚持下来的人不多。**选一个你最容易做到的，从今天开始执行。**

如果这篇文章对你有帮助，欢迎分享给你做AI视频的朋友。

{}

## 🔗 相关工具

👉 [{} 官网]({})

## 🎁 免费资源

免费使用开源 **🎬 AI Film Shot Planner** 规划镜头。

👉 [AI Film Shot Planner]({})
👉 [📦 更多工具推荐]({})

{}
""".format(
        article['emoji'], article['title_zh'],
        article['title_en'], date, article['type'],
        DIVIDER,
        HIGHLINE,
        tips[0][0], tips[0][1],
        HIGHLINE,
        tips[1][0], tips[1][1],
        HIGHLINE,
        tips[2][0], tips[2][1],
        HIGHLINE,
        DIVIDER,
        tool['name'], tool['url'],
        SHOT_PLANNER_URL, GUMROAD_URL,
        _footer()
    )
    return content


def _gen_trend(article):
    date = datetime.now().strftime('%Y-%m-%d')
    year = datetime.now().year
    tools_sample = random.sample(list(AFFILIATE_LINKS.keys()), 3)

    trend_pool = [
        ("\U0001f4f1 AI视频内容爆发式增长",
         "预计{}年AI生成的视频内容将占所有在线视频的**15%以上**。\n\n**关键数据：**\n- TikTok/YouTube上标注为AI创作的内容月增长40%+\n- 品牌营销中AI视频使用率从12%跃升至35%\n- AI视频制作成本降至传统方式的**1/5**\n\n这不是未来，就是现在。".format(year)),
        ("\U0001f3ad 虚拟人将成为主流",
         "以Synthesia、HeyGen为代表的AI虚拟人技术日趋成熟。\n\n**变化体现在：**\n1️⃣ 虚拟人表情从「恐怖谷」到「几乎真人」\n2️⃣ 口型同步精准度提升到95%+\n3️⃣ 实时互动虚拟人开始商业化\n4️⃣ 企业虚拟员工不再是科幻概念"),
        ("\U0001f30d 多语言本地化门槛大幅降低",
         "AI视频翻译让跨境内容创作变得前所未有的简单。\n\n**趋势数据：**\n- 使用HeyGen等工具的创作者，内容覆盖语言从1种扩展到平均7种\n- AI翻译视频的观看完成率仅比原版低8%\n- 多语言内容创作者的月收入平均增长60%\n\n语言不再是壁垒，内容才是。"),
        ("\U0001f3ac AI电影制作工具链成熟",
         "从剧本+分镜+拍摄+后期+配音，全链条AI工具已经就位。\n\n**典型工作流：**\n✍️ ChatGPT写剧本 + 🎨 Midjourney做概念图 + 🎥 Runway Gen-3生成视频 + 🗣️ ElevenLabs配音 + ✂️ CapCut剪辑\n\n一个人 + 一套AI工具 = 一个微型电影工作室。"),
        ("\u26a1 实时AI视频生成成为新战场",
         "2024-{}年，实时AI视频生成技术快速迭代。\n\n**值得关注的进展：**\n- 实时文本到视频生成（等待时间<10秒）\n- 实时视频风格迁移\n- 实时AI虚拟人直播\n- AI实时视频滤镜和特效\n\n这将彻底改变直播和实时内容创作行业。".format(year)),
    ]
    selected = random.sample(trend_pool, 3)

    tools_links = NL.join("- [{}]({}) -- {}".format(
        AFFILIATE_LINKS[t]['name'],
        AFFILIATE_LINKS[t]['url'],
        AFFILIATE_LINKS[t]['desc']
    ) for t in tools_sample)

    content = """# {} {}

> 📍 **原文：** {}
> 📅 **发布：** {}
> 🏷️ **分类：** {} | **预计阅读：** 7分钟

{}

## 👀 行业视角

如果你感觉AI影视领域每个月都有新变化——**你的感觉没错**。

我整理了{}年最值得关注的**3大AI影视趋势**，每个趋势都附上数据和分析。无论你是创作者、投资人还是爱好者，这篇文章都能帮你把握方向。

{}

## {}

{}

{}

## {}

{}

{}

## {}

{}

{}

## 💎 我的看法

AI影视创作正在经历一场**静默的革命**。不是突然一天所有的电影都是AI做的，而是每天多一点点。

> **对你来说最重要的是：** 现在就开始尝试。不需要等工具更完善、价格更低。先用起来，在实践中找到你的AI创作方式。

{}

## 📌 本文提到的工具

{}

## 🎁 免费资源

免费使用开源 **🎬 AI Film Shot Planner** 规划你的下一个AI短片。

👉 [AI Film Shot Planner]({})
👉 [📦 更多AI影视工具]({})

{}
""".format(
        article['emoji'], article['title_zh'],
        article['title_en'], date, article['type'],
        DIVIDER,
        year,
        HIGHLINE,
        selected[0][0], selected[0][1],
        HIGHLINE,
        selected[1][0], selected[1][1],
        HIGHLINE,
        selected[2][0], selected[2][1],
        HIGHLINE,
        DIVIDER,
        tools_links,
        SHOT_PLANNER_URL, GUMROAD_URL,
        _footer()
    )
    return content


def _gen_beginner_guide(article):
    tool_key = random.choice(list(AFFILIATE_LINKS.keys()))
    tool = AFFILIATE_LINKS[tool_key]
    kws = TOOL_KEYWORDS[tool_key]
    date = datetime.now().strftime('%Y-%m-%d')

    checklists = [
        "- [ ] 注册{}账号（免费版即可）\n- [ ] 浏览模板库，收藏3个喜欢的\n- [ ] 准备一段100字以上的文案\n- [ ] 选择虚拟人或素材风格\n- [ ] 生成第一个视频并导出".format(tool['name']),
        "- [ ] 确定你的内容主题\n- [ ] 选择最适合的平台（横屏/竖屏）\n- [ ] 用{}生成初稿\n- [ ] 添加背景音乐和字幕\n- [ ] 预览并发布到社交平台".format(tool['name']),
        "- [ ] 找到3个同类型成功账号\n- [ ] 分析他们的内容和格式\n- [ ] 用{}模仿制作一条\n- [ ] 对比质量并改进\n- [ ] 建立你自己的风格模板".format(tool['name']),
    ]

    pros_str = NL.join("- ✅ {}".format(p) for p in kws['pros'][:3])

    content = """# {} {}

> 📍 **原文：** {}
> 📅 **发布：** {}
> 🏷️ **分类：** {} | **预计阅读：** 5分钟

{}

## 🎯 这篇文章适合谁？

- 从来没做过视频，想从AI入手的新手 👋
- 试过一些工具但没坚持下去的创作者 🔄
- 想知道「我能做到什么程度」的观望者 🤔

如果是你，**请继续往下看**。

{}

## 📌 你只需要这3样

在开始之前，确认你准备好了：

> ✅ **一个想法** — 想做什么内容？（教程/Vlog/科普/营销...）
> ✅ **一个工具** — 推荐从{}开始，免费版就够了
> ✅ **一个目标** — 不用大，第一条视频发布就算胜利

{}

## 🗺️ 5步入门路线图

### Step 1 | 选工具

{} 为什么适合新手？

{}

### Step 2 | 注册与探索

去 [{} 官网]({}) 注册免费账号，花15分钟把所有功能点一遍。不用记住全部——**先有个印象**。

### Step 3 | 做你的第一个作品

跟着这个checklist一步一步来：

{}

### Step 4 | 发布并获得反馈

不要追求完美！发出你的第一条作品，然后：

- 📊 观察观看数据（完播率、点赞率）
- 💬 看评论区的真实反馈
- 🔄 根据反馈迭代下一个作品

### Step 5 | 持续优化

每周至少创作1条视频。30天后回头看你第一条，你会惊讶自己的进步。

{}

## 🚫 新手常犯的3个错误

| 错误 | 正确做法 |
|:---|:---|
| ❌ 追求完美迟迟不发布 | ✅ 先完成再完美，60分就发 |
| ❌ 同时学太多工具 | ✅ 专注1个工具到精通 |
| ❌ 忽视内容只拼技术 | ✅ 技术是手段，内容是核心 |

{}

## 🎁 立刻行动

**今天就开始，不要等到「准备好」的那一天。**

👉 [从 {} 开始你的AI视频之旅]({})
👉 [📦 更多新手友好工具]({})

---

## 🎬 免费工具

免费使用 **AI Film Shot Planner** 规划你的镜头，创作更有条理。

👉 [AI Film Shot Planner 免费使用]({})

{}
""".format(
        article['emoji'], article['title_zh'],
        article['title_en'], date, article['type'],
        DIVIDER,
        HIGHLINE,
        tool['name'],
        HIGHLINE,
        tool['name'], pros_str,
        tool['name'], tool['url'],
        random.choice(checklists),
        HIGHLINE,
        DIVIDER,
        tool['name'], tool['url'], GUMROAD_URL,
        SHOT_PLANNER_URL,
        _footer()
    )
    return content


def _footer():
    return "\n---\n\n*📢 本文包含联盟营销链接。通过本链接购买产品我将获得一定比例的佣金，但不影响你的购买价格。感谢支持！*"


CATEGORY_GENERATORS = {
    "教程": _gen_tutorial,
    "对比": _gen_comparison,
    "技巧": _gen_tips,
    "趋势": _gen_trend,
    "入门指南": _gen_beginner_guide,
}


def save_article(content, slug):
    os.makedirs(BLOG_DIR, exist_ok=True)
    filepath = os.path.join(BLOG_DIR, "{}.md".format(slug))
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def generate_articles(force_all=False):
    available = [a for a in ARTICLE_TEMPLATES if a["slug"] not in PREVIOUS_SLUGS]
    if not available:
        print("\u26a0\ufe0f 所有模板都已生成过，重置后重新生成。")
        available = ARTICLE_TEMPLATES[:]
    if force_all:
        to_generate = available
    else:
        count = min(random.randint(3, 5), len(available))
        to_generate = random.sample(available, count)
    results = []
    for article in to_generate:
        gen_fn = CATEGORY_GENERATORS.get(article["type"], _gen_tutorial)
        content = gen_fn(article)
        path = save_article(content, article["slug"])
        results.append({"article": article, "path": path})
    return results


def generate_index_html(articles_with_paths=None):
    if articles_with_paths is None:
        existing = []
        for fname in os.listdir(BLOG_DIR):
            if fname.endswith(".md") and fname != "README.md":
                slug = fname.replace(".md", "")
                match = next((a for a in ARTICLE_TEMPLATES if a["slug"] == slug), None)
                if match:
                    existing.append({"article": match, "path": os.path.join(BLOG_DIR, fname)})
        articles_with_paths = existing

    today = datetime.now().strftime('%Y-%m-%d')

    cards_html = ""
    for item in articles_with_paths:
        a = item["article"]
        emoji = a.get("emoji", "\U0001f4c4")
        cat = a.get("type", "评测")
        slug = a["slug"]
        link = "./{}".format(slug)
        title = a["title_zh"]
        excerpt = "{} {} -- 一篇关于AI影视创作的{}文章，帮助你更好地使用AI工具。".format(emoji, a['title_en'], cat)

        cards_html += """
    <a href="{link}" class="card card-{cat}">
      <div class="card-badge">{emoji} {cat}</div>
      <h3 class="card-title">{title}</h3>
      <p class="card-excerpt">{excerpt}</p>
      <div class="card-footer">
        <span class="card-date">📅 {today}</span>
        <span class="card-read">📖 5-10分钟</span>
      </div>
    </a>""".format(link=link, cat=cat, emoji=emoji, title=title, excerpt=excerpt, today=today)

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎬 AI影视工具博客 -- 教程·评测·技巧·趋势</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg: #0a0a0b;
      --surface: #141416;
      --surface-2: #1c1c1f;
      --border: #2a2a2e;
      --text: #f4f4f5;
      --text-2: #a1a1aa;
      --text-3: #71717a;
      --accent: #6366f1;
      --accent-hover: #818cf8;
      --indigo: #6366f1;
      --emerald: #10b981;
      --amber: #f59e0b;
      --rose: #f43f5e;
      --cyan: #06b6d4;
      --radius: 16px;
    }
    html { font-size: 16px; scroll-behavior: smooth; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
    }
    a { color: var(--accent); text-decoration: none; }
    a:hover { color: var(--accent-hover); }
    .container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
    .hero {
      padding: 60px 0 40px;
      text-align: center;
      border-bottom: 1px solid var(--border);
      margin-bottom: 48px;
    }
    .hero h1 {
      font-size: 2.6rem;
      font-weight: 800;
      background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 12px;
    }
    .hero p {
      font-size: 1.1rem;
      color: var(--text-2);
      max-width: 600px;
      margin: 0 auto;
    }
    .hero-stats {
      display: flex;
      justify-content: center;
      gap: 32px;
      margin-top: 20px;
      color: var(--text-3);
      font-size: 0.9rem;
    }
    .hero-stats span { display: flex; align-items: center; gap: 6px; }
    .tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: center;
      margin-bottom: 36px;
    }
    .tab {
      padding: 8px 20px;
      border: 1px solid var(--border);
      border-radius: 999px;
      font-size: 0.85rem;
      color: var(--text-2);
      cursor: pointer;
      transition: all 0.2s;
      background: transparent;
    }
    .tab:hover { border-color: var(--accent); color: var(--text); }
    .tab.active { background: var(--accent); color: white; border-color: var(--accent); }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
      padding-bottom: 60px;
    }
    .card {
      display: flex;
      flex-direction: column;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }
    .card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 3px;
      background: var(--accent);
      opacity: 0;
      transition: opacity 0.25s;
    }
    .card:hover {
      transform: translateY(-4px);
      border-color: var(--accent);
      box-shadow: 0 8px 32px rgba(99,102,241,0.12);
    }
    .card:hover::before { opacity: 1; }
    .card-教程::before { background: var(--indigo); }
    .card-对比::before { background: var(--amber); }
    .card-技巧::before { background: var(--emerald); }
    .card-趋势::before { background: var(--rose); }
    .card-入门指南::before { background: var(--cyan); }
    .card-badge {
      display: inline-block;
      font-size: 0.78rem;
      padding: 4px 12px;
      border-radius: 999px;
      background: rgba(99,102,241,0.1);
      color: var(--accent);
      margin-bottom: 14px;
      align-self: flex-start;
    }
    .card-教程 .card-badge { background: rgba(99,102,241,0.1); color: var(--indigo); }
    .card-对比 .card-badge { background: rgba(245,158,11,0.1); color: var(--amber); }
    .card-技巧 .card-badge { background: rgba(16,185,129,0.1); color: var(--emerald); }
    .card-趋势 .card-badge { background: rgba(244,63,94,0.1); color: var(--rose); }
    .card-入门指南 .card-badge { background: rgba(6,182,212,0.1); color: var(--cyan); }
    .card-title {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 10px;
      line-height: 1.4;
      color: var(--text);
    }
    .card-excerpt {
      font-size: 0.88rem;
      color: var(--text-2);
      line-height: 1.6;
      flex-grow: 1;
      margin-bottom: 16px;
    }
    .card-footer {
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      color: var(--text-3);
      border-top: 1px solid var(--border);
      padding-top: 14px;
    }
    .site-footer {
      text-align: center;
      padding: 32px 0 48px;
      border-top: 1px solid var(--border);
      color: var(--text-3);
      font-size: 0.85rem;
    }
    .site-footer a { margin: 0 10px; }
    @media (max-width: 640px) {
      .hero h1 { font-size: 1.8rem; }
      .grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="hero">
      <h1>🎬 AI影视工具博客</h1>
      <p>教程 · 评测 · 技巧 · 趋势 · 入门指南 -- 帮你用好AI，创作更好的影视内容</p>
      <div class="hero-stats">
        <span>📚 共 __COUNT__ 篇文章</span>
        <span>📅 更新于 __TODAY__</span>
        <span>🏷️ 教程 · 对比 · 技巧 · 趋势 · 入门指南</span>
      </div>
    </header>
    <div class="tabs" id="tabs">
      <button class="tab active" data-filter="all">🏠 全部</button>
      <button class="tab" data-filter="教程">🎓 教程</button>
      <button class="tab" data-filter="对比">⚔️ 对比</button>
      <button class="tab" data-filter="技巧">💡 技巧</button>
      <button class="tab" data-filter="趋势">📈 趋势</button>
      <button class="tab" data-filter="入门指南">🚀 入门</button>
    </div>
    <div class="grid" id="grid">
      __CARDS__
    </div>
    <footer class="site-footer">
      <p>🎬 <a href="https://zhanggengxi.github.io/ai-film-tools/">AI Film Shot Planner</a> 免费使用</p>
      <p><a href="https://gengxi.gumroad.com">📦 Gumroad 商店</a> &middot; <a href="https://afdian.net/a/xiaosimao">⚡ 爱发电支持</a></p>
      <p style="margin-top:12px; font-size:0.78rem;">📢 部分文章包含联盟营销链接</p>
    </footer>
  </div>
  <script>
    document.getElementById('tabs').addEventListener('click', function(e) {
      var btn = e.target.closest('.tab');
      if (!btn) return;
      document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
      btn.classList.add('active');
      var filter = btn.dataset.filter;
      document.querySelectorAll('.card').forEach(function(card) {
        if (filter === 'all') {
          card.style.display = '';
        } else {
          card.style.display = card.classList.contains('card-' + filter) ? '' : 'none';
        }
      });
    });
  </script>
</body>
</html>"""
    html = html.replace("__CARDS__", cards_html)
    html = html.replace("__COUNT__", str(len(articles_with_paths)))
    html = html.replace("__TODAY__", today)

    index_path = os.path.join(BLOG_DIR, "index.html")
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    return index_path


def main():
    import sys
    force_all = "--all" in sys.argv

    print("=" * 50)
    print("  \U0001f3ac AI 联盟营销内容生成器 v2.0")
    print("=" * 50)

    if force_all:
        print("  \U0001f504 模式：生成全部文章")
    else:
        print("  \U0001f504 模式：每周随机轮换")

    results = generate_articles(force_all=force_all)
    print("\n  \u2705 生成了 {} 篇文章：".format(len(results)))
    for r in results:
        a = r["article"]
        print("     {} [{}] {}".format(a['emoji'], a['type'], a['title_zh']))
        print("        -> {}".format(r['path']))

    index_path = generate_index_html(results)
    print("\n  \U0001f4c4 博客首页已更新 -> {}".format(index_path))

    print("\n" + "=" * 50)
    print("  \U0001f4ca 总计 {} 篇新文章 + 1 个首页".format(len(results)))
    print("=" * 50)


if __name__ == "__main__":
    main()
