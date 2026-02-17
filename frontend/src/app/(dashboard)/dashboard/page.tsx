"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BarChart3,
  TrendingUp,
  Users,
  MessageCircle,
  Heart,
  Share2,
  Eye,
  AlertTriangle,
  RefreshCw,
  Settings,
  Download,
  Calendar,
  Zap,
  User,
  Sparkles,
  Mail,
  Moon,
  Sun
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  Area,
  AreaChart
} from 'recharts';
import { toast } from "sonner";

// Mock data for demonstration
const mockRealtimeData = {
  totalPosts: 1247,
  totalEngagement: 45632,
  sentimentDistribution: {
    positive: 65,
    neutral: 25,
    negative: 10
  },
  platformStats: [
    { name: 'Twitter', posts: 523, engagement: 18234, color: '#1DA1F2' },
    { name: 'LinkedIn', posts: 324, engagement: 15234, color: '#0077B5' },
    { name: 'Facebook', posts: 267, engagement: 9876, color: '#1877F2' },
    { name: 'Instagram', posts: 133, engagement: 2288, color: '#E4405F' }
  ],
  recentPosts: [
    {
      id: 1,
      platform: 'Twitter',
      content: 'Excited about the new AI developments in our industry! #AI #Tech',
      sentiment: 'positive',
      engagement: 234,
      timestamp: '2 minutes ago'
    },
    {
      id: 2,
      platform: 'LinkedIn',
      content: 'Great insights on machine learning applications in business intelligence',
      sentiment: 'positive',
      engagement: 89,
      timestamp: '5 minutes ago'
    },
    {
      id: 3,
      platform: 'Twitter',
      content: 'Concerned about data privacy issues with new regulations',
      sentiment: 'negative',
      engagement: 156,
      timestamp: '8 minutes ago'
    }
  ],
  sentimentTrend: [
    { time: '00:00', positive: 45, neutral: 30, negative: 25 },
    { time: '04:00', positive: 52, neutral: 28, negative: 20 },
    { time: '08:00', positive: 48, neutral: 32, negative: 20 },
    { time: '12:00', positive: 61, neutral: 25, negative: 14 },
    { time: '16:00', positive: 58, neutral: 27, negative: 15 },
    { time: '20:00', positive: 63, neutral: 22, negative: 15 },
    { time: 'Now', positive: 65, neutral: 25, negative: 10 }
  ],
  topTopics: [
    { topic: 'AI Technology', mentions: 234, sentiment: 0.8 },
    { topic: 'Machine Learning', mentions: 189, sentiment: 0.7 },
    { topic: 'Data Privacy', mentions: 156, sentiment: -0.3 },
    { topic: 'Business Intelligence', mentions: 143, sentiment: 0.6 },
    { topic: 'Innovation', mentions: 98, sentiment: 0.9 }
  ]
};

const COLORS = ['#3b82f6', '#06b6d4', '#8b5cf6', '#f59e0b', '#ef4444', '#10b981', '#ec4899'];

export default function DashboardPage() {
  const [realtimeData, setRealtimeData] = useState(mockRealtimeData);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [generatingReport, setGeneratingReport] = useState(false);
  const [userProfiles, setUserProfiles] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [theme, setTheme] = useState<'dark' | 'darker'>('dark');

  // Initialize lastUpdate on client side to prevent hydration mismatch
  useEffect(() => {
    setLastUpdate(new Date());
    // Simulate loading time for better UX
    setTimeout(() => setIsLoading(false), 1000);
  }, []);
  const wsRef = useRef<WebSocket | null>(null);

  // Fetch user social profiles
  useEffect(() => {
    const fetchUserProfiles = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        try {
          const response = await fetch("http://localhost:8001/api/users/profile", {
            headers: {
              "Authorization": `Bearer ${token}`,
            },
          });

          if (response.ok) {
            const userData = await response.json();
            setUserProfiles(userData.social_profiles || {});
          } else {
            // API not available, check local storage
            const localProfiles = localStorage.getItem("social_profiles");
            if (localProfiles) {
              setUserProfiles(JSON.parse(localProfiles));
            }
          }
        } catch (apiError) {
          // API not available, check local storage
          console.warn("API not available, checking local storage:", apiError);
          const localProfiles = localStorage.getItem("social_profiles");
          if (localProfiles) {
            setUserProfiles(JSON.parse(localProfiles));
          }
        }
      } catch (error) {
        console.error("Failed to fetch user profiles:", error);
      }
    };

    fetchUserProfiles();
  }, []);

  // WebSocket connection for real-time updates
  useEffect(() => {
    const connectWebSocket = () => {
      // In a real app, get user ID from auth context
      const userId = 1; // Mock user ID
      const ws = new WebSocket(`ws://localhost:8001/api/realtime/ws/dashboard/${userId}`);

      ws.onopen = () => {
        console.log('Connected to real-time dashboard');
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (message.type === 'stats_update') {
            setRealtimeData(prev => ({ ...prev, ...message.data }));
            setLastUpdate(new Date());
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onclose = () => {
        console.log('Disconnected from real-time dashboard');
        setIsConnected(false);
        // Attempt to reconnect after 5 seconds
        setTimeout(connectWebSocket, 5000);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

      wsRef.current = ws;
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Simulate real-time updates (remove in production)
  useEffect(() => {
    const interval = setInterval(() => {
      setRealtimeData(prev => ({
        ...prev,
        totalPosts: prev.totalPosts + Math.floor(Math.random() * 3),
        totalEngagement: prev.totalEngagement + Math.floor(Math.random() * 50),
        sentimentDistribution: {
          positive: Math.max(50, Math.min(80, prev.sentimentDistribution.positive + (Math.random() - 0.5) * 5)),
          neutral: Math.max(15, Math.min(35, prev.sentimentDistribution.neutral + (Math.random() - 0.5) * 3)),
          negative: Math.max(5, Math.min(20, prev.sentimentDistribution.negative + (Math.random() - 0.5) * 2))
        }
      }));
      setLastUpdate(new Date());
    }, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-400 bg-green-900/50 border border-green-700';
      case 'negative': return 'text-red-400 bg-red-900/50 border border-red-700';
      case 'neutral': return 'text-yellow-400 bg-yellow-900/50 border border-yellow-700';
      default: return 'text-slate-400 bg-slate-800/50 border border-slate-600';
    }
  };

  const generatePersonalAnalysis = async () => {
    setGeneratingReport(true);
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        window.location.href = "/login";
        return;
      }

      try {
        const response = await fetch("http://localhost:8001/api/reports/personal-social-analysis", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const report = await response.json();
          toast.success("Personal social analysis report generated and sent to your email!");
        } else if (response.status === 400) {
          const error = await response.json();
          toast.error(error.detail);
        } else {
          toast.error("Failed to generate personal analysis report");
        }
      } catch (apiError) {
        // API not available, simulate report generation
        console.warn("API not available, simulating report generation:", apiError);

        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 2000));

        toast.success("Personal analysis report generated (simulated - API not available)");
        toast.info("Report would be sent to your email when backend is running");
      }
    } catch (error) {
      toast.error("Failed to generate personal analysis report");
    } finally {
      setGeneratingReport(false);
    }
  };

  const getConnectedPlatformsCount = () => {
    if (!userProfiles) return 0;
    return Object.values(userProfiles).filter((value: any) => value && value.trim()).length;
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    setLastUpdate(new Date());
    setIsRefreshing(false);
  };

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'darker' : 'dark');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center space-y-4"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="mx-auto w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full"
          />
          <h2 className="text-2xl font-bold text-white">Loading Dashboard</h2>
          <p className="text-slate-400">Initializing AI-powered analytics...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">AI Social Intelligence Dashboard</h1>
            <p className="text-slate-400 mt-1">Real-time social media analytics and insights</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
              <span className="text-sm text-slate-400">
                {isConnected ? 'Live' : 'Connecting...'}
              </span>
            </div>
            <Badge variant="outline" className="text-xs">
              Last update: {lastUpdate ? lastUpdate.toLocaleTimeString() : 'Loading...'}
            </Badge>
            <div className="flex items-center space-x-2">
              <Button
                size="sm"
                variant="outline"
                onClick={toggleTheme}
                className="hover:bg-purple-500/10 hover:border-purple-400/50 transition-all duration-300"
              >
                {theme === 'dark' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={handleRefresh}
                disabled={isRefreshing}
                className="hover:bg-blue-500/10 hover:border-blue-400/50 transition-all duration-300"
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
                {isRefreshing ? 'Refreshing...' : 'Refresh'}
              </Button>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Total Posts</CardTitle>
                <BarChart3 className="h-4 w-4 text-blue-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{realtimeData.totalPosts.toLocaleString()}</div>
                <p className="text-xs text-green-400 mt-1">
                  <TrendingUp className="w-3 h-3 inline mr-1" />
                  +12% from yesterday
                </p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Total Engagement</CardTitle>
                <Heart className="h-4 w-4 text-red-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{realtimeData.totalEngagement.toLocaleString()}</div>
                <p className="text-xs text-green-400 mt-1">
                  <TrendingUp className="w-3 h-3 inline mr-1" />
                  +8% from yesterday
                </p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Avg Sentiment</CardTitle>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">
                  {(realtimeData.sentimentDistribution.positive / 100 * 5 + 3).toFixed(1)}/5
                </div>
                <Progress
                  value={realtimeData.sentimentDistribution.positive}
                  className="mt-2"
                />
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Active Platforms</CardTitle>
                <Users className="h-4 w-4 text-purple-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-gray-900">{realtimeData.platformStats.length}</div>
                <p className="text-xs text-gray-600 mt-1">
                  Twitter, LinkedIn, Facebook, Instagram
                </p>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Personal Social Analysis */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <Card className="bg-gradient-to-r from-slate-800/80 to-slate-700/80 backdrop-blur-md border border-slate-600">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center">
                  <User className="w-5 h-5 mr-2 text-purple-600" />
                  Your Personal Social Media Analysis
                </div>
                <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                  {getConnectedPlatformsCount()} platforms connected
                </Badge>
              </CardTitle>
              <CardDescription>
                Get AI-powered insights about your social media presence across all platforms
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="space-y-2">
                  <p className="text-sm text-gray-600">
                    {getConnectedPlatformsCount() > 0
                      ? `Connected to ${getConnectedPlatformsCount()} social media platforms. Generate a comprehensive analysis report.`
                      : "Connect your social media profiles in Settings to unlock personalized AI analysis."
                    }
                  </p>
                  {getConnectedPlatformsCount() > 0 && (
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <div className="flex items-center">
                        <Mail className="w-4 h-4 mr-1" />
                        Report sent to email
                      </div>
                      <div className="flex items-center">
                        <Sparkles className="w-4 h-4 mr-1" />
                        AI-powered insights
                      </div>
                    </div>
                  )}
                </div>
                <div className="flex space-x-3">
                  {getConnectedPlatformsCount() === 0 ? (
                    <Button
                      variant="outline"
                      onClick={() => window.location.href = "/settings"}
                      className="border-purple-300 text-purple-700 hover:bg-purple-100"
                    >
                      <Settings className="w-4 h-4 mr-2" />
                      Connect Profiles
                    </Button>
                  ) : (
                    <Button
                      onClick={generatePersonalAnalysis}
                      disabled={generatingReport}
                      className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                    >
                      {generatingReport ? (
                        <>
                          <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                          Generating...
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-4 h-4 mr-2" />
                          Generate Report
                        </>
                      )}
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Sentiment Trend */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <TrendingUp className="w-5 h-5 mr-2 text-blue-400" />
                  Sentiment Trend (24h)
                </CardTitle>
                <CardDescription className="text-slate-400">Real-time sentiment analysis over time</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full h-[300px] chart-container">
                  <ResponsiveContainer width="100%" height="100%">
                    {realtimeData.sentimentTrend && realtimeData.sentimentTrend.length > 0 ? (
                      <AreaChart data={realtimeData.sentimentTrend}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="time" tick={{ fill: '#9CA3AF' }} axisLine={{ stroke: '#4B5563' }} />
                    <YAxis tick={{ fill: '#9CA3AF' }} axisLine={{ stroke: '#4B5563' }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                        color: '#F9FAFB'
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="positive"
                      stackId="1"
                      stroke="#10B981"
                      fill="#10B981"
                      fillOpacity={0.4}
                    />
                    <Area
                      type="monotone"
                      dataKey="neutral"
                      stackId="1"
                      stroke="#F59E0B"
                      fill="#F59E0B"
                      fillOpacity={0.4}
                    />
                    <Area
                      type="monotone"
                      dataKey="negative"
                      stackId="1"
                      stroke="#EF4444"
                      fill="#EF4444"
                      fillOpacity={0.4}
                      />
                    </AreaChart>
                    ) : (
                      <div className="flex items-center justify-center h-full text-slate-400">
                        Loading chart data...
                      </div>
                    )}
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Platform Distribution */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <BarChart3 className="w-5 h-5 mr-2 text-purple-400" />
                  Platform Distribution
                </CardTitle>
                <CardDescription className="text-slate-400">Posts and engagement by platform</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="w-full h-[300px] chart-container">
                  <ResponsiveContainer width="100%" height="100%">
                    {realtimeData.platformStats && realtimeData.platformStats.length > 0 ? (
                      <BarChart data={realtimeData.platformStats}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="name" tick={{ fill: '#9CA3AF' }} axisLine={{ stroke: '#4B5563' }} />
                    <YAxis tick={{ fill: '#9CA3AF' }} axisLine={{ stroke: '#4B5563' }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                        color: '#F9FAFB'
                      }}
                    />
                    <Bar dataKey="posts" fill="#3B82F6"                       />
                    </BarChart>
                    ) : (
                      <div className="flex items-center justify-center h-full text-slate-400">
                        Loading chart data...
                      </div>
                    )}
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Bottom Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Sentiment Distribution */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <MessageCircle className="w-5 h-5 mr-2 text-green-400" />
                  Sentiment Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="w-full h-[200px]">
                  <ResponsiveContainer width="100%" height="100%">
                    {realtimeData.sentimentDistribution ? (
                      <PieChart>
                    <Pie
                      data={[
                        { name: 'Positive', value: realtimeData.sentimentDistribution.positive, color: '#10B981' },
                        { name: 'Neutral', value: realtimeData.sentimentDistribution.neutral, color: '#F59E0B' },
                        { name: 'Negative', value: realtimeData.sentimentDistribution.negative, color: '#EF4444' }
                      ]}
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={80}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {[
                        { name: 'Positive', value: realtimeData.sentimentDistribution.positive, color: '#10B981' },
                        { name: 'Neutral', value: realtimeData.sentimentDistribution.neutral, color: '#F59E0B' },
                        { name: 'Negative', value: realtimeData.sentimentDistribution.negative, color: '#EF4444' }
                      ].map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                        color: '#F9FAFB'
                      }}
                    />
                      </PieChart>
                    ) : (
                      <div className="flex items-center justify-center h-full text-slate-400">
                        Loading chart data...
                      </div>
                    )}
                  </ResponsiveContainer>
                </div>
                <div className="flex justify-center space-x-4 mt-4">
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-green-400 rounded-full mr-2" />
                    <span className="text-sm text-slate-300">Positive: {realtimeData.sentimentDistribution.positive}%</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-yellow-400 rounded-full mr-2" />
                    <span className="text-sm text-slate-300">Neutral: {realtimeData.sentimentDistribution.neutral}%</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-3 h-3 bg-red-400 rounded-full mr-2" />
                    <span className="text-sm text-slate-300">Negative: {realtimeData.sentimentDistribution.negative}%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Top Topics */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.7 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <Zap className="w-5 h-5 mr-2 text-orange-400" />
                  Top Topics
                </CardTitle>
                <CardDescription className="text-slate-400">Trending topics and sentiment</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {realtimeData.topTopics.map((topic, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex-1">
                        <p className="text-sm font-medium text-white">{topic.topic}</p>
                        <p className="text-xs text-slate-400">{topic.mentions} mentions</p>
                      </div>
                      <Badge
                        className={`${
                          topic.sentiment > 0.5 ? 'bg-green-900/50 text-green-300 border border-green-700' :
                          topic.sentiment < -0.2 ? 'bg-red-900/50 text-red-300 border border-red-700' :
                          'bg-yellow-900/50 text-yellow-300 border border-yellow-700'
                        }`}
                      >
                        {(topic.sentiment * 100).toFixed(0)}%
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Recent Posts */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.8 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center text-white">
                  <MessageCircle className="w-5 h-5 mr-2 text-blue-400" />
                  Recent Posts
                </CardTitle>
                <CardDescription className="text-slate-400">Latest social media activity</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <AnimatePresence>
                    {realtimeData.recentPosts.map((post) => (
                      <motion.div
                        key={post.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        className="border-l-4 border-blue-500 pl-4 py-2"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <p className="text-sm text-white line-clamp-2">{post.content}</p>
                            <div className="flex items-center space-x-2 mt-2">
                              <Badge variant="outline" className="text-xs border-slate-600 text-slate-300">
                                {post.platform}
                              </Badge>
                              <Badge className={`text-xs ${getSentimentColor(post.sentiment)}`}>
                                {post.sentiment}
                              </Badge>
                              <span className="text-xs text-slate-400">{post.timestamp}</span>
                            </div>
                          </div>
                          <div className="flex items-center space-x-1 text-xs text-slate-400">
                            <Heart className="w-3 h-3" />
                            <span>{Math.floor(post.engagement / 3)}</span>
                            <MessageCircle className="w-3 h-3 ml-2" />
                            <span>{Math.floor(post.engagement / 6)}</span>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}