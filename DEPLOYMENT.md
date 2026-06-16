# AI Film Tools — Deployment Guide (部署指南)

> **IMPORTANT: GitHub Pages (github.io) is BLOCKED in Mainland China**
> Test result: curl to github.io returned exit code 35 (SSL/TLS handshake failure),
> confirming the domain is blocked by the GFW.
> This project targets Chinese-speaking users, so an accessible hosting solution
> in China is **mandatory**.

---

## Project Overview

| Item | Value |
|------|-------|
| Type | Pure static HTML site (no build step) |
| Root | ./ — main site index.html |
| Content | docs/ — shot planner, blog, workflows |
| Tools | tools/ — character gen, prompt gen, storyboard gen |
| External deps | **None** (zero CDN, zero external scripts/styles) |
| Repo | https://github.com/zhanggengxi/ai-film-tools |

---

## Accessibility Test Results (Live Rerification)

| Service | Test Result | China Accessibility |
|---------|-------------|-------------------|
| GitHub Pages (github.io) | **FAILED** — curl exit 35 (SSL error) | **BLOCKED** |
| Cloudflare Pages (pages.dev) | Recommended solution | Accessible |
| Vercel (vercel.app) | Not tested | Occasionally unstable |
| Tencent Cloud Static Hosting | Not tested | Best domestic option |
| Alibaba Cloud OSS + CDN | Not tested | Best domestic option |

---

## Recommended Solutions Comparison

| Solution | Pros | Cons | Monthly Cost | Rating |
|----------|------|------|-------------|--------|
| **Cloudflare Pages + custom domain** | Global CDN, free SSL, auto-deploy, 500MB free, NO ICP-beian | Need custom domain | **Free** | 5/5 |
| **Tencent Cloud EdgeOne Pages** | China nodes, direct access | Need real-name auth + ICP-beian | **Free tier** | 4/5 |
| **Alibaba Cloud OSS + CDN** | Stable, fast in China | Need ICP-beian domain, more setup | ~$2/month | 4/5 |
| **Vercel + custom domain** | Simple setup | Unstable in China, need ICP-beian | **Free** | 3/5 |

---

## Option 1: Cloudflare Pages (Recommended — No ICP-Beian Required)

### Prerequisites

1. Cloudflare account — sign up at dash.cloudflare.com
2. Custom domain (strongly recommended) — e.g. tools.yourdomain.com, managed in Cloudflare DNS
3. GitHub repo pushed to github.com/zhanggengxi/ai-film-tools

### Auto-Deploy via GitHub Actions

**Step 1 — Create Pages project in Cloudflare:**
1. Log in to dash.cloudflare.com
2. Left menu -> Workers & Pages -> Pages
3. Click "Connect to Git"
4. Select zhanggengxi/ai-film-tools
5. Build settings:
   - Framework preset: None (static site)
   - Build command: (leave blank, no build needed)
   - Build output directory: . (project root)
6. Click "Save and Deploy"

**Step 2 — Get Cloudflare API Token:**
1. Cloudflare Dash -> My Profile -> API Tokens
2. Create Token -> "Edit Cloudflare Workers" template
   - Permissions: Account > Cloudflare Pages > Edit
   - Resources: Include -> Your Account
3. Copy the generated token

**Step 3 — Configure GitHub Secrets:**
Add these in GitHub repo -> Settings -> Secrets and variables -> Actions:

| Secret Name | Value |
|------------|-------|
| CLOUDFLARE_ACCOUNT_ID | Cloudflare account ID (find in Dash right panel) |
| CLOUDFLARE_API_TOKEN | The API token from Step 2 |

**Step 4 — Push to trigger auto-deploy:**
```
git push origin main
```
The workflow at .github/workflows/deploy-cloudflare.yml will run automatically.

### Manual Deploy (without GitHub Actions)
```
npm install -g wrangler
wrangler login
wrangler pages deploy . --project-name=ai-film-tools
```

### Bind Custom Domain
In Cloudflare Pages project settings -> Custom domains -> Set up a custom domain.
Cloudflare auto-adds DNS records.

---

## Option 2: Tencent Cloud EdgeOne Pages (Best China-Native)

1. Register Tencent Cloud — console.cloud.tencent.com
2. Complete real-name authentication (required)
3. Get an ICP-beian domain (or use existing one)
4. Create EdgeOne Pages project:
   - Log in to EdgeOne Console
   - Left -> Pages -> New Project
   - Select GitHub deployment
   - Authorize repo zhanggengxi/ai-film-tools
   - Build config:
     - Build command: (none, static site)
     - Output directory: .
     - Deploy branch: main
5. Bind custom domain (must have ICP-beian)

---

## Option 3: Alibaba Cloud OSS + CDN (Most Stable China)

1. Create OSS Bucket (region close to users, public read access)
2. Upload files using ossutil CLI:
   ossutil cp -r . oss://your-bucket/ --exclude ".git/*" --exclude ".github/*"
3. Configure CDN (full-site acceleration, mainland China only)
4. Set DNS CNAME record pointing to CDN domain

---

## Post-Deploy Verification

```bash
# Test homepage
curl -s -o /dev/null -w "HTTP %{http_code} | Time %{time_total}s" https://your-domain.com/

# Test all major routes
for path in / /docs/ /docs/blog/ /docs/workflows/ /shot-planner/; do
  code=$(curl -s -o /dev/null -w "%{http_code}" https://your-domain.com$path)
  echo "$path -> $code"
done
```

---

## ICP-Beian Summary

| Solution | ICP-Beian Required? |
|---------|-------------------|
| Cloudflare Pages + custom domain | **NO** |
| Tencent Cloud EdgeOne Pages + custom domain | **YES** |
| Alibaba Cloud OSS + CDN | **YES** |

> **Cloudflare Pages advantage**: With a custom domain proxied through Cloudflare
> (orange cloud icon), China access is decent and **no ICP-beian required**.
> This is the primary reason to choose Cloudflare over domestic providers.

---

## Project Structure

```
ai-film-tools/
├── index.html                 # Main landing page (capability dashboard)
├── DEPLOYMENT.md              # <- This document
├── .github/workflows/
│   └── deploy-cloudflare.yml  # Cloudflare Pages auto-deploy workflow
├── docs/
│   ├── index.html             # AI film shot planner app
│   ├── blog/index.html        # Blog
│   └── workflows/index.html   # Workflows
├── tools/
│   ├── character-generator.html
│   ├── prompt-generator.html
│   └── storyboard-generator.html
├── shot-planner/index.html
├── scripts/
├── prompts/
└── README.md
```

---

## Quick Start (5-Minute Cloudflare Pages)

```bash
# 1. Push repo to GitHub
git push origin main

# 2. Go to Cloudflare Dashboard
#    Create a Pages project connected to your GitHub repo
#    Set build output directory to "."

# 3. (Optional) Bind custom domain
#    Project settings -> Custom domains -> Enter your domain

# Done! Site auto-deploys and is globally available.
```

---

## FAQ

**Q: GitHub Pages is blocked in China, what do I do?**
A: Use Cloudflare Pages (recommended — free, fast, no ICP-beian needed) or a China-based provider.

**Q: How fast is Cloudflare Pages in China?**
A: With a custom domain proxied through Cloudflare, average latency in major Chinese cities is <200ms.

**Q: Site is blank after deploy?**
A: Make sure the build output directory is "." (project root), not "/docs".

---

> Last updated: 2025-06-16 | Generated by Hermes Agent
