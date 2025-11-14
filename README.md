# AI Trend Radar

AI Trend Radar 是一个展示最新 AI 热点关键词、AI 应用下载趋势、社交媒体讨论热度、新闻和新品趋势的网站。它自动计算综合趋势指数（Trend Score），并提供榜单和可视化页面。

## 目标

*   MVP 可直接运行的 AI 热点趋势网站。
*   可视化首页展示热门关键词、APP、社交讨论和新闻。
*   自动更新趋势指数和榜单。
*   结构清晰，方便迭代和扩展。

## 技术栈

*   **前端**: Next.js (App Router) + React + TypeScript + shadcn/ui + Tailwind CSS
*   **后端**: FastAPI + Pydantic + SQLAlchemy + Python
*   **数据库**: Supabase (PostgreSQL)
*   **定时任务**: Cron (通过 Railway Cron / Vercel Cron 部署)
*   **爬虫**: Python (httpx, BeautifulSoup, pytrends, praw, feedparser)
*   **部署**:
    *   前端: Vercel
    *   后端: Railway / Vercel Serverless Functions
    *   定时任务: Railway Cron / Vercel Cron (或独立服务器上的 `cron`)

## 功能模块

1.  **关键词热榜**: 综合 Google Trends / AI 平台 / RSS 获取热门 AI 关键词。
2.  **AI 应用榜单**: 抓取 App Store / Play Store 免费榜单或 API，显示下载量及变化趋势。
3.  **社交热度榜**: 抓取 Reddit r/ArtificialIntelligence、r/ChatGPT 热帖，提取关键词和讨论量。
4.  **新闻 & 新品**: 抓取 AI 相关新闻 RSS + Product Hunt / HackerNews AI 标签，自动生成摘要。
5.  **趋势指数计算**: 综合各数据源，计算 0–100 的 AI Trend Score。
6.  **前端页面**: 首页显示各榜单，可搜索、分页、趋势折线图。详细页展示单条关键词 / APP / 热点的历史趋势。
7.  **数据库设计**: Supabase，存储 keywords、trends、reddit_posts、news、trend_score、timestamp。
8.  **API**: RESTful，提供 `/api/trends`、`/api/apps`、`/api/reddit`、`/api/news`。
9.  **定时更新**: 每小时抓取数据并更新趋势指数。

## 项目启动步骤

### 1. 数据库设置 (Supabase)

1.  在 Supabase 创建新项目。
2.  获取你的 `DATABASE_URL` (可在项目设置 -> Database -> Connection string 中找到)。
3.  在 Supabase SQL Editor 中运行 `scripts/setup_database.sql` 中的所有 SQL 语句，创建所需的表和策略。

### 2. 后端 (FastAPI)

1.  克隆项目仓库：
    ```bash
    git clone https://github.com/your-username/AI-Trend-Radar.git
    cd AI-Trend-Radar/backend
    ```
2.  创建并激活虚拟环境：
    ```bash
    python -m venv venv
    source venv/bin/activate # macOS/Linux
    # venv\Scripts\activate # Windows
    ```
3.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
4.  创建 `.env` 文件并配置数据库连接字符串：
    ```
    # backend/.env
    DATABASE_URL="postgresql://postgres:[YOUR_PASSWORD]@db.[YOUR_SUPABASE_PROJECT_REF].supabase.co:5432/postgres"
    # 或者 Supabase 提供的完整连接字符串
    ```
5.  运行后端服务：
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    后端将在 `http://localhost:8000` 运行。API 文档可在 `http://localhost:8000/docs` 查看。

### 3. 爬虫和定时任务 (Workers)

1.  进入 `workers` 目录：
    ```bash
    cd ../workers
    ```
2.  安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
3.  创建 `.env` 文件并配置数据库连接字符串及各爬虫的 API 密钥：
    ```
    # workers/.env
    DATABASE_URL="postgresql://postgres:[YOUR_PASSWORD]@db.[YOUR_SUPABASE_PROJECT_REF].supabase.co:5432/postgres"
    GOOGLE_TRENDS_USERNAME="your_google_username"
    GOOGLE_TRENDS_PASSWORD="your_google_password"
    REDDIT_CLIENT_ID="your_reddit_client_id"
    REDDIT_CLIENT_SECRET="your_reddit_client_secret"
    REDDIT_USER_AGENT="AITrendRadarBot by /u/YourRedditUsername"
    # OPENAI_API_KEY="your_openai_api_key" # 如果使用LangChain
    ```
4.  手动运行爬虫和计算器进行测试：
    ```bash
    python main.py
    ```
5.  部署到 Railway Cron 或配置你自己的 `crontab` 以每小时自动运行。

### 4. 前端 (Next.js)

1.  进入 `frontend` 目录：
    ```bash
    cd ../frontend
    ```
2.  安装依赖：
    ```bash
    npm install
    # 或 yarn install
    ```
3.  配置 shadcn/ui (如果尚未配置)：
    ```bash
    npx shadcn-ui@latest init
    ```
4.  添加所需的 shadcn/ui 组件 (例如 `button`, `card`, `tabs`, `skeleton`)：
    ```bash
    npx shadcn-ui@latest add button card tabs skeleton
    ```
5.  创建 `.env.local` 文件并配置后端 API 地址：
    ```
    # frontend/.env.local
    NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api" # 本地开发时
    # 部署时替换为您的后端API的公共URL，例如：https://your-fastapi-app.railway.app/api
    ```
6.  运行前端开发服务器：
    ```bash
    npm run dev
    # 或 yarn dev
    ```
    Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## API 调用示例

### 获取最新AI趋势

```bash
curl http://localhost:8000/api/trends/latest
```

### 获取关键词历史趋势 (替换 `keyword_id` 为实际UUID)

```bash
curl http://localhost:8000/api/trends/a1b2c3d4-e5f6-7890-1234-567890abcdef/history?days=7
```

### 获取最新AI应用榜单

```bash
curl http://localhost:8000/api/apps/latest
```

### 获取最新Reddit热门帖子

```bash
curl http://localhost:8000/api/reddit/latest
```

### 获取最新AI新闻和新品

```bash
curl http://localhost:8000/api/news/latest
```

## 数据源说明

*   **Google Trends**: 使用 `pytrends` 库抓取 Google Trends 实时搜索热度。
*   **App Store / Play Store**: 通过网页抓取或第三方 API 获取应用榜单数据。（请注意：应用商店爬虫可能受限于反爬策略，需要更 robust 的实现）。
*   **Reddit**: 使用 `PRAW` (Python Reddit API Wrapper) 访问 Reddit API 获取热门帖子。
*   **新闻 & 新品**:
    *   **RSS Feed**: 抓取预设的 AI 相关新闻 RSS 源。
    *   **Product Hunt / HackerNews**: 同样可以通过网页抓取或其提供的 API 获取相关信息。

## 部署

### 前端 (Vercel)

1.  将 `frontend` 目录推送到 GitHub/GitLab/Bitbucket 仓库。
2.  登录 Vercel，导入项目，选择 `frontend` 目录作为根目录。
3.  配置环境变量 `NEXT_PUBLIC_API_BASE_URL` 为您部署的 FastAPI 后端的公共 URL。
4.  Vercel 将自动构建并部署您的 Next.js 应用。

### 后端 (Railway)

1.  将 `backend` 目录推送到 GitHub/GitLab/Bitbucket 仓库。
2.  登录 Railway，新建项目，连接您的仓库。
3.  选择 `backend` 目录，Railway 会自动检测为 Python 项目。
4.  配置环境变量 `DATABASE_URL` (来自 Supabase)。
5.  确保 `requirements.txt` 和 `Dockerfile` (可选) 正确。
6.  Railway 将自动部署您的 FastAPI 应用。

### 定时任务 (Railway Cron / Vercel Cron)

*   **Railway Cron**: 在 Railway 项目中添加 `Cron Job` 服务，并配置命令为 `python /app/workers/main.py` (确保路径正确)。
*   **Vercel Cron**: 对于 Vercel Cron，您可以在 Next.js 项目中创建一个 API 路由 (例如 `/api/cron/trigger`)，该路由负责向您的 Railway 后端或一个独立的 Worker 服务发送请求，触发数据抓取和计算。
    *   例如，在 `frontend/app/api/cron/trigger/route.ts` 中：
        ```typescript
        // frontend/app/api/cron/trigger/route.ts
        export async function GET() {
          const workerUrl = process.env.WORKER_SERVICE_URL; // 部署在Railway的Worker服务的URL
          if (!workerUrl) {
            return new Response("Worker service URL not configured", { status: 500 });
          }
          try {
            const response = await fetch(workerUrl + '/run-tasks', { method: 'POST' }); // 假设Worker服务有一个/run-tasks接口
            if (!response.ok) {
              throw new Error(`Worker service failed: ${response.statusText}`);
            }
            const data = await response.json();
            return new Response(JSON.stringify(data), { status: 200 });
          } catch (error: any) {
            return new Response(`Error triggering worker: ${error.message}`, { status: 500 });
          }
        }
        ```
    *   然后在 Vercel Cron 配置中，每小时触发 `/api/cron/trigger`。
    *   这意味着你的 `workers/main.py` 脚本需要包装成一个简单的 FastAPI 应用，提供 `/run-tasks` 接口供 Vercel Cron 调用。

