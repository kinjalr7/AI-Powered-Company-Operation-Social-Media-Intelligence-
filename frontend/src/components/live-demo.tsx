'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown, Users, MessageCircle, Heart, Share } from 'lucide-react';

interface DemoData {
  sentiment: {
    positive: number;
    neutral: number;
    negative: number;
  };
  posts: number;
  engagement: number;
  trend: 'up' | 'down' | 'stable';
}

export function LiveDemo() {
  const [data, setData] = useState<DemoData>({
    sentiment: { positive: 65, neutral: 25, negative: 10 },
    posts: 1247,
    engagement: 8920,
    trend: 'up'
  });

  const [isLive, setIsLive] = useState(true);

  useEffect(() => {
    if (!isLive) return;

    const interval = setInterval(() => {
      setData(prev => ({
        sentiment: {
          positive: Math.max(50, Math.min(80, prev.sentiment.positive + (Math.random() - 0.5) * 5)),
          neutral: Math.max(15, Math.min(35, prev.sentiment.neutral + (Math.random() - 0.5) * 3)),
          negative: Math.max(5, Math.min(20, prev.sentiment.negative + (Math.random() - 0.5) * 2))
        },
        posts: prev.posts + Math.floor(Math.random() * 5),
        engagement: prev.engagement + Math.floor(Math.random() * 20),
        trend: Math.random() > 0.7 ? (prev.trend === 'up' ? 'down' : 'up') : prev.trend
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, [isLive]);

  const totalSentiment = data.sentiment.positive + data.sentiment.neutral + data.sentiment.negative;

  return (
    <div className="space-y-6">
      {/* Live Status */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${isLive ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
          <span className="text-sm text-slate-300">
            {isLive ? 'Live Demo' : 'Demo Paused'}
          </span>
        </div>
        <button
          onClick={() => setIsLive(!isLive)}
          className="px-3 py-1 text-xs bg-slate-700 hover:bg-slate-600 rounded-md transition-colors"
        >
          {isLive ? 'Pause' : 'Resume'}
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-300">Total Posts</CardTitle>
            <MessageCircle className="h-4 w-4 text-blue-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{data.posts.toLocaleString()}</div>
            <div className="flex items-center space-x-1 text-xs text-slate-400">
              <TrendingUp className="h-3 w-3" />
              <span>+12% from last hour</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-300">Engagement</CardTitle>
            <Heart className="h-4 w-4 text-red-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{data.engagement.toLocaleString()}</div>
            <div className="flex items-center space-x-1 text-xs text-slate-400">
              <TrendingUp className="h-3 w-3" />
              <span>+8% from last hour</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-300">Sentiment Trend</CardTitle>
            {data.trend === 'up' ? (
              <TrendingUp className="h-4 w-4 text-green-400" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-400" />
            )}
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white capitalize">{data.trend}</div>
            <div className="text-xs text-slate-400">Overall sentiment</div>
          </CardContent>
        </Card>
      </div>

      {/* Sentiment Breakdown */}
      <Card className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/30">
        <CardHeader>
          <CardTitle className="text-white">Sentiment Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-500 rounded-full" />
                <span className="text-sm text-slate-300">Positive</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-white font-medium">{data.sentiment.positive.toFixed(1)}%</span>
                <div className="w-20 bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-green-500 h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${(data.sentiment.positive / totalSentiment) * 100}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-yellow-500 rounded-full" />
                <span className="text-sm text-slate-300">Neutral</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-white font-medium">{data.sentiment.neutral.toFixed(1)}%</span>
                <div className="w-20 bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-yellow-500 h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${(data.sentiment.neutral / totalSentiment) * 100}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full" />
                <span className="text-sm text-slate-300">Negative</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-white font-medium">{data.sentiment.negative.toFixed(1)}%</span>
                <div className="w-20 bg-slate-700 rounded-full h-2">
                  <div
                    className="bg-red-500 h-2 rounded-full transition-all duration-1000"
                    style={{ width: `${(data.sentiment.negative / totalSentiment) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <Card className="bg-slate-800/50 backdrop-blur-lg border border-slate-700/30">
        <CardHeader>
          <CardTitle className="text-white">Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { time: '2 min ago', action: 'New post detected', platform: 'Twitter', sentiment: 'positive' },
              { time: '5 min ago', action: 'Sentiment alert', platform: 'LinkedIn', sentiment: 'negative' },
              { time: '8 min ago', action: 'High engagement post', platform: 'Instagram', sentiment: 'positive' },
              { time: '12 min ago', action: 'New follower surge', platform: 'Twitter', sentiment: 'neutral' }
            ].map((activity, index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-slate-700/30 last:border-b-0">
                <div className="flex items-center space-x-3">
                  <Badge
                    variant={activity.sentiment === 'positive' ? 'default' : activity.sentiment === 'negative' ? 'destructive' : 'secondary'}
                    className="text-xs"
                  >
                    {activity.sentiment}
                  </Badge>
                  <div>
                    <p className="text-sm text-white">{activity.action}</p>
                    <p className="text-xs text-slate-400">{activity.platform}</p>
                  </div>
                </div>
                <span className="text-xs text-slate-500">{activity.time}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}