import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Newspaper } from 'lucide-react';
import Link from 'next/link';
import { format } from 'date-fns';

interface NewsCardProps {
  title: string;
  source: string;
  summary: string | null;
  url: string;
  publishedAt: string | null;
}

export default function NewsCard({ title, source, summary, url, publishedAt }: NewsCardProps) {
  const formattedDate = publishedAt ? format(new Date(publishedAt), 'yyyy-MM-dd HH:mm') : '未知时间';

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle className="text-base font-medium">
          <Link href={url} target="_blank" rel="noopener noreferrer" className="hover:underline">
            {title}
          </Link>
        </CardTitle>
        <CardDescription className="flex items-center space-x-1 text-sm text-muted-foreground">
          <Newspaper className="h-4 w-4" />
          <span>{source}</span>
          <span>•</span>
          <span>{formattedDate}</span>
        </CardDescription>
      </CardHeader>
      {summary && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-3">
            {summary}
          </p>
        </CardContent>
      )}
    </Card>
  );
}

