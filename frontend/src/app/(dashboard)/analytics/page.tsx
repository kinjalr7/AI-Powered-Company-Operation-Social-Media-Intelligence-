"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Brain,
  TrendingUp,
  TrendingDown,
  MessageCircle,
  Users,
  BarChart3,
  PieChart,
  Activity,
  Calendar,
  Filter,
  Download,
  RefreshCw
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
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  AreaChart,
  Area,
  ScatterChart,
  Scatter
} from 'recharts';

// Mock data for demonstration
const sentimentTrendData = [
  { date: '2024-01-01', positive: 65, negative: 15, neutral: 20, volume: 1200 },
  { date: '2024-01-02', positive: 68, negative: 12, neutral: 20, volume: 1350 },
  { date: '2024-01-03', positive: 72, negative: 10, neutral: 18, volume: 1100 },
  { date: '2024-01-04', positive: 69, negative: 14, neutral: 17, volume: 1400 },
  { date: '2024-01-05', positive: 75, negative: 8, neutral: 17, volume: 1600 },
  { date: '2024-01-06', positive: 71, negative: 11, neutral: 18, volume: 1450 },
  { date: '2024-01-07', positive: 78, negative: 9, neutral: 13, volume: 1800 }
];

const topicAnalysisData = [
  { topic: 'AI Technology', mentions: 234, sentiment: 0.8, growth: 15 },
  { topic: 'Machine Learning', mentions: 189, sentiment: 0.7, growth: 8 },
  { topic: 'Data Privacy', mentions: 156, sentiment: -0.3, growth: -5 },
  { topic: 'Business Intelligence', mentions: 143, sentiment: 0.6, growth: 12 },
  { topic: 'Innovation', mentions: 98, sentiment: 0.9, growth: 20 },
  { topic: 'Digital Transformation', mentions: 87, sentiment: 0.7, growth: 18 },
  { topic: 'Automation', mentions: 76, sentiment: 0.5, growth: 25 }
];

const platformPerformanceData = [
  { platform: 'Twitter', posts: 523, engagement: 18234, sentiment: 0.75, reach: 125000 },
  { platform: 'LinkedIn', posts: 324, engagement: 15234, sentiment: 0.82, reach: 89000 },
  { platform: 'Facebook', posts: 267, engagement: 9876, sentiment: 0.68, reach: 156000 },
  { platform: 'Instagram', posts: 133, engagement: 2288, sentiment: 0.71, reach: 67000 }
];

const engagementCorrelationData = [
  { sentiment: 0.1, engagement: 120 },
  { sentiment: 0.3, engagement: 180 },
  { sentiment: 0.5, engagement: 250 },
  { sentiment: 0.7, engagement: 320 },
  { sentiment: 0.9, engagement: 450 },
  { sentiment: 0.2, engagement: 140 },
  { sentiment: 0.4, engagement: 210 },
  { sentiment: 0.6, engagement: 280 },
  { sentiment: 0.8, engagement: 380 },
  { sentiment: 0.15, engagement: 135 }
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState('7d');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState('all');

  const refreshData = () => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => setIsLoading(false), 1000);
  };

  const exportData = () => {
    // Simulate export functionality
    console.log('Exporting analytics data...');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white flex items-center">
              <Brain className="w-8 h-8 mr-3 text-blue-400" />
              Advanced Analytics
            </h1>
            <p className="text-slate-400 mt-1">Deep insights powered by AI and machine learning</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-slate-400" />
              <select
                value={selectedPlatform}
                onChange={(e) => setSelectedPlatform(e.target.value)}
                className="border border-slate-600 rounded-lg px-3 py-1 text-sm bg-slate-800/50 text-white backdrop-blur-sm"
              >
                <option value="all">All Platforms</option>
                <option value="twitter">Twitter</option>
                <option value="linkedin">LinkedIn</option>
                <option value="facebook">Facebook</option>
                <option value="instagram">Instagram</option>
              </select>
            </div>
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="border border-slate-600 rounded-lg px-3 py-1 text-sm bg-slate-800/50 text-white backdrop-blur-sm"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
              <option value="1y">Last year</option>
            </select>
            <Button
              variant="outline"
              size="sm"
              onClick={refreshData}
              disabled={isLoading}
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={exportData}
            >
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
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
                <CardTitle className="text-sm font-medium text-slate-400">Sentiment Score</CardTitle>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">78.5%</div>
                <p className="text-xs text-green-600 mt-1">
                  +5.2% from last period
                </p>
                <Progress value={78.5} className="mt-2" />
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
                <CardTitle className="text-sm font-medium text-slate-400">Topic Diversity</CardTitle>
                <MessageCircle className="h-4 w-4 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">47</div>
                <p className="text-xs text-blue-600 mt-1">
                  Active topics identified
                </p>
                <div className="text-xs text-slate-500 mt-1">+12 new topics</div>
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
                <CardTitle className="text-sm font-medium text-slate-400">Engagement Rate</CardTitle>
                <Activity className="h-4 w-4 text-purple-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-600">12.4%</div>
                <p className="text-xs text-green-600 mt-1">
                  +2.1% from last period
                </p>
                <div className="text-xs text-slate-500 mt-1">3.2K total engagements</div>
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
                <CardTitle className="text-sm font-medium text-slate-400">AI Insights</CardTitle>
                <Brain className="h-4 w-4 text-orange-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-orange-600">23</div>
                <p className="text-xs text-orange-600 mt-1">
                  Generated this week
                </p>
                <div className="text-xs text-slate-500 mt-1">87% accuracy rate</div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Main Charts */}
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
                  Sentiment Trend Analysis
                </CardTitle>
                <CardDescription className="text-slate-400">Daily sentiment distribution over time</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={sentimentTrendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis
                      dataKey="date"
                      tick={{ fill: '#9CA3AF' }}
                      axisLine={{ stroke: '#4B5563' }}
                      tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    />
                    <YAxis tick={{ fill: '#9CA3AF' }} axisLine={{ stroke: '#4B5563' }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1F2937',
                        border: '1px solid #374151',
                        borderRadius: '8px',
                        color: '#F9FAFB'
                      }}
                      labelFormatter={(value) => new Date(value).toLocaleDateString()}
                      formatter={(value, name) => [`${value}%`, String(name).charAt(0).toUpperCase() + String(name).slice(1)]}
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
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>

          {/* Platform Performance */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="w-5 h-5 mr-2 text-purple-600" />
                  Platform Performance
                </CardTitle>
                <CardDescription>Engagement and sentiment by platform</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={platformPerformanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip />
                    <Bar yAxisId="left" dataKey="engagement" fill="#3B82F6" name="Engagement" />
                    <Bar yAxisId="right" dataKey="sentiment" fill="#10B981" name="Sentiment Score" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Bottom Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Topic Analysis */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <MessageCircle className="w-5 h-5 mr-2 text-green-600" />
                  Top Topics Analysis
                </CardTitle>
                <CardDescription>Trending topics with sentiment scores</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {topicAnalysisData.slice(0, 5).map((topic, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex-1">
                        <p className="text-sm font-medium text-white">{topic.topic}</p>
                        <p className="text-xs text-slate-500">{topic.mentions} mentions</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge
                          className={`${
                            topic.sentiment > 0.5 ? 'bg-green-100 text-green-800' :
                            topic.sentiment < -0.2 ? 'bg-red-100 text-red-800' :
                            'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {(topic.sentiment * 100).toFixed(0)}%
                        </Badge>
                        <div className={`text-xs ${topic.growth > 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {topic.growth > 0 ? '+' : ''}{topic.growth}%
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Sentiment vs Engagement Correlation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.7 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="w-5 h-5 mr-2 text-orange-600" />
                  Sentiment-Engagement Correlation
                </CardTitle>
                <CardDescription>How sentiment affects engagement</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <ScatterChart data={engagementCorrelationData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      type="number"
                      dataKey="sentiment"
                      name="Sentiment Score"
                      domain={[-1, 1]}
                    />
                    <YAxis
                      type="number"
                      dataKey="engagement"
                      name="Engagement"
                    />
                    <Tooltip
                      formatter={(value, name) => [value, name]}
                      labelFormatter={() => ''}
                    />
                    <Scatter
                      name="Posts"
                      dataKey="engagement"
                      fill="#F59E0B"
                    />
                  </ScatterChart>
                </ResponsiveContainer>
                <div className="text-xs text-slate-500 mt-2 text-center">
                  Correlation coefficient: 0.78 (Strong positive)
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* AI Insights Summary */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.8 }}
          >
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="w-5 h-5 mr-2 text-indigo-600" />
                  AI Insights Summary
                </CardTitle>
                <CardDescription>Key findings from AI analysis</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <div className="text-sm font-medium text-blue-900">Trend Alert</div>
                    <div className="text-xs text-blue-700 mt-1">
                      AI adoption discussions increased by 45% this week
                    </div>
                  </div>
                  <div className="p-3 bg-green-50 rounded-lg">
                    <div className="text-sm font-medium text-green-900">Positive Momentum</div>
                    <div className="text-xs text-green-700 mt-1">
                      Brand sentiment improved across all platforms
                    </div>
                  </div>
                  <div className="p-3 bg-yellow-50 rounded-lg">
                    <div className="text-sm font-medium text-yellow-900">Watch Topic</div>
                    <div className="text-xs text-yellow-700 mt-1">
                      Data privacy concerns showing mixed reactions
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}