import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ArrowUpRight, ArrowDownRight, TrendingUp } from 'lucide-react';
import { cn } from '../lib/utils';
import Link from 'next/link';

interface TrendCardProps {
  keyword: string;
  trendScore: number;
  change: number;
  keywordId: string;
}

export default function TrendCard({ keyword, trendScore, change, keywordId }: TrendCardProps) {
  const isUp = change > 0;
  const isDown = change < 0;

  return (
    <Link href={`/trends/${keywordId}`}>
      <Card className="hover:shadow-lg transition-shadow cursor-pointer">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{keyword}</CardTitle>
          {isUp && <ArrowUpRight className="h-4 w-4 text-green-500" />}
          {isDown && <ArrowDownRight className="h-4 w-4 text-red-500" />}
          {!isUp && !isDown && <TrendingUp className="h-4 w-4 text-muted-foreground" />}
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{trendScore.toFixed(2)}</div>
          <p className={cn(
            "text-xs",
            isUp ? "text-green-500" : isDown ? "text-red-500" : "text-muted-foreground"
          )}>
            {change > 0 ? '+' : ''}{change.toFixed(2)}% Compared to last hour
          </p>
        </CardContent>
      </Card>
    </Link>
  );
}

