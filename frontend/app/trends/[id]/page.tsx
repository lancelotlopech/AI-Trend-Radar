'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';
import { Skeleton } from '../../components/ui/skeleton';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

interface TrendHistoryData {
  timestamp: string;
  trend_score: number;
  google_trends_score?: number;
  reddit_score?: number;
  news_score?: number;
  app_score?: number;
}

export default function TrendDetailPage() {
  const params = useParams();
  const keywordId = params.id as string;
  const [history, setHistory] = useState<TrendHistoryData[]>([]);
  const [keywordName, setKeywordName] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const keywordRes = await fetch(`${API_BASE_URL}/trends/keywords`);
        if (!keywordRes.ok) throw new Error('Failed to fetch keywords');
        const keywords = await keywordRes.json();
        const currentKeyword = keywords.find((kw: any) => kw.id === keywordId);
        setKeywordName(currentKeyword?.keyword || '未知关键词');

        const historyRes = await fetch(`${API_BASE_URL}/trends/${keywordId}/history?days=30`);
        if (!historyRes.ok) throw new Error('Failed to fetch trend history');
        const data: TrendHistoryData[] = await historyRes.json();
        setHistory(data.map(item => ({
          ...item,
          timestamp: format(new Date(item.timestamp), 'MM-dd HH:00')
        })));
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [keywordId]);

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-3/4" />
        <Skeleton className="h-6 w-1/2" />
        <Card className="p-6">
          <Skeleton className="h-[400px] w-full" />
        </Card>
      </div>
    );
  }

  if (error) {
    return <div className="text-red-500">Error: {error}</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-4xl font-bold">{keywordName} 趋势详情</h1>
      <Card>
        <CardHeader>
          <CardTitle>趋势指数历史 ({keywordName})</CardTitle>
          <CardDescription>近30天趋势指数变化</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart
              data={history}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Line type="monotone" dataKey="trend_score" stroke="#8884d8" name="总趋势指数" activeDot={{ r: 8 }} />
              <Line type="monotone" dataKey="google_trends_score" stroke="#82ca9d" name="Google Trends" />
              <Line type="monotone" dataKey="reddit_score" stroke="#ffc658" name="Reddit 热度" />
              <Line type="monotone" dataKey="news_score" stroke="#ff7300" name="新闻热度" />
              <Line type="monotone" dataKey="app_score" stroke="#a4de6c" name="App 下载量变化" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}

