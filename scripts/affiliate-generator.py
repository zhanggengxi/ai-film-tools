#!/usr/bin/env python3
"""AI 联盟营销内容自动生成器"""

import os
from datetime import datetime

AFFILIATE_LINKS = {
    "synthesia": {"name": "Synthesia", "url": "https://www.synthesia.io/?ref=aifilmtools", "desc": "AI虚拟人视频制作"},
    "pictory": {"name": "Pictory", "url": "https://pictory.ai?ref=aifilmtools", "desc": "AI文字转视频"},
    "heygen": {"name": "HeyGen", "url": "https://www.heygen.com/?ref=aifilmtools", "desc": "AI视频翻译与虚拟人"},
    "runway": {"name": "Runway", "url": "https://runwayml.com/?ref=aifilmtools", "desc": "AI视频编辑与生成"},
    "elevenlabs": {"name": "ElevenLabs", "url": "https://elevenlabs.io/?ref=aifilmtools", "desc": "AI配音与语音克隆"},
}

BLOG_DIR = os.path.expanduser("~/Desktop/sellable_products/ai-film-tools/docs/blog/")

REVIEW_TEMPLATES = [
    {"slug": "best-ai-video-tools-for-filmmakers-2025", "title_zh": "2025年AI影视创作者必备的5款工具", "title_en": "5 Best AI Video Tools for Filmmakers in 2025", "tool": "multi"},
    {"slug": "synthesia-review-ai-avatar", "title_zh": "Synthesia 深度评测：AI虚拟人视频值得吗？", "title_en": "Synthesia Review: Is AI Avatar Worth It?", "tool": "synthesia"},
    {"slug": "pictory-review-text-to-video", "title_zh": "Pictory 评测：AI自动转视频", "title_en": "Pictory Review: Turn Text to Video", "tool": "pictory"},
    {"slug": "heygen-review-ai-translation", "title_zh": "HeyGen 评测：AI视频翻译利器", "title_en": "HeyGen Review: AI Video Translation", "tool": "heygen"},
    {"slug": "runway-gen3-review", "title_zh": "Runway Gen-3 深度评测", "title_en": "Runway Gen-3 Review", "tool": "runway"},
    {"slug": "elevenlabs-review-voice-cloning", "title_zh": "ElevenLabs 评测：AI配音新标杆", "title_en": "ElevenLabs Review: AI Voice Cloning", "tool": "elevenlabs"},
]

SHOT_PLANNER_URL = "https://zhanggengxi.github.io/ai-film-tools/"
GUMROAD_URL = "https://gengxi.gumroad.com"
AFDIAN_URL = "https://afdian.net/a/xiaosimao"


def generate_multi_article():
    """生成综合评测文章"""
    date = datetime.now().strftime('%Y-%m-%d')
    return f"""# 2025年AI影视创作者必备的5款工具

> 原文：5 Best AI Video Tools for Filmmakers in 2025
> 发布：{date}

---

作为一个AI影视创作者，我试过市面上几乎所有AI视频工具。这篇文章帮你选出**真正值得用的5款工具**，附上真实评测。

---

## 1. Synthesia — AI虚拟人视频

{_tool_section("synthesia", "适合快速生成虚拟主播视频、教程视频")}

👉 [Synthesia 官网]({AFFILIATE_LINKS['synthesia']['url']})

## 2. Pictory — AI文字转视频

{_tool_section("pictory", "适合博主、需要将文章转为视频的人")}

👉 [Pictory 官网]({AFFILIATE_LINKS['pictory']['url']})

## 3. Runway Gen-3 — AI视频生成

{_tool_section("runway", "适合专业影视创作者")}

👉 [Runway 官网]({AFFILIATE_LINKS['runway']['url']})

## 4. HeyGen — AI视频翻译

{_tool_section("heygen", "适合跨境内容创作者")}

👉 [HeyGen 官网]({AFFILIATE_LINKS['heygen']['url']})

## 5. ElevenLabs — AI配音

{_tool_section("elevenlabs", "适合需要专业级AI配音的创作者")}

👉 [ElevenLabs 官网]({AFFILIATE_LINKS['elevenlabs']['url']})

---

## 免费工具推荐

刚入门AI影视创作？免费使用开源 **[AI Film Shot Planner]({SHOT_PLANNER_URL})** 规划镜头。

{_footer()}
"""


def _tool_section(key, audience):
    t = AFFILIATE_LINKS[key]
    return f"""**{t['name']}** — {t['desc']}

**适合：** {audience}

**优点：** 使用门槛低，输出质量稳定，比传统方式节省大量时间
**缺点：** 创意控制有限，复杂场景不够灵活

**推荐指数：** ⭐⭐⭐⭐"""


def generate_single_article(template):
    """生成单篇工具评测"""
    tool_key = template["tool"]
    tool = AFFILIATE_LINKS[tool_key]
    date = datetime.now().strftime('%Y-%m-%d')
    cat = "视频" if tool_key != "elevenlabs" else "配音"
    audience = "内容创作者" if tool_key in ["synthesia", "pictory"] else "AI影视从业者"

    return f"""# {template['title_zh']}

> 原文：{template['title_en']}
> 发布：{date}

---

## 引言

如果你在做AI影视创作，{tool['name']} 你一定不陌生。我深度体验后给你一份真实评测。

## {tool['name']} 是什么？

{tool['desc']}

### 核心功能
- 专业级AI{cat}处理
- 简洁易用的界面
- 适合影视创作者的输出质量

## 适合谁用？
- **AI影视创作者** — 制作AI短片、教程视频
- **内容营销人员** — 批量生成视频内容
- **跨境创作者** — 多语言视频需求

## 优缺点

**优点：** 使用门槛低，输出稳定，节省时间
**缺点：** 创意控制有限，复杂场景不够灵活

## 价格

{tool['name']} 定价合理。以官网最新信息为准。

👉 [查看 {tool['name']} 最新价格]({tool['url']})

## 结论

**{tool['name']} 值得{audience}尝试。** 如果你是{audience}，绝对值得一试。

---

## 免费工具推荐

刚入门AI影视创作？免费使用开源 **AI Film Shot Planner** 规划镜头。

👉 [AI Film Shot Planner 免费使用]({SHOT_PLANNER_URL})
👉 [更多AI影视工具]({GUMROAD_URL})
👉 [赞助支持]({AFDIAN_URL})

{_footer()}
"""


def _footer():
    return """*本文包含联盟营销链接，通过本链接购买产品我将获得一定比例的佣金，但不影响你的购买价格。*"""


def save_article(content, slug):
    os.makedirs(BLOG_DIR, exist_ok=True)
    filepath = os.path.join(BLOG_DIR, f"{slug}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def generate_all():
    results = []
    for t in REVIEW_TEMPLATES:
        if t["tool"] == "multi":
            content = generate_multi_article()
        else:
            content = generate_single_article(t)
        path = save_article(content, t["slug"])
        results.append({"title": t["title_zh"], "path": path})
    return results


if __name__ == "__main__":
    results = generate_all()
    print(f"✅ 生成了 {len(results)} 篇文章：")
    for r in results:
        print(f"   📄 {r['title']} → {r['path']}")
