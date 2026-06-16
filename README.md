# 🎬 AI Film Tools · 人工智能影视制作工具

> **Open-source AI tools for film production, shot planning, prompt engineering, and creative workflows**
> **开源人工智能影视制作工具集 —— 镜头规划、提示词工程与创意工作流**

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/status-alpha-yellow" alt="Status: Alpha">
  <img src="https://img.shields.io/badge/language-HTML%2FJS%2FCSS-orange" alt="Language">
  <img src="https://img.shields.io/badge/AI-Film%20Tools-brightgreen" alt="AI Film Tools">
</p>

---

## 📖 Overview · 概述

**AI Film Tools** is an open-source collection of practical AI-powered tools designed specifically for **AI filmmakers**, **prompt engineers**, **content creators**, and **independent directors**. Our mission is to democratize AI film production — making professional-grade AI filmmaking tools accessible to everyone.

**AI Film Tools** 是一个专为 **AI影视创作者**、**提示词工程师**、**内容创作者** 和 **独立导演** 打造的开源 AI 实用工具集。我们的使命是让 AI 影视制作民主化 —— 让每个人都能使用专业级的 AI 电影制作工具。

---

## 🧰 Tools · 工具集

### ✅ Available Now · 当前可用

| Tool · 工具 | Description · 描述 | Status · 状态 |
|------------|-------------------|--------------|
| **🎥 AI Film Shot Planner** | Interactive shot-by-shot planning tool with scene composition, camera angles, lighting setup, and prompt export | ✅ Stable · 稳定版 |

### 🚧 Coming Soon · 即将推出

| Tool · 工具 | Description · 描述 | Status · 状态 |
|------------|-------------------|--------------|
| **🤖 Prompt Generator** | AI-powered cinematic prompt generation for text-to-video models | 🔧 In Development |
| **📋 Production Workflow** | End-to-end AI film production workflow templates | 📝 Planning |
| **🎭 Character Consistency** | AI character consistency system for multi-shot narratives | 📝 Planning |
| **⚙️ Pipeline Integrations** | Integration tools for Runway, Pika, Sora, Kling, and more | 🔧 In Development |

---

## 🎥 AI Film Shot Planner · AI电影镜头规划器

A comprehensive, interactive web tool for planning every shot of your AI-generated film. Perfect for directors working with text-to-video AI models like Sora, Runway Gen, Pika, Kling, and more.

一个全面的交互式网页工具，用于规划 AI 生成电影的每一个镜头。非常适合使用 Sora、Runway Gen、Pika、Kling 等文生视频 AI 模型的导演。

### ✨ Features · 功能特性

| Feature | Description |
|---------|-------------|
| **🎯 Scene Management** | Add, edit, delete, and reorder scenes with drag-and-drop simplicity · 场景管理：拖放式增删改排 |
| **📐 Shot Composition** | Configure aspect ratio, camera angle, movement, framing, and lens · 镜头构图：配置宽高比、机位、运动、景别和焦距 |
| **🎨 Visual Style** | Set color palette, lighting style, mood, and time of day · 视觉风格：设定配色、灯光、氛围和时段 |
| **🤖 Prompt Engineering** | Generate optimized prompts for AI video models with one click · 提示词工程：一键生成适配 AI 视频模型的优化提示词 |
| **📤 Export & Share** | Export complete shot list as text, markdown, or JSON · 导出分享：将完整镜头表导出为文本、Markdown 或 JSON |
| **💾 Auto-Save** | Browser local storage keeps your work safe · 自动保存：浏览器本地存储，工作永不丢失 |

### 🚀 Quick Start · 快速上手

1. Open the tool: [`shot-planner/index.html`](shot-planner/index.html) — just open in any modern browser, no server needed!
2. Click **"Add Scene"** to start building your shot list
3. Fill in scene details — location, time, mood, character actions
4. Configure shot parameters — camera angle, movement, framing, lens
5. Set visual style — color palette, lighting, atmosphere
6. Click **"Generate AI Prompt"** to create an optimized prompt
7. Export your complete shot list as Markdown or JSON

> **No installation required!** Runs entirely in the browser — pure HTML/CSS/JavaScript.

---

1. 打开工具：[`shot-planner/index.html`](shot-planner/index.html) — 直接在浏览器中打开即可，无需服务器！
2. 点击 **"添加场景"** 开始构建你的镜头列表
3. 填写场景详情 — 地点、时间、氛围、角色动作
4. 配置镜头参数 — 机位、运镜、景别、焦距
5. 设定视觉风格 — 配色、灯光、氛围
6. 点击 **"生成 AI 提示词"** 创建优化后的提示词
7. 将完整镜头表导出为 Markdown 或 JSON

> **无需安装！** 完全在浏览器中运行 — 纯 HTML/CSS/JavaScript。

---

## 🌍 Target Audience · 目标用户

- **AI Filmmakers** — directors producing AI-generated short films, music videos, and experimental cinema
- **Prompt Engineers** — creators who craft and optimize prompts for AI video models
- **Content Creators** — YouTubers, TikTokers, and social media creators using AI in their workflow
- **Independent Directors** — low-budget filmmakers leveraging AI for pre-visualization and storyboarding
- **Students & Educators** — film students learning AI production techniques

---

- **AI 影视创作者** — 制作 AI 短片、音乐视频和实验电影的导演
- **提示词工程师** — 为 AI 视频模型制作和优化提示词的创作者
- **内容创作者** — 在创作流程中使用 AI 的 YouTuber、TikToker 和社交媒体创作者
- **独立导演** — 利用 AI 进行预览和分镜的低预算电影人
- **学生与教育者** — 学习 AI 制作技术的电影专业学生

---

## 📂 Project Structure · 项目结构

```
ai-film-tools/
├── README.md               # This file · 本说明文件 (中文 + English)
├── LICENSE                 # MIT License · 开源许可证
├── .gitignore
├── .github/
│   └── FUNDING.yml         # Sponsorship configuration · 赞助配置
├── shot-planner/           # AI Film Shot Planner · AI电影镜头规划器
│   └── index.html          # The tool · 工具主文件
└── prompts/                # Prompt packs & templates (coming soon) · 提示词包与模板 (即将推出)
```

---

## 🛠️ Development · 开发指南

This project is built with **vanilla HTML/CSS/JavaScript** — no frameworks, no build tools, no dependencies. Contributions are welcome!

本项目使用 **纯 HTML/CSS/JavaScript** 构建 —— 无框架、无构建工具、无依赖。欢迎贡献代码！

### Getting Started · 开始开发

```bash
git clone https://github.com/your-username/ai-film-tools.git
cd ai-film-tools
# That's it! Open any HTML file in your browser.
# 就这么简单！在浏览器中打开任意 HTML 文件即可。
```

### Contributing · 贡献指南

1. Fork the repository · Fork 本仓库
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🤝 Sponsorship · 赞助支持

If these tools are valuable to your creative work, please consider supporting the project:

如果这些工具对你的创作有价值，请考虑支持本项目：

| Platform · 平台 | Link · 链接 |
|-----------------|-------------|
| 🌟 **GitHub Sponsors** | [github.com/sponsors/your-username](#) |
| ☕ **Buy Me a Coffee** | [buymeacoffee.com/aifilmtools](#) |
| 💳 **Stripe** | [One-time donation](#) |
| 🇨🇳 **爱发电** | [afdian.net](#) |

Your support helps us build more tools, improve documentation, and keep everything free and open-source.

你的支持将帮助我们开发更多工具、完善文档，并保持一切免费开源。

---

## 📜 License · 许可证

This project is **MIT licensed** — you are free to use, modify, and distribute it for any purpose, including commercial projects.

本项目采用 **MIT 许可证** —— 你可以自由使用、修改和分发，包括用于商业项目。

See [LICENSE](LICENSE) for details. · 详见 [LICENSE](LICENSE)。

---

## 📬 Contact · 联系

- **Issues**: [GitHub Issues](https://github.com/your-username/ai-film-tools/issues) — bug reports, feature requests
- **Discussions**: [GitHub Discussions](https://github.com/your-username/ai-film-tools/discussions) — community Q&A
- **Creator**: [@zhanggengxi](https://github.com/zhanggengxi)

---

<p align="center">
  <strong>🎬 Lights, Camera, AI! · 灯光，摄影，AI！</strong><br>
  Made with ❤️ for the AI filmmaking community<br>
  为 AI 影视制作社区用心打造
</p>
