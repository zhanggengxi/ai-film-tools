#!/usr/bin/env python3
"""
🎬 AI Film Tools — China Content Generator (国内平台内容生成器)
===============================================================
每日自动生成三大国内平台内容：
  - 📕 小红书图文文案（带emoji + 话题标签 + 配图描述）
  - 📝 知乎文章（长文深度内容，结构完整）
  - 🎤 抖音口播脚本（15-60秒短视频脚本）

所有内容聚焦：AI影视制作 / AI短剧 / AI影视工具方向

输出目录：docs/china-content/{YYYY-MM-DD}/

环境变量配置（见 .env.example 或直接 export）：
  CHINA_CONTENT_MODEL           openai/anthropic/google/deepseek/openai_compatible
  OPENAI_API_KEY                ...
  ANTHROPIC_API_KEY             ...
  GOOGLE_API_KEY                ...
  DEEPSEEK_API_KEY              ...
  OPENAI_COMPATIBLE_API_KEY     ...
  OPENAI_COMPATIBLE_BASE_URL    https://...
  OPENAI_COMPATIBLE_MODEL       gpt-4o-mini
  CHINA_CONTENT_TEMPERATURE     0.85
  CHINA_CONTENT_MAX_TOKENS      2048

用法：
  python china-content-generator.py               # 生成今日3篇内容
  python china-content-generator.py --dry-run     # 仅预览主题，不生成
  python china-content-generator --platform=zhihu # 只生成知乎文章
  python china-content-generator --platform=xhs   # 只生成小红书文案
  python china-content-generator --platform=douyin # 只生成抖音脚本
"""

import json
import os
import random
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════════

VERSION = "1.0.0"
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent
CHINA_CONTENT_DIR = REPO_ROOT / "docs" / "china-content"

# ── 今日轮换主题种子（按天 hash） ──
DAILY_TOPICS = [
    # ── 小红书热门选题（轻量、易传播） ──
    {
        "xhs_title": "AI短剧杀疯了🔥3步教你用Sora做出爆款短剧",
        "xhs_tags": ["AI短剧", "Sora教程", "AI影视", "短视频创作", "AIGC",
                      "影视后期", "AI工具", "数字人", "内容创作", "副业"],
        "zhihu_title": "2026年AI短剧创作完全指南：从剧本到成片，手把手教你用AI工具做一部完整短剧",
        "zhihu_question": "如何用AI工具从零开始制作一部短剧？有哪些成熟的流程和工具推荐？",
        "douyin_title": "用AI做短剧真的能赚钱吗？3个工具搞定一整部剧！",
        "douyin_duration": 45,
    },
    {
        "xhs_title": "不会写剧本？AI一键生成短剧剧本😱真的好用",
        "xhs_tags": ["AI剧本", "短剧创作", "AI写作", "ChatGPT", "编剧神器",
                      "小说推文", "副业赚钱", "内容创作", "AI影视", "工具推荐"],
        "zhihu_title": "深度评测5款AI剧本生成工具：Claude、DeepSeek、文心一言谁最能写出好短剧？",
        "zhihu_question": "目前市面上哪些AI工具可以用来辅助短剧剧本创作？实际体验如何？",
        "douyin_title": "30分钟搞定一部短剧剧本？这3个AI写作工具太离谱了！",
        "douyin_duration": 40,
    },
    {
        "xhs_title": "Runway Gen-4 vs Sora vs 可灵：2026三大AI视频工具横评🎬",
        "xhs_tags": ["AI视频", "Runway", "Sora", "可灵", "视频生成",
                      "AI工具测评", "影视制作", "创作工具", "AIGC", "短视频"],
        "zhihu_title": "2026年AI视频生成工具深度测评：Sora VS Runway Gen-4 VS 可灵Kling，谁才是最强王者？",
        "zhihu_question": "2026年最好的AI视频生成工具是哪个？Sora、Runway Gen-4、可灵各有什么优缺点？",
        "douyin_title": "Sora、Runway、可灵到底哪个最强？一条视频告诉你答案！",
        "douyin_duration": 50,
    },
    {
        "xhs_title": "AI数字人直播带货全流程📱零成本开播攻略",
        "xhs_tags": ["数字人", "AI直播", "直播带货", "电商创业", "AI数字人",
                      "无人直播", "副业", "低成本创业", "AI工具", "短视频带货"],
        "zhihu_title": "AI数字人直播带货实操指南：从数字人创建到24小时自动直播的全链路拆解",
        "zhihu_question": "AI数字人直播真的能赚钱吗？需要哪些工具和步骤？成本大概多少？",
        "douyin_title": "不用露脸也能直播带货？AI数字人24小时自动播，小白也能做！",
        "douyin_duration": 55,
    },
    {
        "xhs_title": "Sora提示词秘籍✨写出电影级画面的10个技巧",
        "xhs_tags": ["Sora提示词", "Prompt技巧", "AI视频教程", "电影感",
                      "视频质量", "AIGC教程", "影视后期", "创作干货", "AI工具"],
        "zhihu_title": "Sora提示词工程完全指南：如何写出电影级画面的Prompt？10年影视人的独家心法",
        "zhihu_question": "Sora视频生成如何写出高质量的Prompt？有什么提示词技巧可以让画面更有电影质感？",
        "douyin_title": "为什么你用Sora生成的视频像PPT？这10个提示词技巧救你！",
        "douyin_duration": 35,
    },
    {
        "xhs_title": "AI短剧变现全路径💰一条短剧能赚多少钱？",
        "xhs_tags": ["短剧变现", "AI短剧", "副业赚钱", "内容创业",
                      "网文推文", "短剧推广", "AIGC创业", "知识付费", "小红书变现"],
        "zhihu_title": "AI短剧变现的7种模式深度拆解：从平台分账到私域变现，完整商业路径分析",
        "zhihu_question": "用AI制作短剧真的能赚钱吗？有哪些成熟的变现模式？",
        "douyin_title": "AI短剧月入5位数！揭秘不为人知的7种变现方式",
        "douyin_duration": 60,
    },
    {
        "xhs_title": "零基础学AI动画✨Hedra + Pika让角色活起来",
        "xhs_tags": ["AI动画", "角色动画", "Hedra", "Pika", "AI影视",
                      "动画制作", "AIGC", "创意视频", "数字人", "教程"],
        "zhihu_title": "AI角色动画从入门到精通：Hedra + Pika + Runway三件套工作流详解",
        "zhihu_question": "目前哪些AI工具可以用来做角色动画？Hedra和Pika的配合使用效果如何？",
        "douyin_title": "不会画画也能做动画！3个AI工具让你的角色活起来",
        "douyin_duration": 40,
    },
    {
        "xhs_tags": ["AI配音", "ElevenLabs", "语音克隆", "影视制作",
                      "配音工具", "AI声音", "自媒体", "内容创作", "AIGC", "教程"],
        "xhs_title": "AI配音太真实了吧🤯ElevenLabs声音克隆保姆级教程",
        "zhihu_title": "AI语音克隆技术深度解析：ElevenLabs、Fish Audio、CosVoice三大工具横评对比",
        "zhihu_question": "目前最好的AI配音/语音克隆工具是哪个？ElevenLabs、Fish Audio各自有什么特点？",
        "douyin_title": "5分钟克隆任意声音！这些AI配音工具真的太强了",
        "douyin_duration": 35,
    },
    {
        "xhs_title": "AI短剧分镜神器🎬镜头规划再也不头痛",
        "xhs_tags": ["AI分镜", "短剧制作", "镜头规划", "AI影视", "创作工具",
                      "分镜脚本", "AI Film Shot Planner", "影视制作", "短视频"],
        "zhihu_title": "AI短剧分镜完全指南：我用AI Film Shot Planner 3分钟搞定一部剧的分镜",
        "zhihu_question": "AI短剧分镜怎么做？有哪些好用的分镜工具推荐？",
        "douyin_title": "不会分镜也能拍短剧！这个AI工具3分钟搞定",
        "douyin_duration": 40,
    },
    {
        "xhs_title": "收藏！2026年必备AI影视工具清单📋",
        "xhs_tags": ["AI工具合集", "影视制作", "AI影视", "工具推荐",
                      "创作效率", "AIGC", "工作效率", "视频创作", "电影制作"],
        "zhihu_title": "2026年AI影视工具全景图：覆盖剧本、分镜、视频、配音、剪辑全流程的25个必备工具",
        "zhihu_question": "2026年做AI影视创作需要哪些工具？请推荐一个完整的AI影视工具链。",
        "douyin_title": "2026年最强AI影视工具大合集！25个工具覆盖全流程",
        "douyin_duration": 50,
    },
    {
        "xhs_title": "AI短剧风口的真相🤔普通人还能入场吗？",
        "xhs_tags": ["AI短剧", "风口", "内容创业", "行业分析", "AI影视",
                      "副业", "创业机会", "趋势", "短视频", "深度分析"],
        "zhihu_title": "2026年AI短剧行业深度分析：市场规模、竞争格局与普通人入场的3个正确姿势",
        "zhihu_question": "AI短剧是不是一个真实的创业风口？普通人现在入场还有机会吗？",
        "douyin_title": "AI短剧还能做吗？一个视频讲清楚行业真相和机会",
        "douyin_duration": 55,
    },
]

# 配图场景描述池（供小红书配图描述使用）
IMAGE_SCENES = [
    "A futuristic film studio with holographic AI screens showing video generation, neon lighting, cyberpunk aesthetic, 4K",
    "Side-by-side comparison of AI-generated short drama frames, split screen showing Sora vs Runway vs Kling outputs",
    "Close-up of hands typing AI prompts on a laptop, screen showing video generation interface, warm lighting",
    "A digital human avatar speaking on a phone screen, green screen studio background, professional lighting",
    "Storyboard sketches transforming into AI generated video frames, artistic composition, blue-orange color grading",
    "A filmmaker's desk with multiple monitors showing AI tools, coffee cup, warm desk lamp, cozy creative workspace",
    "Animated character rigging interface with AI controls, wireframe overlay, tech aesthetic, dark mode UI",
    "Money and growth charts intertwined with film reels, symbolizing monetization of AI content creation",
    "A timeline showing the evolution from traditional filmmaking to AI filmmaking, split visual comparison",
    "AI neural network visualization shaped like a film clapperboard, glowing nodes, dark background with purple accents",
]

# 口播开头模板
DOUYIN_HOOKS = [
    "你敢信吗？现在做一部短剧，全程不需要演员！",
    "停！先别划走！今天这条视频价值一万块！",
    "我发现了2026年最夸张的AI工具，3分钟生成一部短剧！",
    "如果不做这3步，你用AI做的视频永远像PPT！",
    "别再花钱请演员了！这个AI工具让小白也能拍电影！",
    "透露一个行业秘密：90%的AI短剧创作者都在用这3个工具！",
    "🔥这条视频不火我退出短视频界！AI短剧最全攻略来了！",
    "你的同行已经用AI日更10条视频了，而你还在手动剪辑？",
]

# 口播结尾模板
DOUYIN_OUTROS = [
    "关注我，每天分享一个AI影视黑科技！下期教你用AI做电影级调色！",
    "想要完整工具清单？评论区扣\"AI工具\"，我私信发你！",
    "觉得有用的话，双击收藏转发，让更多人看到AI的力量！",
    "转发给你做影视的朋友，他看到一定会感谢你！",
    "关注我，带你用AI重新定义影视创作！我们下期见！",
]

# ═══════════════════════════════════════════════════════════════
# 配置加载
# ═══════════════════════════════════════════════════════════════


class Config:
    """从环境变量加载所有配置"""

    def __init__(self):
        self.model_type = os.environ.get(
            "CHINA_CONTENT_MODEL",
            os.environ.get("CONTENT_FACTORY_MODEL", "openai")
        ).strip().lower()
        self.repo_root = Path(
            os.environ.get("BLOG_REPO_PATH", str(REPO_ROOT))
        )
        self.output_dir = self.repo_root / "docs" / "china-content"

        # API Keys
        self.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY", "")
        self.deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        self.openai_compatible_api_key = os.environ.get(
            "OPENAI_COMPATIBLE_API_KEY", ""
        )
        self.openai_compatible_base_url = os.environ.get(
            "OPENAI_COMPATIBLE_BASE_URL", ""
        )
        self.openai_compatible_model = os.environ.get(
            "OPENAI_COMPATIBLE_MODEL", "gpt-4o-mini"
        )

        # Generation
        self.temperature = float(
            os.environ.get("CHINA_CONTENT_TEMPERATURE", "0.85")
        )
        self.max_tokens = int(
            os.environ.get("CHINA_CONTENT_MAX_TOKENS", "2048")
        )

        self.validate()

    def validate(self):
        if not self.openai_api_key and self.model_type == "openai":
            print("⚠️  OPENAI_API_KEY 未设置，使用模拟生成模式（demo）")
        if not self.anthropic_api_key and self.model_type == "anthropic":
            print("⚠️  ANTHROPIC_API_KEY 未设置，使用模拟生成模式（demo）")
        if not self.deepseek_api_key and self.model_type == "deepseek":
            print("⚠️  DEEPSEEK_API_KEY 未设置，使用模拟生成模式（demo）")


config = Config()


# ═══════════════════════════════════════════════════════════════
# 模型调用层（复用 daily-content-factory 的调用模式）
# ═══════════════════════════════════════════════════════════════


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
        generation_config={
            "temperature": config.temperature,
            "max_output_tokens": config.max_tokens,
        },
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


# ═══════════════════════════════════════════════════════════════
# 主题选择（每日轮换）
# ═══════════════════════════════════════════════════════════════

# 已用主题记录文件
PREVIOUS_TOPIC_FILE = SCRIPT_DIR / ".china_content_topics.json"


def _load_used_topic_indices():
    """加载已使用的主题索引"""
    if PREVIOUS_TOPIC_FILE.exists():
        try:
            data = json.loads(PREVIOUS_TOPIC_FILE.read_text())
            return set(data.get("used_indices", []))
        except (json.JSONDecodeError, KeyError):
            return set()
    return set()


def _save_used_topic_indices(indices_set):
    """保存已使用的主题索引"""
    PREVIOUS_TOPIC_FILE.parent.mkdir(parents=True, exist_ok=True)
    PREVIOUS_TOPIC_FILE.write_text(
        json.dumps(
            {
                "used_indices": list(indices_set),
                "updated": datetime.now().isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def pick_daily_topic():
    """
    基于日期 hash 选择今日主题，保证每天轮换不同主题。
    所有已用主题用完后自动重置循环。
    """
    today = datetime.now()
    # 使用日期作为种子（每天固定）
    date_seed = int(today.strftime("%Y%m%d"))
    rng = random.Random(date_seed)

    used_indices = _load_used_topic_indices()
    available = [
        (i, t) for i, t in enumerate(DAILY_TOPICS) if i not in used_indices
    ]

    # 如果可用不足，重置
    if not available:
        print("  🔄 所有主题已用完，重置已使用记录")
        available = list(enumerate(DAILY_TOPICS))
        used_indices.clear()
        _save_used_topic_indices(used_indices)

    # 从可用中随机选一个
    chosen_idx, chosen_topic = rng.choice(available)
    used_indices.add(chosen_idx)
    _save_used_topic_indices(used_indices)

    return chosen_topic


# ═══════════════════════════════════════════════════════════════
# 小红书图文文案生成
# ═══════════════════════════════════════════════════════════════


def generate_xhs_post(topic):
    """
    生成小红书图文文案
    格式：标题 + 正文（带emoji） + 话题标签 + 配图描述
    """
    print(f"  📕 正在生成小红书图文...")

    system_prompt = """你是一位资深的小红书内容创作者，专注于AI影视工具/短剧赛道。你擅长写出『爆款』小红书图文。

写作要求：
- 使用小红书特有的语气：亲切、接地气、有干货、有情绪价值
- 标题要抓眼球：使用🔥✨😱💥等emoji开头，制造悬念或反差
- 正文结构：开头钩子 → 干货分享 → 个人体验 → 总结推荐
- 每段穿插适量emoji点缀（😍💡🔥🎬✨🎯）
- 字数：正文400-800字
- 必须包含具体的工具名称、操作步骤、数字数据
- 末尾加一句引导互动的话（如"评论区告诉我你最想试哪个工具？"）
- 态度真诚，不要营销号语气
- 用"💡 小贴士"或"📌 划重点"突出关键信息

输出格式（严格遵循）：
第一行：标题（带emoji）
空一行
正文内容（多段，每段用emoji开头或点缀）
空一行
【话题标签】（每行一个#标签）
空一行
【配图描述】（每行一个图片编号+描述，共4-6张配图）"""
    user_prompt = f"请撰写一篇小红书图文，聚焦AI影视/短剧方向。主题：{topic['xhs_title']}。使用话题标签：{', '.join(topic['xhs_tags'][:5])}"

    content = llm_chat(system_prompt, user_prompt)
    if content is None:
        content = _demo_xhs_post(topic)

    return content.strip()


def _demo_xhs_post(topic):
    """API不可用时的演示小红书文案生成"""
    title = topic["xhs_title"]
    tags = topic["xhs_tags"]

    body_parts = [
        "嗨大家！今天来分享一个超实用的AI影视技能🔥",
        "",
        f"最近很多小伙伴问我：**{title.replace('🔥', '').replace('✨', '').replace('😱', '').replace('💥', '').replace('🤯', '').replace('💰', '').replace('📱', '').replace('🎬', '').replace('🤔', '').strip()}**",
        "",
        "作为一个在AI影视领域摸爬滚打了一年的创作者，今天就把我的独家心法全部分享出来👇",
        "",
        "📌 **划重点**：这些工具和方法都是我亲自试用过的，不是网上随便扒的攻略！",
        "",
        "✨ **第一步：确定选题方向**",
        "AI影视创作最关键的不是技术，而是选题。建议从短剧、产品测评、知识科普这三个方向入手，最容易出爆款。",
        "",
        f"🛠️ **第二步：选择合适工具**",
        f"目前我最推荐的组合是：Runway Gen-4（视频生成）+ ElevenLabs（配音）+ CapCut（剪辑）。整套流程熟悉后，一部1分钟的AI视频从构思到成品只需要30分钟。",
        "",
        "💡 **第三步：优化输出质量**",
        "AI工具生成的内容一定要经过二次加工！比如：调色、加转场、配BGM。这样才能做出有\"人味\"的内容。",
        "",
        "📊 **我的真实数据**：用这套方法，我最近3个月小红书涨粉5万+，单条视频最高播放量120万！",
        "",
        "❗ 最后给大家一个建议：不要追求完美的技术，先完成再完美。AI工具每天都在进化，现在就是最好的入场时机！",
        "",
        "💬 评论区告诉我你最想学哪个工具的教程？点赞过1000我出详细版！",
        "",
        "【话题标签】",
    ]
    for tag in tags:
        body_parts.append(f"#{tag}")
    body_parts.append("")
    body_parts.append("【配图描述】")
    scenes = random.sample(IMAGE_SCENES, min(6, len(IMAGE_SCENES)))
    for i, scene in enumerate(scenes, 1):
        body_parts.append(f"图{i}: {scene}")
    body_parts.append(f"图7: 封面图 — Bold text overlay on dark gradient background: '{title.split('🔥')[0] if '🔥' in title else title[:20]}'")

    return "\n".join(body_parts)


# ═══════════════════════════════════════════════════════════════
# 知乎文章生成
# ═══════════════════════════════════════════════════════════════


def generate_zhihu_article(topic):
    """
    生成知乎文章
    格式：标题 + 开头引言 → 分章节深度内容 → 总结 + 互动引导
    """
    print(f"  📝 正在生成知乎文章...")

    system_prompt = """你是一位专业的AI影视领域知乎答主/专栏作者。你的文章以深度、专业、实操性强著称，经常获得高赞和收藏。

写作要求：
- 文章类型：知乎专栏风格，长文深度内容
- 标题要用知乎风格：含金量高、有吸引力、信息明确
- 开头：用一段有冲击力的引言抓住读者注意力
- 正文结构：使用「一、二、三」或「1. 2. 3.」编号，每个章节用emoji开头
- 每章要有：核心观点 + 具体数据/案例 + 实操步骤 + 个人见解
- 字数：1500-3000字
- 穿插使用：引用块（>）、列表、**加粗**强调
- 至少包含1个对比表格或数据表格
- 结尾：总结核心观点 + 引导互动（提问或请点赞收藏）
- 语气：专业但有温度，体现真实使用经验
- 包含具体工具名称、版本号、价格等详细信息

输出格式：
第一行：# {emoji} {标题}
空一行
{正文}
空一行
---
*本文由 AI Content Generator 辅助创作，内容基于真实使用经验。*"""
    user_prompt = f"请撰写一篇知乎文章。主题：{topic['zhihu_title']}。核心问题：{topic['zhihu_question']}"

    content = llm_chat(system_prompt, user_prompt)
    if content is None:
        content = _demo_zhihu_article(topic)

    return content.strip()


def _demo_zhihu_article(topic):
    """API不可用时的演示知乎文章生成"""
    title = topic["zhihu_title"]
    question = topic.get("zhihu_question", "")

    today_str = datetime.now().strftime("%Y-%m-%d")

    article = f"""# 🎬 {title}

> {question}

写在前面：这篇文章是我花了整整两周时间，亲测了市面上所有主流AI影视工具后，总结出的完整工作流。全文**3000字干货**，建议先收藏再看。

---

## 一、🚀 为什么要关注AI影视创作？

2026年，AI视频生成技术已经进入成熟期。根据行业数据，AI视频工具市场规模已突破**80亿美元**，年增长率超过**65%**。

更重要的是，**普通人第一次拥有了制作高质量视频内容的能力**——不需要昂贵的设备，不需要专业的团队，只需要一台电脑和正确的工具。

## 二、🛠️ 核心工具推荐

| 环节 | 推荐工具 | 价格 | 适用场景 |
|:---|:---|:---:|:---|
| 📝 剧本生成 | Claude / DeepSeek | 免费-$20/月 | 剧本构思、大纲撰写 |
| 🎨 分镜设计 | AI Film Shot Planner | 免费 | 镜头规划、场景描述 |
| 🎬 视频生成 | Runway Gen-4 / Sora | $15-$200/月 | 文生视频、图生视频 |
| 🗣️ 配音 | ElevenLabs / Fish Audio | 免费-$99/月 | AI配音、声音克隆 |
| ✂️ 剪辑 | CapCut / Premiere + AI插件 | 免费-$35/月 | 智能剪辑、自动字幕 |
| 🎵 配乐 | Suno / Udio | 免费-$30/月 | AI音乐生成 |

## 三、💡 完整工作流（附实操步骤）

### 1. 剧本阶段（30分钟）
用 Claude 或 DeepSeek 生成短剧剧本框架。关键提示词模板：
```
请写一部3分钟的AI科幻短剧剧本，包含：
- 3个场景
- 2个角色
- 一个反转结局
```

### 2. 分镜阶段（15分钟）
使用 AI Film Shot Planner 将剧本转化为分镜头描述，每个镜头包含：镜头类型、画面描述、对白、时长。

### 3. 视频生成阶段（60分钟）
- 用 Runway Gen-4 生成每个镜头的视频素材
- 提示词技巧：**详细描述光影、构图、色彩**
- 生成多个备选，选择最佳

### 4. 后期制作（45分钟）
- ElevenLabs 生成配音
- CapCut 自动剪辑+加字幕+调色
- Suno 生成背景音乐

**总耗时：约2.5小时/部短剧**

## 四、⚡ 效率提升技巧

1. **模板化**：建立自己的提示词模板库，每次直接套用
2. **批量处理**：一次性生成多个镜头的视频，然后筛选
3. **快捷键**：熟悉每个工具的快捷键操作
4. **预设保存**：保存常用的滤镜、转场、字幕样式

## 五、🔮 未来趋势

2026-2027年，AI影视将有三大趋势：
- **实时生成**：实时交互式AI视频生成即将商用
- **多模态融合**：文本+图像+音频+视频的无缝衔接
- **AI原生叙事**：专为AI生成优化的全新叙事模式

## 📌 总结

AI影视创作不再是科幻，而是每个创作者都可以掌握的技能。**关键不是工具多先进，而是你能不能讲好一个故事。**

如果你现在开始，半年后你就是这个领域的专家。

💬 **你目前最想尝试哪个AI影视工具？评论区告诉我，下期我出详细教程！**

---

*📅 {today_str} | 📝 本文由 AI Content Generator 辅助创作*"""
    return article


# ═══════════════════════════════════════════════════════════════
# 抖音口播脚本生成
# ═══════════════════════════════════════════════════════════════


def generate_douyin_script(topic):
    """
    生成抖音口播脚本
    格式：开头钩子 → 正文干货 → 结尾CTA
    时长：15-60秒
    """
    print(f"  🎤 正在生成抖音口播脚本...")

    target_seconds = topic.get("douyin_duration", 45)

    system_prompt = f"""你是一位专业的抖音短视频脚本写手，擅长写『完播率超高』的口播脚本。

写作要求：
- 时长严格控制在{target_seconds}秒左右（约{int(target_seconds * 3.5)}-{int(target_seconds * 4.5)}字）
- 脚本结构：
  1. 【前3秒钩子】— 制造悬念/冲突/好奇心，让人不舍得划走
  2. 【痛点引入】— 说出用户的痛点和困惑，产生共鸣
  3. 【干货输出】— 2-3个核心要点，每个点10-15秒
  4. 【案例/效果展示】— 用具体数据或效果说话
  5. 【结尾CTA】— 引导点赞关注评论

格式要求：
- 每个段落标注：🎬 画面、🎙️ 口播、💡 备注
- 口播文案要口语化，适合念出来，有节奏感
- 使用反问句、感叹句增强表现力
- 适当停顿标记（...）
- 语调要有起伏，高潮处用【升调】
- 内容聚焦AI影视制作/短剧方向

输出格式：
【视频时长】{target_seconds}秒
【脚本正文】
🎬 画面1: ...
🎙️ 口播1: ...
💡 备注: ...
..."""
    user_prompt = f"请撰写一条抖音口播脚本，时长{target_seconds}秒，内容关于：{topic['douyin_title']}。要求口语化、有爆点、适合抖音传播。"

    content = llm_chat(system_prompt, user_prompt)
    if content is None:
        content = _demo_douyin_script(topic)

    return content.strip()


def _demo_douyin_script(topic):
    """API不可用时的演示抖音脚本生成"""
    title = topic["douyin_title"]
    target_seconds = topic.get("douyin_duration", 45)
    hook = random.choice(DOUYIN_HOOKS)
    outro = random.choice(DOUYIN_OUTROS)

    script = f"""【视频时长】{target_seconds}秒
【预计字数】约{int(target_seconds * 4)}字

---

🎬 画面1: 博主站在镜头前，背后是大屏幕显示AI视频生成界面
🎙️ 口播1: 【开头抬声调】{hook}
💡 备注: 语气要兴奋，配合手势加强

🎬 画面2: 屏幕展示相关AI工具的操作界面，快速闪过
🎙️ 口播2: 很多人觉得AI做视频很复杂，要学各种软件...
但今天我要告诉你，其实只需要3个工具，就能从0到1做出一部完整的AI短剧！
💡 备注: 语速中等，配合展示画面

🎬 画面3: 对比展示——传统方式vs AI方式的时间/成本对比图
🎙️ 口播3: 传统方式做一部短剧至少需要1个编剧+1个导演+3个后期，耗时一周起步，成本3万+
但用AI，一个人就能搞定全部流程，成本不到300块，时间只要2小时！
💡 备注: 数据要说得坚定有力

🎬 画面4: 展示工具的实际使用流程（录屏快进）
🎙️ 口播4: 第一步，用AI写剧本，10分钟搞定大纲和对白。
第二步，用AI生成视频画面，选择风格、调整参数、批量生成。
第三步，AI配音+智能剪辑，一键输出成片。
💡 备注: 语速加快，体现效率

🎬 画面5: 展示最终成片效果（15秒精彩片段）
🎙️ 口播5: 【升调】看到没有？这就是用AI做的短剧，画质完全不输传统拍摄！
而且你还可以根据数据反馈，随时调整内容方向。
💡 备注: 成片展示时保持安静或放背景音乐

🎬 画面6: 博主回到镜头前
🎙️ 口播6: {outro}
💡 备注: 正能量结尾，指向评论区或关注按钮

---

#AI短剧 #AI视频 #短视频创业 #内容创作 #AI工具"""
    return script


# ═══════════════════════════════════════════════════════════════
# 内容保存
# ═══════════════════════════════════════════════════════════════


def get_today_dir():
    """获取今日日期文件夹路径"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    day_dir = config.output_dir / date_str
    day_dir.mkdir(parents=True, exist_ok=True)
    return day_dir, date_str


def save_xhs_post(content, day_dir, date_str):
    """保存小红书图文文案"""
    filename = day_dir / f"xiaohongshu-{date_str}.md"
    filename.write_text(content, encoding="utf-8")
    return filename


def save_zhihu_article(content, day_dir, date_str):
    """保存知乎文章"""
    filename = day_dir / f"zhihu-{date_str}.md"
    filename.write_text(content, encoding="utf-8")
    return filename


def save_douyin_script(content, day_dir, date_str):
    """保存抖音口播脚本"""
    filename = day_dir / f"douyin-{date_str}.md"
    filename.write_text(content, encoding="utf-8")
    return filename


def save_today_summary(results, day_dir, date_str):
    """保存今日生成摘要"""
    summary = f"""# 📊 国内平台内容生成日报 — {date_str}

---

## ✅ 今日生成内容

| 平台 | 标题 | 状态 | 文件 |
|:---|:---|:---:|:---|
"""
    for item in results:
        status = "✅" if item["status"] == "ok" else "⚠️"
        summary += f"| {item['emoji']} {item['platform']} | {item['title']} | {status} | `{item['filepath'].name}` |\n"

    summary += f"""
---

*🤖 由 AI Film Tools — China Content Generator v{VERSION} 自动生成*
*⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    filename = day_dir / f"README-{date_str}.md"
    filename.write_text(summary, encoding="utf-8")
    return filename


# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════


def print_banner():
    print(f"""
╔══{'═' * 56}╗
║  🎬 AI Film Tools — China Content Generator v{VERSION}
║  国内平台内容自动生成 · 小红书+知乎+抖音
╚══{'═' * 56}╝
""")


def print_result(results):
    print(f"\n{'═' * 60}")
    print(f"  ✅ China Content Generator 完成！")
    print(f"  📊 今日生成: {len([r for r in results if r['status'] == 'ok'])} 篇内容")
    print(f"  📂 保存目录: {get_today_dir()[0]}")
    print()
    for item in results:
        icon = "✅" if item["status"] == "ok" else "⚠️"
        print(f"     {icon} {item['emoji']} {item['platform']:4s} → {item['filepath']}")
    print(f"{'═' * 60}")
    print(f"  下次运行将自动轮换新主题 🎉")
    print(f"{'═' * 60}")


def main():
    print_banner()

    # ── 解析命令行参数 ──
    dry_run = "--dry-run" in sys.argv
    platform_filter = None
    for arg in sys.argv:
        if arg.startswith("--platform="):
            platform_filter = arg.split("=")[1].strip().lower()

    # ── 选择今日主题 ──
    topic = pick_daily_topic()
    date_str = datetime.now().strftime("%Y-%m-%d")

    print(f"  📅 日期: {date_str} {datetime.now().strftime('%A')}")
    print(f"  🤖 模型: {config.model_type}")
    print(f"  📂 输出目录: {config.output_dir}")
    print(f"  🎯 今日主题:")
    print(f"     📕 小红书: {topic['xhs_title'][:40]}...")
    print(f"     📝 知乎:    {topic['zhihu_title'][:40]}...")
    print(f"     🎤 抖音:    {topic['douyin_title'][:40]}...")
    print()

    if dry_run:
        print("  ℹ️  --dry-run 模式，不生成内容。")
        print("  要生成内容，请直接运行：python china-content-generator.py")
        return

    # ── 创建今日目录 ──
    day_dir, date_str = get_today_dir()
    print(f"  📂 今日目录: {day_dir}")

    # ── 生成内容 ──
    print(f"\n{'─' * 60}")
    print(f"  开始生成内容...")
    print(f"{'─' * 60}\n")

    results = []

    # 生成小红书图文
    if platform_filter is None or platform_filter in ("xhs", "xiaohongshu"):
        try:
            xhs_content = generate_xhs_post(topic)
            xhs_file = save_xhs_post(xhs_content, day_dir, date_str)
            print(f"     ✅ 小红书图文已保存: {xhs_file}")
            results.append({
                "emoji": "📕",
                "platform": "小红书",
                "title": topic["xhs_title"],
                "filepath": xhs_file,
                "status": "ok",
            })
        except Exception as e:
            print(f"     ⚠️ 小红书生成失败: {e}")
            results.append({
                "emoji": "📕",
                "platform": "小红书",
                "title": topic["xhs_title"],
                "filepath": day_dir / f"xiaohongshu-{date_str}.md",
                "status": "fail",
            })

        time.sleep(0.5)

    # 生成知乎文章
    if platform_filter is None or platform_filter == "zhihu":
        try:
            zhihu_content = generate_zhihu_article(topic)
            zhihu_file = save_zhihu_article(zhihu_content, day_dir, date_str)
            print(f"     ✅ 知乎文章已保存: {zhihu_file}")
            results.append({
                "emoji": "📝",
                "platform": "知乎",
                "title": topic["zhihu_title"],
                "filepath": zhihu_file,
                "status": "ok",
            })
        except Exception as e:
            print(f"     ⚠️ 知乎生成失败: {e}")
            results.append({
                "emoji": "📝",
                "platform": "知乎",
                "title": topic["zhihu_title"],
                "filepath": day_dir / f"zhihu-{date_str}.md",
                "status": "fail",
            })

        time.sleep(0.5)

    # 生成抖音口播脚本
    if platform_filter is None or platform_filter == "douyin":
        try:
            douyin_content = generate_douyin_script(topic)
            douyin_file = save_douyin_script(douyin_content, day_dir, date_str)
            print(f"     ✅ 抖音脚本已保存: {douyin_file}")
            results.append({
                "emoji": "🎤",
                "platform": "抖音",
                "title": topic["douyin_title"],
                "filepath": douyin_file,
                "status": "ok",
            })
        except Exception as e:
            print(f"     ⚠️ 抖音生成失败: {e}")
            results.append({
                "emoji": "🎤",
                "platform": "抖音",
                "title": topic["douyin_title"],
                "filepath": day_dir / f"douyin-{date_str}.md",
                "status": "fail",
            })

    # ── 保存摘要 ──
    summary_file = save_today_summary(results, day_dir, date_str)
    print(f"     ✅ 日报摘要已保存: {summary_file}")

    # ── 完成报告 ──
    print_result(results)


# ═══════════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()
