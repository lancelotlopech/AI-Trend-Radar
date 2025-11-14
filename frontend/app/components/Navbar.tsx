import Link from 'next/link';
import { BrainCircuit } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="border-b">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <BrainCircuit className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold text-foreground">AI Trend Radar</span>
        </Link>
        <div className="space-x-4">
          <Link href="/trends" className="text-muted-foreground hover:text-primary transition-colors">
            趋势榜
          </Link>
          <Link href="/apps" className="text-muted-foreground hover:text-primary transition-colors">
            应用榜
          </Link>
          <Link href="/news" className="text-muted-foreground hover:text-primary transition-colors">
            新闻/新品
          </Link>
        </div>
      </div>
    </nav>
  );
}

