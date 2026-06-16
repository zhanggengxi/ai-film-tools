#!/bin/bash
# Cloudflare Pages Manual Deploy Script
set -euo pipefail

test -x /usr/bin/wrangler || test -x /usr/local/bin/wrangler || command -v wrangler || { echo WRANGLER_NOT_FOUND; exit 1; }
cd "$(dirname "$0")/.."
echo Deploying ai-film-tools to Cloudflare Pages...
wrangler pages deploy . --project-name=ai-film-tools
echo Done