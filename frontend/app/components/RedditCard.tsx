import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { MessageSquare, ThumbsUp } from 'lucide-react';
import Link from 'next/link';

interface RedditCardProps {
  title: string;
  subreddit: string;
  score: number;
  numComments: number;
  url: string;
}

export default function RedditCard({ title, subreddit, score, numComments, url }: RedditCardProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle className="text-base font-medium">
          <Link href={url} target="_blank" rel="noopener noreferrer" className="hover:underline">
            {title}
          </Link>
        </CardTitle>
        <CardDescription className="text-sm text-muted-foreground">r/{subreddit}</CardDescription>
      </CardHeader>
      <CardContent className="flex items-center justify-between">
        <div className="flex items-center space-x-1 text-sm text-muted-foreground">
          <ThumbsUp className="h-4 w-4" />
          <span>{score}</span>
        </div>
        <div className="flex items-center space-x-1 text-sm text-muted-foreground">
          <MessageSquare className="h-4 w-4" />
          <span>{numComments}</span>
        </div>
      </CardContent>
    </Card>
  );
}

