import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import TrendCard from './components/TrendCard';
import AppCard from './components/AppCard';
import RedditCard from './components/RedditCard';
import NewsCard from './components/NewsCard';
import { Button } from './components/ui/button';
import Link from 'next/link';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

async function getLatestTrends() {
  const res = await fetch(`${API_BASE_URL}/trends/latest?limit=10`, { next: { revalidate: 3600 } });
  if (!res.ok) {
    console.error("Failed to fetch trends", res.status, await res.text());
    return [];
  }
  return res.json();
}

async function getLatestApps() {
  const res = await fetch(`${API_BASE_URL}/apps/latest?limit=10`, { next: { revalidate: 3600 } });
  if (!res.ok) {
    console.error("Failed to fetch apps", res.status, await res.text());
    return [];
  }
  return res.json();
}

async function getLatestRedditPosts() {
  const res = await fetch(`${API_BASE_URL}/reddit/latest?limit=10`, { next: { revalidate: 3600 } });
  if (!res.ok) {
    console.error("Failed to fetch reddit posts", res.status, await res.text());
    return [];
  }
  return res.json();
}

async function getLatestNews() {
  const res = await fetch(`${API_BASE_URL}/news/latest?limit=10`, { next: { revalidate: 3600 } });
  if (!res.ok) {
    console.error("Failed to fetch news", res.status, await res.text());
    return [];
  }
  return res.json();
}


export default async function HomePage() {
  const [trends, apps, redditPosts, newsArticles] = await Promise.all([
    getLatestTrends(),
    getLatestApps(),
    getLatestRedditPosts(),
    getLatestNews(),
  ]);

  return (
    <div className="space-y-8">
      <section className="text-center">
        <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">
          AI Trend Radar
        </h1>
        <p className="mt-4 text-xl text-muted-foreground">
          实时洞察AI热点关键词、应用趋势、社交讨论与新闻动态
        </p>
      </section>

      <Tabs defaultValue="trends" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="trends">AI热榜</TabsTrigger>
          <TabsTrigger value="apps">应用榜</TabsTrigger>
          <TabsTrigger value="social">社交热度</TabsTrigger>
          <TabsTrigger value="news">新闻 & 新品</TabsTrigger>
        </TabsList>

        <TabsContent value="trends" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>AI 热点关键词榜</CardTitle>
              <CardDescription>根据综合趋势指数实时更新</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {trends.map((trend: any) => (
                  <TrendCard
                    key={trend.id}
                    keyword={trend.keyword?.keyword || '未知关键词'}
                    trendScore={trend.trend_score}
                    change={5.2}
                    keywordId={trend.keyword_id}
                  />
                ))}
              </div>
              <div className="flex justify-end mt-4">
                <Button variant="outline" asChild>
                  <Link href="/trends">查看更多</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="apps" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>AI 应用榜单</CardTitle>
              <CardDescription>App Store / Play Store 热门AI应用</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {apps.map((app: any) => (
                  <AppCard
                    key={app.id}
                    appName={app.app_name}
                    platform={app.store_platform}
                    rank={app.current_rank}
                    downloadChange={app.download_change}
                    iconUrl={app.icon_url}
                    appUrl={app.app_url}
                  />
                ))}
              </div>
              <div className="flex justify-end mt-4">
                <Button variant="outline" asChild>
                  <Link href="/apps">查看更多</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="social" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>社交媒体热度榜</CardTitle>
              <CardDescription>Reddit 热门讨论与关键词</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {redditPosts.map((post: any) => (
                  <RedditCard
                    key={post.id}
                    title={post.title}
                    subreddit={post.subreddit}
                    score={post.score}
                    numComments={post.num_comments}
                    url={post.url}
                  />
                ))}
              </div>
              <div className="flex justify-end mt-4">
                <Button variant="outline" asChild>
                  <Link href="/reddit">查看更多</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="news" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>AI 新闻 & 新品</CardTitle>
              <CardDescription>最新AI行业动态与产品发布</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {newsArticles.map((article: any) => (
                  <NewsCard
                    key={article.id}
                    title={article.title}
                    source={article.source}
                    summary={article.summary}
                    url={article.url}
                    publishedAt={article.published_at}
                  />
                ))}
              </div>
              <div className="flex justify-end mt-4">
                <Button variant="outline" asChild>
                  <Link href="/news">查看更多</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

