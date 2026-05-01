"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  PieChart as PieChartIcon,
  BarChart3,
  TrendingUp,
  Activity,
  Calendar,
  Filter,
  Download,
  RefreshCw,
  ZoomIn,
  Settings
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
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
  AreaChart,
  Area,
  ScatterChart,
  Scatter,
  ComposedChart,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  FunnelChart,
  Funnel,
  LabelList
} from 'recharts';

// Mock data for various charts
const sentimentData = [
  { month: 'Jan', positive: 65, neutral: 25, negative: 10 },
  { month: 'Feb', positive: 68, neutral: 22, negative: 10 },
  { month: 'Mar', positive: 72, neutral: 18, negative: 10 },
  { month: 'Apr', positive: 69, neutral: 21, negative: 10 },
  { month: 'May', positive: 75, neutral: 15, negative: 10 },
  { month: 'Jun', positive: 78, neutral: 12, negative: 10 }
];

const platformData = [
  { name: 'Twitter', value: 35, engagement: 18234, color: '#1DA1F2' },
  { name: 'LinkedIn', value: 28, engagement: 15234, color: '#0077B5' },
  { name: 'Facebook', value: 22, engagement: 9876, color: '#1877F2' },
  { name: 'Instagram', value: 15, engagement: 2288, color: '#E4405F' }
];

const engagementTrend = [
  { time: '00:00', likes: 120, shares: 45, comments: 78, total: 243 },
  { time: '06:00', likes: 98, shares: 32, comments: 65, total: 195 },
  { time: '12:00', likes: 245, shares: 89, comments: 134, total: 468 },
  { time: '18:00', likes: 312, shares: 156, comments: 198, total: 666 },
  { time: 'Now', likes: 289, shares: 134, comments: 167, total: 590 }
];

const topicSentimentData = [
  { topic: 'AI Technology', sentiment: 0.8, mentions: 234 },
  { topic: 'Machine Learning', sentiment: 0.7, mentions: 189 },
  { topic: 'Data Privacy', sentiment: -0.3, mentions: 156 },
  { topic: 'Business Intelligence', sentiment: 0.6, mentions: 143 },
  { topic: 'Innovation', sentiment: 0.9, mentions: 98 },
  { topic: 'Digital Transformation', sentiment: 0.7, mentions: 87 }
];

const funnelData = [
  { name: 'Total Posts', value: 10000, fill: '#8884d8' },
  { name: 'Analyzed', value: 8500, fill: '#82ca9d' },
  { name: 'Positive Sentiment', value: 6800, fill: '#ffc658' },
  { name: 'High Engagement', value: 3400, fill: '#ff7c7c' },
  { name: 'Actionable Insights', value: 1700, fill: '#8dd1e1' }
];

const radarData = [
  { subject: 'Sentiment Analysis', A: 85, fullMark: 100 },
  { subject: 'Engagement Tracking', A: 92, fullMark: 100 },
  { subject: 'Trend Detection', A: 78, fullMark: 100 },
  { subject: 'Platform Coverage', A: 95, fullMark: 100 },
  { subject: 'Real-time Updates', A: 88, fullMark: 100 },
  { subject: 'AI Accuracy', A: 91, fullMark: 100 }
];

const chartTypes = [
  { id: 'sentiment-trend', name: 'Sentiment Trend', icon: TrendingUp },
  { id: 'platform-distribution', name: 'Platform Distribution', icon: PieChartIcon },
  { id: 'engagement-patterns', name: 'Engagement Patterns', icon: Activity },
  { id: 'topic-analysis', name: 'Topic Analysis', icon: BarChart3 },
  { id: 'conversion-funnel', name: 'Conversion Funnel', icon: TrendingUp },
  { id: 'performance-radar', name: 'Performance Radar', icon: Activity }
];

export default function ChartsPage() {
  const [selectedChart, setSelectedChart] = useState('sentiment-trend');
  const [timeRange, setTimeRange] = useState('30d');
  const [isFullscreen, setIsFullscreen] = useState(false);

  const renderChart = () => {
    switch (selectedChart) {
      case 'sentiment-trend':
        return (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Sentiment Trend Over Time</h3>
              <Badge variant="secondary">6 Months</Badge>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={sentimentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip formatter={(value, name) => [`${value}%`, String(name).charAt(0).toUpperCase() + String(name).slice(1)]} />
                <Area type="monotone" dataKey="positive" stackId="1" stroke="#10B981" fill="#10B981" fillOpacity={0.8} />
                <Area type="monotone" dataKey="neutral" stackId="1" stroke="#F59E0B" fill="#F59E0B" fillOpacity={0.8} />
                <Area type="monotone" dataKey="negative" stackId="1" stroke="#EF4444" fill="#EF4444" fillOpacity={0.8} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        );

      case 'platform-distribution':
        return (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Platform Distribution & Engagement</h3>
              <Badge variant="secondary">All Platforms</Badge>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={platformData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={120}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {platformData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                    <LabelList dataKey="name" position="outside" />
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}%`, 'Distribution']} />
                </PieChart>
              </ResponsiveContainer>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={platformData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip formatter={(value) => [value.toLocaleString(), 'Engagement']} />
                  <Bar dataKey="engagement" fill="#3B82F6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        );

      case 'engagement-patterns':
        return (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Engagement Patterns Throughout Day</h3>
              <Badge variant="secondary">24 Hours</Badge>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <ComposedChart data={engagementTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Bar yAxisId="left" dataKey="total" fill="#3B82F6" name="Total Engagement" />
                <Line yAxisId="right" type="monotone" dataKey="likes" stroke="#10B981" name="Likes" strokeWidth={3} />
                <Line yAxisId="right" type="monotone" dataKey="comments" stroke="#F59E0B" name="Comments" strokeWidth={3} />
                <Line yAxisId="right" type="monotone" dataKey="shares" stroke="#EF4444" name="Shares" strokeWidth={3} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        );

      case 'topic-analysis':
        return (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Topic Sentiment Analysis</h3>
              <Badge variant="secondary">Top 6 Topics</Badge>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <ScatterChart data={topicSentimentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" dataKey="sentiment" name="Sentiment Score" domain={[-1, 1]} />
                <YAxis type="number" dataKey="mentions" name="Mentions" />
                <Tooltip
                  formatter={(value, name) => [
                    name === 'Mentions' ? value : (typeof value === 'number' ? value.toFixed(2) : value),
                    name
                  ]}
                  labelFormatter={(label, payload) => {
                    if (payload && payload[0]) {
                      return payload[0].payload.topic;
                    }
                    return label;
                  }}
                />
                <Scatter name="Topics" dataKey="mentions" fill="#8884d8" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        );

      case 'conversion-funnel':
        return (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Content Performance Funnel</h3>
              <Badge variant="secondary">Conversion Analysis</Badge>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <FunnelChart>
                <Tooltip />
                <Funnel
                  dataKey="value"
                  data={funnelData}
                  isAnimationActive
                >
                  <LabelList position="center" fill="#fff" stroke="none" />
                </Funnel>
              </FunnelChart>
            </ResponsiveContainer>
          </div>
        );

      case 'performance-radar':
        return (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">AI Performance Metrics</h3>
              <Badge variant="secondary">System Health</Badge>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <PolarRadiusAxis angle={90} domain={[0, 100]} />
                <Radar
                  name="Performance"
                  dataKey="A"
                  stroke="#8884d8"
                  fill="#8884d8"
                  fillOpacity={0.6}
                  strokeWidth={2}
                />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        );

      default:
        return <div>Select a chart type</div>;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <BarChart3 className="w-8 h-8 mr-3 text-blue-600" />
              Interactive Charts
            </h1>
            <p className="text-gray-600 mt-1">Advanced visualizations for social media intelligence</p>
          </div>
          <div className="flex items-center space-x-4">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm bg-white"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
              <option value="1y">Last year</option>
            </select>
            <Button variant="outline" size="sm">
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsFullscreen(!isFullscreen)}
            >
              <ZoomIn className="w-4 h-4 mr-2" />
              {isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
            </Button>
          </div>
        </div>

        <div className={`grid ${isFullscreen ? 'grid-cols-1' : 'grid-cols-1 lg:grid-cols-4'} gap-6`}>
          {/* Chart Type Selector */}
          {!isFullscreen && (
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Chart Types</CardTitle>
                  <CardDescription>Select a visualization to explore</CardDescription>
                </CardHeader>
                <CardContent className="space-y-2">
                  {chartTypes.map((chart) => {
                    const Icon = chart.icon;
                    return (
                      <motion.div
                        key={chart.id}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <button
                          onClick={() => setSelectedChart(chart.id)}
                          className={`w-full flex items-center space-x-3 p-3 rounded-lg transition-all ${
                            selectedChart === chart.id
                              ? 'bg-blue-100 text-blue-900 border border-blue-300'
                              : 'hover:bg-gray-100 text-gray-700'
                          }`}
                        >
                          <Icon className="w-5 h-5" />
                          <span className="text-sm font-medium">{chart.name}</span>
                        </button>
                      </motion.div>
                    );
                  })}
                </CardContent>
              </Card>

              {/* Quick Stats */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Quick Stats</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Total Posts</span>
                    <span className="font-semibold">12,456</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Avg Sentiment</span>
                    <span className="font-semibold text-green-600">78.5%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Engagement Rate</span>
                    <span className="font-semibold text-blue-600">12.4%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Active Topics</span>
                    <span className="font-semibold">47</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Main Chart Area */}
          <div className={`${isFullscreen ? 'col-span-1' : 'lg:col-span-3'}`}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Settings className="w-5 h-5 text-gray-500" />
                      <span className="text-sm text-gray-600">Interactive Controls</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button variant="ghost" size="sm">
                        <RefreshCw className="w-4 h-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Filter className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {renderChart()}
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>

        {/* Additional Insights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Key Insights</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-green-500 mr-2">•</span>
                  Sentiment improved by 8% this month
                </li>
                <li className="flex items-start">
                  <span className="text-blue-500 mr-2">•</span>
                  Twitter shows highest engagement rates
                </li>
                <li className="flex items-start">
                  <span className="text-purple-500 mr-2">•</span>
                  AI topics trending across all platforms
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Trending Topics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {topicSentimentData.slice(0, 3).map((topic, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm font-medium">{topic.topic}</span>
                    <Badge className={topic.sentiment > 0.5 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                      {topic.sentiment > 0.5 ? 'Positive' : 'Neutral'}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Performance Metrics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Accuracy</span>
                  <span className="font-semibold text-green-600">95.2%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Coverage</span>
                  <span className="font-semibold text-blue-600">87.4%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Speed</span>
                  <span className="font-semibold text-purple-600">1.2s avg</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}