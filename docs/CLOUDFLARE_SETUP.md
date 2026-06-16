# ☁️ Cloudflare Pages 部署指南（5分钟搞定）

## 前提
- 代码已在 GitHub → `https://github.com/zhanggengxi/ai-film-tools`
- GitHub Actions 工作流已配置好（`.github/workflows/deploy-cloudflare.yml`）

---

## 操作步骤

### 第1步：注册 Cloudflare（如果还没有）

打开 https://dash.cloudflare.com/sign-up → 用邮箱注册

### 第2步：创建 API Token

1. 登录 Cloudflare → 右上角头像 → **My Profile** → **API Tokens**
2. 点 **Create Token**
3. 选 **Create Custom Token**
4. 名称填 `github-pages-deploy`
5. 权限：**Cloudflare Pages** → **Edit**
6. Account Resources → 选你的账号
7. 点 **Continue to summary** → **Create Token**
8. **复制 Token（只显示一次！）**

### 第3步：获取 Account ID

1. Cloudflare 首页 → 右侧 **Account ID**（一串字符）
2. 复制它

### 第4步：配置 GitHub Secrets

1. 打开 https://github.com/zhanggengxi/ai-film-tools/settings/secrets/actions
2. 点 **New repository secret**
3. 添加两个：

| Secret 名称 | 值 |
|:------------|:----|
| `CLOUDFLARE_API_TOKEN` | 第2步复制的 Token |
| `CLOUDFLARE_ACCOUNT_ID` | 第3步复制的 Account ID |

### 第5步：触发部署

只要推送代码到 main 分支，GitHub Actions 会自动部署到 Cloudflare Pages。

**部署完成后你的工具站在：**
```
https://ai-film-tools.pages.dev
（或你绑定的自定义域名）
```

---

## 完成后效果

| 当前 (GitHub Pages) | 部署后 (Cloudflare) |
|:--------------------|:--------------------|
| 国内访问慢/可能被墙 | ⚡ 国内速度快 |
| github.io 域名 | pages.dev 或自定义域名 |
| 手动部署 | ✅ 自动部署（推送即更新） |
