import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './styles/globals.css';
import { cn } from './lib/utils';
import Navbar from './components/Navbar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AI Trend Radar - 实时洞察AI热点',
  description: '展示最新的AI热点关键词、AI应用下载趋势、社交媒体讨论热度、新闻和新品趋势。',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body
        className={cn(
          'min-h-screen bg-background font-sans antialiased',
          inter.className
        )}
      >
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}

