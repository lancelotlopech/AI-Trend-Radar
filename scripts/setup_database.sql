-- 1. `keywords` table: 存储所有追踪的AI关键词
CREATE TABLE public.keywords (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. `trend_scores` table: 存储每日或每小时的综合趋势指数
CREATE TABLE public.trend_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword_id UUID REFERENCES public.keywords(id) ON DELETE CASCADE,
    trend_score NUMERIC(5, 2) NOT NULL, -- 0-100
    google_trends_score NUMERIC(5, 2),
    reddit_score NUMERIC(5, 2),
    news_score NUMERIC(5, 2),
    app_score NUMERIC(5, 2),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_keyword_timestamp UNIQUE (keyword_id, timestamp)
);

-- 3. `app_trends` table: 存储AI应用下载趋势
CREATE TABLE public.app_trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    app_name TEXT NOT NULL,
    store_platform TEXT NOT NULL, -- 'App Store', 'Play Store'
    category TEXT,
    current_rank INT,
    download_change INT, -- 比如日下载量变化
    icon_url TEXT,
    app_url TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_app_platform_timestamp UNIQUE (app_name, store_platform, timestamp)
);

-- 4. `reddit_posts` table: 存储Reddit热门帖子数据
CREATE TABLE public.reddit_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id TEXT NOT NULL UNIQUE,
    subreddit TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    score INT,
    num_comments INT,
    created_utc TIMESTAMP WITH TIME ZONE,
    extracted_keywords TEXT[], -- 提取出的关键词
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. `news_articles` table: 存储AI相关新闻和新品发布
CREATE TABLE public.news_articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL, -- e.g., 'Product Hunt', 'HackerNews', 'RSS Feed Name'
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    published_at TIMESTAMP WITH TIME ZONE,
    summary TEXT,
    image_url TEXT,
    extracted_keywords TEXT[],
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. RLS (Row Level Security) 配置
ALTER TABLE public.keywords ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trend_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.app_trends ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reddit_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.news_articles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON public.keywords FOR SELECT USING (TRUE);
CREATE POLICY "Enable read access for all users" ON public.trend_scores FOR SELECT USING (TRUE);
CREATE POLICY "Enable read access for all users" ON public.app_trends FOR SELECT USING (TRUE);
CREATE POLICY "Enable read access for all users" ON public.reddit_posts FOR SELECT USING (TRUE);
CREATE POLICY "Enable read access for all users" ON public.news_articles FOR SELECT USING (TRUE);

-- 索引 (优化查询性能)
CREATE INDEX idx_keywords_keyword ON public.keywords(keyword);
CREATE INDEX idx_trend_scores_timestamp ON public.trend_scores(timestamp);
CREATE INDEX idx_trend_scores_keyword_id ON public.trend_scores(keyword_id);
CREATE INDEX idx_app_trends_timestamp ON public.app_trends(timestamp);
CREATE INDEX idx_reddit_posts_timestamp ON public.reddit_posts(timestamp);
CREATE INDEX idx_news_articles_timestamp ON public.news_articles(timestamp);

