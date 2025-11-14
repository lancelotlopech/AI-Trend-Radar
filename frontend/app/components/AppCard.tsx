import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import Image from 'next/image';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { cn } from '../lib/utils';
import Link from 'next/link';

interface AppCardProps {
  appName: string;
  platform: string;
  rank: number;
  downloadChange: number | null;
  iconUrl: string | null;
  appUrl: string;
}

export default function AppCard({ appName, platform, rank, downloadChange, iconUrl, appUrl }: AppCardProps) {
  const isUp = downloadChange && downloadChange > 0;
  const isDown = downloadChange && downloadChange < 0;

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <div className="flex items-center space-x-2">
          {iconUrl && (
            <Image src={iconUrl} alt={appName} width={24} height={24} className="rounded-md" />
          )}
          <CardTitle className="text-base font-medium">{appName}</CardTitle>
        </div>
        {isUp && <ArrowUpRight className="h-4 w-4 text-green-500" />}
        {isDown && <ArrowDownRight className="h-4 w-4 text-red-500" />}
      </CardHeader>
      <CardContent>
        <div className="text-xl font-bold">#{rank} <span className="text-sm text-muted-foreground">({platform})</span></div>
        {downloadChange !== null && (
          <p className={cn(
            "text-xs",
            isUp ? "text-green-500" : isDown ? "text-red-500" : "text-muted-foreground"
          )}>
            {downloadChange > 0 ? '+' : ''}{downloadChange} changes
          </p>
        )}
        <Link href={appUrl} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:underline mt-2 block">
          View on {platform}
        </Link>
      </CardContent>
    </Card>
  );
}

