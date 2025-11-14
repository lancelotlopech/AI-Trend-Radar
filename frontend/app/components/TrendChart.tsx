// This component will be used in the trend detail page
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface TrendChartProps {
  data: Array<{
    timestamp: string;
    trend_score: number;
    google_trends_score?: number;
    reddit_score?: number;
    news_score?: number;
    app_score?: number;
  }>;
  title: string;
  description?: string;
}

export default function TrendChart({ data, title, description }: TrendChartProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <p className="text-sm text-muted-foreground">{description}</p>}
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart
            data={data}
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
            <Legend />
            <Line type="monotone" dataKey="trend_score" stroke="#8884d8" name="总趋势指数" activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="google_trends_score" stroke="#82ca9d" name="Google Trends" />
            <Line type="monotone" dataKey="reddit_score" stroke="#ffc658" name="Reddit 热度" />
            <Line type="monotone" dataKey="news_score" stroke="#ff7300" name="新闻热度" />
            <Line type="monotone" dataKey="app_score" stroke="#a4de6c" name="App 下载量变化" />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

