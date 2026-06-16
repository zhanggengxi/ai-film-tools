#!/usr/bin/env python3
"""
🎬 AI Film Tools — Daily Content Factory
==========================================
多模型AI内容工厂 · 每日自动生成5-10篇中英双语文章并发布到 GitHub Pages

特性：
  - 支持 OpenAI / Anthropic / Google / DeepSeek / 任意兼容 OpenAI 的 API
  - 8 种文章类型，40+ 轮换主题（每周自动轮换）
  - AI 生成中文 → 自动翻译英文 → 生成中英双语 Markdown
  - 自动更新博客首页并 Git 提交推送

环境变量配置（见 .env.example 或直接 export）：
  CONTENT_FACTORY_MODEL       openi/anthropic/google/deepseek/openai_compatible
  OPENAI_API_KEY              ...
  ANTHROPIC_API_KEY           ...
  GOOGLE_API_KEY              ...
  DEEPSEEK_API_KEY            ...
  OPENAI_COMPATIBLE_API_KEY   ...
  OPENAI_COMPATIBLE_BASE_URL  https://...
  OPENAI_COMPATIBLE_MODEL     gpt-4o-mini
  GIT_USER_NAME               Your Name
  GIT_USER_EMAIL              your@email.com
  BLOG_REPO_PATH              默认 ~/Desktop/sellable_products/ai-film-tools

用法：
  python daily-content-factory.py              # 生成 5-10 篇
  python daily-content-factory.py --count 3   # 指定篇数
  python daily-content-factory.py --dry-run   # 仅打印主题，不生成
  python daily-content-factory.py --no-push   # 生成+提交但不推送
"""

import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════

VERSION = "1.0.0"
SCRIPT_DIR = Path(__file__).parent.resolve()
DEFAULT_BLOG_REPO = SCRIPT_DIR.parent / "docs" / "blog"
DEFAULT_REPO_ROOT = SCRIPT_DIR.parent

# 文章类型及对应的 Emoji
ARTICLE_TYPES = [
    "教程",      # tutorial
    "对比",      # comparison
    "技巧",      # tips
    "趋势",      # trends
    "新闻",      # news
    "案例",      # case_study
    "工具推荐",  # tool_recommendation
    "行业分析",  # industry_analysis
]

TYPE_EMOJI = {
    "教程": "🎓",
    "对比": "⚔️",
    "技巧": "💡",
    "趋势": "📈",
    "新闻": "📰",
    "案例": "📋",
    "工具推荐": "🛠️",
    "行业分析": "🔬",
}

# ── 40+ 轮换主题（每周 Hash 决定子集） ──
TOPIC_POOL = [
    # ── 教程类 ──
    ("教程", "sora-text-to-video-beginners", "Sora文生视频新手教程：用文字创造电影"),
    ("教程", "runway-gen4-advanced-techniques", "Runway Gen-4 高级技巧：从入门到精通"),
    ("教程", "pika-labs-tutorial-storytelling", "Pika Labs 讲故事教程：AI动画短片创作"),
    ("教程", "kaiber-ai-music-video-guide", "Kaiber AI 音乐视频制作指南"),
    ("教程", "hedra-ai-character-animation", "Hedra AI 角色动画入门：让角色活起来"),
    ("教程", "luma-dream-machine-guide", "Luma Dream Machine 3D生成完全教程"),
    ("教程", "veo-google-deepmind-video-gen", "Google Veo 视频生成：DeepMind最强模型实战"),
    ("教程", "minimax-video-hailuo-guide", "MiniMax 视频生成全面指南"),
    # ── 对比类 ──
    ("对比", "sora-vs-runway-vs-pika-2026", "Sora vs Runway vs Pika：2026三大文生视频工具横评"),
    ("对比", "midjourney-vs-dall-e-vs-stable", "Midjourney vs DALL·E vs Stable Diffusion影视应用对比"),
    ("对比", "elevenlabs-vs-fish-audio-vs-playht", "ElevenLabs vs Fish Audio vs Play.ht 配音工具对比"),
    ("对比", "capcut-vs-premiere-vs-davinchi-ai", "剪映 vs Premiere vs DaVinci Resolve：AI剪辑功能对比"),
    ("对比", "heygen-vs-synthesia-vs-d-id", "HeyGen vs Synthesia vs D-ID 虚拟人平台深度对比"),
    ("对比", "kling-vs-vidu-chinese-video-tools", "可灵 vs Vidu：国产AI视频工具全面对比"),
    ("对比", "sunshine-vs-mochi-open-source-video", "Sunshine vs Mochi：开源AI视频模型对比"),
    # ── 技巧类 ──
    ("技巧", "ai-prompt-engineering-video", "AI视频提示词工程：写出完美Prompt的10个技巧"),
    ("技巧", "text-to-video-quality-hacks", "文生视频画质提升秘籍：告别AI感"),
    ("技巧", "ai-video-color-grading-tips", "AI视频调色技巧：让画面拥有电影质感"),
    ("技巧", "storyboard-ai-tools-workflow", "AI分镜工作流：从文字到分镜图只需5分钟"),
    ("技巧", "ai-video-seo-optimization", "AI视频SEO优化：让更多人在YouTube找到你的内容"),
    ("技巧", "multi-camera-ai-editing", "多机位AI剪辑技巧：自动选择最佳镜头"),
    ("技巧", "ai-video-watermark-removal", "AI去水印与视频修复：专业级修复技巧"),
    # ── 趋势类 ──
    ("趋势", "ai-film-industry-2027-predictions", "2027年AI影视行业十大预测"),
    ("趋势", "real-time-ai-video-generation", "实时AI视频生成技术：实时交互重塑内容创作"),
    ("趋势", "ai-generated-movies-first-feature", "首部AI长片电影深度解析：技术突破与艺术争议"),
    ("趋势", "ai-actor-digital-human-rights", "AI数字演员与肖像权：影视行业的法律新挑战"),
    ("趋势", "open-source-ai-video-models-2026", "开源AI视频模型2026全景图：社区驱动的革命"),
    ("趋势", "ai-video-advertising-revolution", "AI视频广告革命：个性化广告从概念到现实"),
    ("趋势", "hollywood-ai-strike-aftermath", "好莱坞AI罢工一周年：行业格局如何改变"),
    # ── 新闻类 ──
    ("新闻", "openai-sora-update-this-week", "OpenAI Sora 最新更新速览"),
    ("新闻", "runway-new-feature-release", "Runway 本月新功能发布汇总"),
    ("新闻", "google-deepmind-veo-news", "Google DeepMind Veo 最新进展"),
    ("新闻", "ai-video-funding-news", "AI视频创企融资动态：资本流向何方"),
    ("新闻", "new-ai-video-tool-launch", "本周新上线的AI视频工具盘点"),
    ("新闻", "china-ai-video-regulation", "中国AI视频生成监管政策最新动态"),
    # ── 案例类 ──
    ("案例", "ai-short-film-festival-winner", "AI短片电影节获奖作品深度解析"),
    ("案例", "brand-ai-video-campaign-case", "品牌AI视频营销案例：Nike/可口可乐怎么用AI？"),
    ("案例", "indie-filmmaker-ai-workflow", "独立电影人如何用AI工具将预算降低80%？"),
    ("案例", "youtuber-ai-content-pipeline", "顶尖YouTuber的AI内容生产流水线揭秘"),
    ("案例", "education-ai-video-success", "教育领域AI视频成功案例：在线课程制作革命"),
    ("案例", "ecommerce-ai-product-video", "电商AI商品视频案例：转化率提升300%的秘密"),
    # ── 工具推荐类 ──
    ("工具推荐", "best-ai-video-tools-2026-june", "2026年6月AI视频工具推荐TOP 20"),
    ("工具推荐", "free-ai-film-tools-no-watermark", "无水印免费AI影视工具合集（持续更新）"),
    ("工具推荐", "ai-video-editing-plugins-premiere", "Premiere Pro最佳AI插件推荐"),
    ("工具推荐", "ai-music-generator-film-scoring", "AI电影配乐工具推荐：免费与付费精选"),
    ("工具推荐", "ai-subtitle-translation-tools", "AI字幕翻译工具推荐：一键多语言覆盖"),
    ("工具推荐", "open-source-ai-video-tools", "开源AI视频工具生态：最佳免费替代方案"),
    # ── 行业分析类 ──
    ("行业分析", "ai-video-market-size-2026", "2026年AI视频市场规模深度分析"),
    ("行业分析", "china-vs-us-ai-video-race", "中美AI视频技术竞赛：谁在领跑？"),
    ("行业分析", "ai-film-jobs-future", "AI将取代哪些影视岗位？未来5年职业趋势"),
    ("行业分析", "ai-video-cost-analysis-2026", "AI视频制作成本深度分析：比传统方式省多少？"),
    ("行业分析", "generative-ai-film-patents", "生成式AI影视专利地图：谁在布局？"),
    ("行业分析", "ai-video-ethics-responsibility", "AI视频伦理问题：深度伪造与内容责任"),
]

assert len(TOPIC_POOL) >= 40, f"Topic pool too small: {len(TOPIC_POOL)}"

# ── 已用 Slugs（防止重复） ──
PREVIOUS_SLUG_FILE = SCRIPT_DIR / ".daily_content_factory_slugs.json"

# ═══════════════════════════════════════════════════════════
# 配置加载
# ═══════════════════════════════════════════════════════════

class Config:
    """从环境变量加载所有配置"""

    def __init__(self):
        self.model_type = os.environ.get("CONTENT_FACTORY_MODEL", "openai").strip().lower()
        self.blog_repo_path = Path(
            os.environ.get("BLOG_REPO_PATH", str(DEFAULT_REPO_ROOT))
        )
        self.blog_dir = self.blog_repo_path / "docs" / "blog"

        # API Keys
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY", "")
        self.deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        self.openai_compatible_api_key = os.environ.get("OPENAI_COMPATIBLE_API_KEY", "")
        self.openai_compatible_base_url = os.environ.get(
            "OPENAI_COMPATIBLE_BASE_URL", ""
        )
        self.openai_compatible_model = os.environ.get(
            "OPENAI_COMPATIBLE_MODEL", "gpt-4o-mini"
        )

        # Git
        self.git_user_name = os.environ.get("GIT_USER_NAME", "AI Content Factory")
        self.git_user_email = os.environ.get(
            "GIT_USER_EMAIL", "content-factory@ai-film-tools.local"
        )

        # Generation
        self.count = int(os.environ.get("CONTENT_COUNT", "0"))  # 0 = auto 5-10
        self.temperature = float(os.environ.get("CONTENT_TEMPERATURE", "0.8"))
        self.max_tokens = int(os.environ.get("CONTENT_MAX_TOKENS", "2048"))

        self.validate()

    def validate(self):
        if not self.openai_api_key and self.model_type == "openai":
            print("⚠️  OPENAI_API_KEY 未设置，使用模拟生成模式（demo）")
        if not self.anthropic_api_key and self.model_type == "anthropic":
            print("⚠️  ANTHROPIC_API_KEY 未设置，使用模拟生成模式（demo）")


config = Config()


# ═══════════════════════════════════════════════════════════
# 模型调用层
# ═══════════════════════════════════════════════════════════

def _call_openai(system_prompt, user_prompt, model="gpt-4o"):
    """调用 OpenAI API"""
    import openai

    client = openai.OpenAI(api_key=config.openai_api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    return resp.choices[0].message.content


def _call_anthropic(system_prompt, user_prompt, model="claude-sonnet-4-20250514"):
    """调用 Anthropic Claude API"""
    from anthropic import Anthropic

    client = Anthropic(api_key=config.anthropic_api_key)
    resp = client.messages.create(
        model=model,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=config.max_tokens,
        temperature=config.temperature,
    )
    return resp.content[0].text


def _call_google(system_prompt, user_prompt, model="gemini-2.0-flash"):
    """调用 Google Gemini API"""
    import google.generativeai as genai

    genai.configure(api_key=config.google_api_key)
    model_obj = genai.GenerativeModel(
        model,
        system_instruction=system_prompt,
        generation_config={"temperature": config.temperature, "max_output_tokens": config.max_tokens},
    )
    resp = model_obj.generate_content(user_prompt)
    return resp.text


def _call_deepseek(system_prompt, user_prompt, model="deepseek-chat"):
    """调用 DeepSeek API（兼容 OpenAI SDK）"""
    import openai

    client = openai.OpenAI(
        api_key=config.deepseek_api_key,
        base_url="https://api.deepseek.com/v1",
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    return resp.choices[0].message.content


def _call_openai_compatible(system_prompt, user_prompt):
    """调用任意兼容 OpenAI 格式的 API"""
    import openai

    client = openai.OpenAI(
        api_key=config.openai_compatible_api_key,
        base_url=config.openai_compatible_base_url,
    )
    resp = client.chat.completions.create(
        model=config.openai_compatible_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    return resp.choices[0].message.content


ROUTER = {
    "openai": lambda s, u: _call_openai(s, u),
    "anthropic": lambda s, u: _call_anthropic(s, u),
    "google": lambda s, u: _call_google(s, u),
    "deepseek": lambda s, u: _call_deepseek(s, u),
    "openai_compatible": lambda s, u: _call_openai_compatible(s, u),
}


def llm_chat(system_prompt, user_prompt):
    """统一的 LLM 调用入口"""
    fn = ROUTER.get(config.model_type)
    if fn is None:
        supported = ", ".join(ROUTER.keys())
        raise ValueError(
            f"不支持的模型类型: {config.model_type}。支持: {supported}"
        )
    try:
        return fn(system_prompt, user_prompt)
    except Exception as e:
        print(f"  ⚠️  API 调用失败: {e}")
        print(f"  ⚠️  降级为模拟生成模式")
        return None


# ═══════════════════════════════════════════════════════════
# 文章内容生成
# ═══════════════════════════════════════════════════════════

def _build_zh_system_prompt(article_type, title_zh):
    """构建中文文章生成系统提示"""
    return f"""你是一位专业的AI影视工具中文内容创作者。你擅长撰写深入、实用、有观点的文章。

写作要求：
- 文章类型：{article_type}
- 标题：{title_zh}
- 使用中文简体写作
- 语气专业但不枯燥，有个人见解
- 篇幅：800-1500字（markdown格式）
- 使用适当的emoji点缀每个小节标题
- 结构清晰，使用 ## 和 ### 分级标题
- 如果有对比、数字、列表，使用表格或列表格式
- 体现真实使用经验，不要笼统的套话
- 结尾要有行动指引（CTA）

必须严格遵守的格式：
1. 第一行是文章标题： # {{emoji}} {{title_zh}}
2. 文章用中文写作
3. 包含实际数据、具体工具名称、版本号
4. 至少包含1个表格
5. 包含"🎁 免费资源"板块推荐 AI Film Shot Planner"""


def _build_en_system_prompt(article_type, title_en):
    """构建英文文章生成系统提示"""
    return f"""You are a professional AI filmmaking tools content creator writing in English.

Writing requirements:
- Article type: {article_type}
- Title: {title_en}
- Professional yet engaging tone
- Length: 600-1200 words in markdown
- Use emoji sparingly but effectively in section headers
- Clear structure with ## and ### headings
- Include specific data, tool versions, real-world examples
- At least 1 comparison table or data table
- End with a clear CTA

Strict format:
1. First line: # {{emoji}} {{title_en}}
2. Include a "🎁 Free Resource" section recommending AI Film Shot Planner
3. Use markdown formatting"""


def _build_translate_system_prompt():
    return """You are a professional translator specializing in AI/tech content translation (Chinese → English).

Requirements:
- Translate the FULL article from Chinese to natural, fluent English
- Preserve markdown formatting, emoji, links, and all structure
- Do NOT add or remove any content sections
- Keep technical terms accurate
- Adapt culturally-specific references when needed
- Output ONLY the translated English article, no explanations
- First line must be: # {emoji} {title_en}"""


def generate_article_zh(article_type, title_zh):
    """生成中文文章"""
    print(f"  📝 正在生成中文文章: {title_zh}")
    sys_prompt = _build_zh_system_prompt(article_type, title_zh)
    user_prompt = f"请撰写一篇关于「{title_zh}」的{article_type}类型文章，篇幅800-1500字。"
    content = llm_chat(sys_prompt, user_prompt)
    if content is None:
        content = _demo_article_zh(article_type, title_zh)
    return content.strip()


def translate_to_en(zh_content, title_en):
    """将中文文章翻译为英文"""
    print(f"  🌐 正在翻译为英文: {title_en}")
    sys_prompt = _build_translate_system_prompt()
    user_prompt = f"Translate this Chinese article to English. English title: {title_en}\n\n---\n\n{zh_content}"
    content = llm_chat(sys_prompt, user_prompt)
    if content is None:
        content = _demo_article_en(zh_content, title_en)
    return content.strip()


def _demo_article_zh(article_type, title_zh):
    """API不可用时的演示文章生成"""
    tools = [
        "Sora (OpenAI)", "Runway Gen-4", "Pika Labs 2.0", "HeyGen",
        "Synthesia", "ElevenLabs", "Kaiber", "Luma Dream Machine",
        "Google Veo", "MiniMax Hailuo", "可灵 (Kling)", "Vidu",
    ]
    date_str = datetime.now().strftime("%Y-%m-%d")
    emoji = TYPE_EMOJI.get(article_type, "📄")

    paragraphs = [
        f"在AI技术日新月异的今天，{article_type}类内容越来越受到创作者的关注。本文将从实操角度出发，深入探讨这一主题。",
        f"根据最新行业数据，2026年AI视频工具市场规模已达到{random.randint(30, 80)}亿美元，年增长率超过{random.randint(40, 90)}%。{random.choice(tools)}等主流平台相继发布了重大更新。",
        f"## 📊 核心要点分析",
        f"| 维度 | 详情 |\n|:---|:---|\n| 📅 发布时间 | {date_str} |\n| 🏷️ 分类 | {article_type} |\n| 🛠️ 涉及工具 | {random.choice(tools)}、{random.choice(tools)} |\n| ⏱️ 预计阅读 | {random.randint(5, 12)}分钟 |",
        f"## 💡 深入分析",
        f"在具体实践中，我们发现以下几个关键点值得每位创作者关注：",
        f"**第一，质量与效率的平衡。** 当前AI视频生成工具在{random.randint(4, 9)}K分辨率下已经能够产出令人满意的结果，但生成时间仍是瓶颈。{random.choice(tools)}的最新版本将生成速度提升了{random.randint(2, 5)}倍。",
        f"**第二，工作流程的整合。** 将多个AI工具串联成高效pipeline，是提升创作效率的关键。推荐的工作流为：剧本→分镜→视频生成→配音→剪辑→发布。",
        f"**第三，成本考量。** 相比传统视频制作，AI视频制作可以降低{random.randint(50, 90)}%的成本，同时将制作周期从周级缩短到小时级。",
        f"## 📝 实操建议",
        f"1. **选择合适的工具** — 根据自己的需求选择最适合的工具，不要盲目追求功能最多的",
        f"2. **持续学习** — AI工具更新极快，建议每周花{random.randint(1, 3)}小时了解最新动态",
        f"3. **内容为王** — 技术只是手段，优质的内容才是核心竞争力的来源",
        f"4. **多平台分发** — 将AI视频适配不同平台格式，最大化内容价值",
        f"## 🔮 展望",
        f"随着技术的持续进步，我们可以预见AI影视工具将变得更加智能、易用。{random.randint(1, 3)}年内，AI生成的视频内容将在质量上与传统视频难以区分。对于创作者来说，现在就是最好的入场时机。",
        f"## 🎁 免费资源",
        f"刚入门AI影视创作？免费使用 **🎬 AI Film Shot Planner** 规划镜头，让你的创作更有条理。\n\n👉 [AI Film Shot Planner 免费使用](https://zhanggengxi.github.io/ai-film-tools/)",
    ]

    content = f"# {emoji} {title_zh}\n\n"
    content += f"> 📍 **原文：** {title_zh}\n"
    content += f"> 📅 **发布：** {date_str}\n"
    content += f"> 🏷️ **分类：** {article_type} | **预计阅读：** {random.randint(5, 12)}分钟\n\n"
    content += "─" * 40 + "\n\n"
    for p in paragraphs:
        content += p + "\n\n"
    content += "─" * 40 + "\n\n"
    content += "*📢 本文由 AI Content Factory 自动生成。*"
    return content


def _demo_article_en(zh_content, title_en):
    """API不可用时的演示英文翻译"""
    emoji_match = re.search(r'^#\s*(\S+)', zh_content)
    emoji = emoji_match.group(1) if emoji_match else "📄"

    # 简单提取中文内容进行"翻译" （demo模式下模拟翻译）
    lines = zh_content.split("\n")
    en_lines = []
    for line in lines:
        if line.startswith("# ") and emoji in line:
            en_lines.append(f"# {emoji} {title_en}")
        elif "原文" in line:
            en_lines.append(f"> 📍 **Original:** {title_en}")
        elif "发布" in line:
            en_lines.append(line.replace("发布", "Published").replace("分类", "Category"))
        elif "预计阅读" in line:
            en_lines.append(line.replace("预计阅读", "Read time"))
        else:
            en_lines.append(line)

    en_content = "\n".join(en_lines)
    en_content += "\n\n---\n\n*📢 This article was auto-generated by AI Content Factory.*"
    return en_content


# ═══════════════════════════════════════════════════════════
# 主题选择（每周轮换）
# ═══════════════════════════════════════════════════════════

def get_weekly_topics(count=0):
    """
    基于当前周的 hash 值，从主题池中选择一组主题。
    保证每周轮换不同的子集，且不会在短时间内重复。
    """
    today = datetime.now()
    # 使用 ISO 周年作为种子，每周自动轮换
    week_seed = today.isocalendar()[0] * 100 + today.isocalendar()[1]
    rng = random.Random(week_seed)

    # 加载已使用 slugs
    used_slugs = _load_used_slugs()

    # 过滤掉已使用的
    available = [t for t in TOPIC_POOL if t[1] not in used_slugs]

    # 如果可用不足，重置
    if len(available) < 5:
        print("  🔄 可用主题不足，重置已使用记录")
        available = TOPIC_POOL[:]
        used_slugs.clear()
        _save_used_slugs(used_slugs)

    # 确定本次生成数量
    if count <= 0:
        count = rng.randint(5, 10)
    count = min(count, len(available))

    # 每个类型至少选一篇（如果可能）
    selected = []
    types_needed = list(ARTICLE_TYPES)
    rng.shuffle(types_needed)

    for atype in types_needed:
        candidates = [t for t in available if t[0] == atype and t not in selected]
        if candidates and len(selected) < count:
            chosen = rng.choice(candidates)
            selected.append(chosen)

    # 补全剩余数量
    remaining = [t for t in available if t not in selected]
    rng.shuffle(remaining)
    while len(selected) < count and remaining:
        selected.append(remaining.pop(0))

    rng.shuffle(selected)
    return selected


def _load_used_slugs():
    """加载已使用的 slugs"""
    if PREVIOUS_SLUG_FILE.exists():
        try:
            data = json.loads(PREVIOUS_SLUG_FILE.read_text())
            return set(data.get("slugs", []))
        except (json.JSONDecodeError, KeyError):
            return set()
    return set()


def _save_used_slugs(slugs_set):
    """保存已使用的 slugs"""
    PREVIOUS_SLUG_FILE.parent.mkdir(parents=True, exist_ok=True)
    PREVIOUS_SLUG_FILE.write_text(
        json.dumps({"slugs": list(slugs_set), "updated": datetime.now().isoformat()},
                   ensure_ascii=False, indent=2)
    )


# ═══════════════════════════════════════════════════════════
# 文章保存
# ═══════════════════════════════════════════════════════════

def build_bilingual_markdown(slug, title_zh, title_en, article_type, zh_content, en_content):
    """
    构建双语 Markdown。
    格式：Frontmatter → 中文全文 → English Version 标题 → 英文全文
    """
    emoji = TYPE_EMOJI.get(article_type, "📄")
    date_str = datetime.now().strftime("%Y-%m-%d")

    # 提取中文标题中的emoji
    zh_emoji_match = re.search(r'^#\s*(\S+)', zh_content)
    first_line_emoji = zh_emoji_match.group(1) if zh_emoji_match else emoji

    # 提取中文正文（去掉标题行）
    zh_lines = zh_content.split("\n")
    zh_body = "\n".join(zh_lines[1:]).strip() if len(zh_lines) > 1 else zh_content

    # 提取英文正文
    en_lines = en_content.split("\n")
    en_body = "\n".join(en_lines[1:]).strip() if len(en_lines) > 1 else en_content

    md = f"""---
slug: {slug}
title_zh: {title_zh}
title_en: {title_en}
date: {date_str}
type: {article_type}
lang: bilingual
---

# {first_line_emoji} {title_zh}

{zh_body}

---

## 🌐 English Version

{en_content}
"""
    return md.strip()


def save_article(slug, md_content):
    """保存文章到 blog 目录"""
    config.blog_dir.mkdir(parents=True, exist_ok=True)
    filepath = config.blog_dir / f"{slug}.md"
    filepath.write_text(md_content, encoding="utf-8")
    return filepath


# ═══════════════════════════════════════════════════════════
# 博客首页更新
# ═══════════════════════════════════════════════════════════

def update_blog_index(new_articles):
    """
    更新 docs/blog/index.html，加入新文章卡片
    """
    index_path = config.blog_dir / "index.html"
    card_template = """
    <a href="./{slug}" class="card card-{type}">
      <div class="card-badge">{emoji} {type}</div>
      <h3 class="card-title">{title_zh}</h3>
      <p class="card-excerpt">{title_en} — 一篇关于AI影视创作的{type}文章。</p>
      <div class="card-footer">
        <span class="card-date">📅 {date}</span>
        <span class="card-read">📖 {read_time}分钟</span>
      </div>
    </a>"""

    if index_path.exists():
        html = index_path.read_text(encoding="utf-8")
    else:
        html = _default_index_html()

    # 生成新卡片 HTML
    new_cards = ""
    for item in new_articles:
        emoji = TYPE_EMOJI.get(item["type"], "📄")
        card_html = card_template.format(
            slug=item["slug"],
            type=item["type"],
            emoji=emoji,
            title_zh=item["title_zh"],
            title_en=item["title_en"],
            date=item["date"],
            read_time=item.get("read_time", random.randint(5, 12)),
        )
        new_cards += card_html + "\n"

    # 获取已有卡片
    existing_cards_match = re.search(
        r'(<div class="grid" id="grid">)(.*?)(</div>\s*<footer)',
        html, re.DOTALL
    )

    if existing_cards_match:
        old_cards = existing_cards_match.group(2).strip()
        all_cards = new_cards.strip() + "\n" + old_cards
        html = html.replace(existing_cards_match.group(2), all_cards)
    else:
        # 如果没有 grid，在 </header> 后插入
        html = html.replace(
            "</header>",
            f"</header>\n<div class=\"grid\" id=\"grid\">\n{new_cards}\n</div>\n",
            1
        )

    # 更新文章数
    card_count = html.count('class="card"')
    today_str = datetime.now().strftime("%Y-%m-%d")
    html = re.sub(r'<span>📚 共 \d+ 篇文章</span>', f'<span>📚 共 {card_count} 篇文章</span>', html)
    html = re.sub(r'<span>📅 更新于 [\d-]+</span>', f'<span>📅 更新于 {today_str}</span>', html)

    index_path.write_text(html, encoding="utf-8")
    print(f"  📄 博客首页已更新 -> {index_path}")
    return index_path


def _default_index_html():
    """生成默认首页（如果不存在）"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎬 AI影视工具博客 -- 教程·评测·技巧·趋势</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #0a0a0b; --surface: #141416; --border: #2a2a2e;
      --text: #f4f4f5; --text-2: #a1a1aa; --text-3: #71717a;
      --accent: #6366f1; --radius: 16px;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'PingFang SC', sans-serif;
      background: var(--bg); color: var(--text); line-height: 1.6;
    }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 0 24px; }}
    .hero {{ padding: 60px 0 40px; text-align: center; border-bottom: 1px solid var(--border); margin-bottom: 48px; }}
    .hero h1 {{ font-size: 2.6rem; font-weight: 800; background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; }}
    .hero p {{ font-size: 1.1rem; color: var(--text-2); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; padding-bottom: 60px; }}
    .card {{ display: flex; flex-direction: column; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; transition: all 0.25s ease; }}
    .card:hover {{ transform: translateY(-4px); border-color: var(--accent); }}
    .card-badge {{ display: inline-block; font-size: 0.78rem; padding: 4px 12px; border-radius: 999px; background: rgba(99,102,241,0.1); color: var(--accent); margin-bottom: 14px; align-self: flex-start; }}
    .card-title {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 10px; }}
    .card-excerpt {{ font-size: 0.88rem; color: var(--text-2); flex-grow: 1; margin-bottom: 16px; }}
    .card-footer {{ display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-3); border-top: 1px solid var(--border); padding-top: 14px; }}
    .site-footer {{ text-align: center; padding: 32px 0 48px; border-top: 1px solid var(--border); color: var(--text-3); }}
    @media (max-width: 640px) {{ .hero h1 {{ font-size: 1.8rem; }} .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <div class="container">
    <header class="hero">
      <h1>🎬 AI影视工具博客</h1>
      <p>教程 · 对比 · 技巧 · 趋势 · 新闻 · 案例 · 工具推荐 · 行业分析</p>
      <div class="hero-stats" style="display:flex;justify-content:center;gap:32px;margin-top:20px;color:var(--text-3);font-size:0.9rem;">
        <span>📚 共 0 篇文章</span>
        <span>📅 更新于 {today}</span>
      </div>
    </header>
    <div class="grid" id="grid"></div>
    <footer class="site-footer">
      <p>🎬 <a href="https://zhanggengxi.github.io/ai-film-tools/">AI Film Shot Planner</a> 免费使用</p>
    </footer>
  </div>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════
# Git 操作
# ═══════════════════════════════════════════════════════════

def git_commit_and_push(repo_root, article_count, dry_run=False, no_push=False):
    """提交并推送新文章到 GitHub Pages"""
    os.chdir(repo_root)

    # 配置 git user（如果未设置全局）
    subprocess.run(
        ["git", "config", "user.name", config.git_user_name],
        capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.email", config.git_user_email],
        capture_output=True
    )

    # git add
    result = subprocess.run(
        ["git", "add", "docs/blog/"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  git add 失败: {result.stderr.strip()}")
        return False

    # 检查是否有变更
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True
    )
    if not result.stdout.strip():
        print("  ℹ️  没有新的变更，跳过提交")
        return True

    # git commit
    date_str = datetime.now().strftime("%Y-%m-%d")
    msg = f"🎬 Daily Content Factory: {article_count} 篇新文章 ({date_str})"
    result = subprocess.run(
        ["git", "commit", "-m", msg],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  git commit 失败: {result.stderr.strip()}")
        # 可能因为没有变更
        if "nothing to commit" in result.stderr:
            return True
        return False

    print(f"  ✅ 已提交: {msg}")

    if no_push:
        print(f"  ℹ️  --no-push 模式，跳过推送")
        return True

    if dry_run:
        print(f"  ℹ️  --dry-run 模式，跳过推送")
        return True

    # git push
    print("  📤 正在推送到远程...")
    result = subprocess.run(
        ["git", "push"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  git push 失败: {result.stderr.strip()}")
        print(f"  ℹ️  你可以稍后手动推送: cd {repo_root} && git push")
        return False

    print("  ✅ 推送成功")
    return True


# ═══════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════

def main():
    print(f"""
╔══ {'═' * 56}╗
║  🎬 AI Film Tools — Daily Content Factory v{VERSION}
║  多模型AI内容工厂 · 中英双语生成 · GitHub Pages 自动发布
╚══ {'═' * 56}╝
""")

    # ── 解析命令行参数 ──
    dry_run = "--dry-run" in sys.argv
    no_push = "--no-push" in sys.argv
    force_count = 0
    for arg in sys.argv:
        if arg.startswith("--count="):
            force_count = int(arg.split("=")[1])

    # ── 选择本周主题 ──
    count = force_count if force_count > 0 else config.count
    topics = get_weekly_topics(count=count)

    print(f"  📅 日期: {datetime.now().strftime('%Y-%m-%d %A')}")
    print(f"  🔢 本周生成: {len(topics)} 篇文章")
    print(f"  🤖 模型: {config.model_type}")
    print(f"  📂 博客目录: {config.blog_dir}")
    print()

    for t in topics:
        print(f"     [{t[0]}] {t[2]}  ({t[1]})")

    if dry_run:
        print(f"\n  ℹ️  --dry-run 模式，不生成内容。")
        return

    print(f"\n{'─' * 60}")
    print(f"  开始生成文章...")
    print(f"{'─' * 60}\n")

    # ── 生成文章 ──
    new_articles = []
    used_slugs = _load_used_slugs()

    for idx, (article_type, slug, title_zh) in enumerate(topics):
        print(f"[{idx+1}/{len(topics)}] 处理: {title_zh}")

        # 提取英文标题（从 TOPIC_POOL 中查找，或自动生成）
        title_en = title_zh  # 默认
        # TOPIC_POOL 没有存英文标题，我们让 AI 生成或自动构造
        # 简单方案：中译英前缀
        type_en_map = {
            "教程": "Tutorial", "对比": "Comparison", "技巧": "Tips",
            "新闻": "News", "案例": "Case Study", "趋势": "Trends",
            "工具推荐": "Tool Recommendation", "行业分析": "Industry Analysis",
        }
        type_en = type_en_map.get(article_type, "Article")
        # 让 AI 生成英文标题
        title_en_prompt = (
            f"Translate this Chinese article title to a natural English title for a blog post "
            f"about AI filmmaking tools: 「{title_zh}」\n"
            f"Output ONLY the English title, no quotes, no explanation."
        )
        en_title_result = None
        try:
            en_title_result = llm_chat(
                "You are a professional translator. Output only the translation, nothing else.",
                title_en_prompt
            )
        except Exception:
            pass

        if en_title_result and len(en_title_result) > 5 and len(en_title_result) < 200:
            title_en = en_title_result.strip().strip('"').strip("'")
        else:
            # Fallback: use Chinese title as-is with type prefix
            title_en = f"{type_en}: {title_zh}"

        # 生成中文文章
        zh_content = generate_article_zh(article_type, title_zh)

        # 翻译为英文
        en_content = translate_to_en(zh_content, title_en)

        # 构建双语 Markdown
        md_content = build_bilingual_markdown(
            slug, title_zh, title_en, article_type, zh_content, en_content
        )

        # 保存
        filepath = save_article(slug, md_content)
        print(f"     ✅ 已保存: {filepath}")

        # 记录
        article_info = {
            "slug": slug,
            "title_zh": title_zh,
            "title_en": title_en,
            "type": article_type,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "read_time": random.randint(5, 12),
            "filepath": str(filepath),
        }
        new_articles.append(article_info)
        used_slugs.add(slug)

        # 避免 API 限流，短暂休息
        if config.model_type != "demo" and idx < len(topics) - 1:
            time.sleep(1)

    # ── 保存已用 slugs ──
    _save_used_slugs(used_slugs)

    # ── 更新博客首页 ──
    print(f"\n{'─' * 60}")
    print(f"  更新博客首页...")
    update_blog_index(new_articles)

    # ── Git 提交与推送 ──
    print(f"\n{'─' * 60}")
    print(f"  Git 操作...")
    git_commit_and_push(
        config.blog_repo_path,
        len(new_articles),
        dry_run=dry_run,
        no_push=no_push,
    )

    # ── 完成报告 ──
    print(f"\n{'═' * 60}")
    print(f"  ✅ Daily Content Factory 完成！")
    print(f"  📊 生成了 {len(new_articles)} 篇双语文章")
    for a in new_articles:
        print(f"     📄 {a['title_zh']}  →  {a['filepath']}")
    print(f"{'═' * 60}")
    print(f"  博客首页: {config.blog_dir / 'index.html'}")
    print(f"  下次运行将自动轮换新主题 🎉")
    print(f"{'═' * 60}")


# ═══════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
