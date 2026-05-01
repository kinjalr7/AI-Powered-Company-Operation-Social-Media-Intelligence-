"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  FileText,
  Download,
  Calendar,
  TrendingUp,
  BarChart3,
  Mail,
  Plus,
  Filter,
  Search,
  MoreVertical,
  Eye,
  Trash2,
  RefreshCw,
  Clock,
  CheckCircle,
  AlertCircle
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";

// Mock data for reports
const mockReports = [
  {
    id: 1,
    title: "Weekly Social Media Performance Report",
    type: "weekly",
    status: "completed",
    generatedAt: "2024-01-15T10:30:00Z",
    summary: "Overall positive sentiment with 15% growth in engagement across all platforms.",
    insights: [
      "Twitter engagement increased by 23%",
      "LinkedIn posts showing highest sentiment scores",
      "AI technology discussions trending upward"
    ],
    metrics: {
      totalPosts: 1247,
      avgSentiment: 0.78,
      totalEngagement: 45632
    }
  },
  {
    id: 2,
    title: "Daily Business Intelligence Summary",
    type: "daily",
    status: "completed",
    generatedAt: "2024-01-14T09:00:00Z",
    summary: "Mixed sentiment with focus on data privacy concerns and AI adoption.",
    insights: [
      "Data privacy discussions increased by 45%",
      "Positive sentiment on AI innovation topics",
      "Facebook engagement showing decline"
    ],
    metrics: {
      totalPosts: 234,
      avgSentiment: 0.65,
      totalEngagement: 8921
    }
  },
  {
    id: 3,
    title: "Monthly Analytics Deep Dive",
    type: "monthly",
    status: "processing",
    generatedAt: "2024-01-13T14:20:00Z",
    summary: "Processing comprehensive monthly analysis...",
    insights: [],
    metrics: {
      totalPosts: 0,
      avgSentiment: 0,
      totalEngagement: 0
    }
  },
  {
    id: 4,
    title: "Custom Period Analysis - Q4 2023",
    type: "custom",
    status: "completed",
    generatedAt: "2024-01-12T16:45:00Z",
    summary: "Quarterly analysis shows consistent growth in brand mentions and positive sentiment.",
    insights: [
      "Brand awareness increased by 28%",
      "Competitor analysis shows market positioning improvement",
      "Content strategy performing well across platforms"
    ],
    metrics: {
      totalPosts: 3456,
      avgSentiment: 0.82,
      totalEngagement: 123456
    }
  }
];

export default function ReportsPage() {
  const [reports, setReports] = useState(mockReports);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedReport, setSelectedReport] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const filteredReports = reports.filter(report => {
    const matchesFilter = filter === 'all' || report.type === filter;
    const matchesSearch = report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         report.summary.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const generateNewReport = async (type: string) => {
    setIsGenerating(true);
    // Simulate API call
    setTimeout(() => {
      const newReport = {
        id: reports.length + 1,
        title: `${type.charAt(0).toUpperCase() + type.slice(1)} Report - ${new Date().toLocaleDateString()}`,
        type,
        status: "processing",
        generatedAt: new Date().toISOString(),
        summary: "Generating AI-powered insights...",
        insights: [],
        metrics: {
          totalPosts: 0,
          avgSentiment: 0,
          totalEngagement: 0
        }
      };
      setReports([newReport, ...reports]);
      setIsGenerating(false);
    }, 2000);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'processing':
        return <RefreshCw className="w-4 h-4 text-blue-600 animate-spin" />;
      case 'failed':
        return <AlertCircle className="w-4 h-4 text-red-600" />;
      default:
        return <Clock className="w-4 h-4 text-gray-600" />;
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <Badge className="bg-green-100 text-green-800">Completed</Badge>;
      case 'processing':
        return <Badge className="bg-blue-100 text-blue-800">Processing</Badge>;
      case 'failed':
        return <Badge className="bg-red-100 text-red-800">Failed</Badge>;
      default:
        return <Badge className="bg-gray-100 text-gray-800">Scheduled</Badge>;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white flex items-center">
              <FileText className="w-8 h-8 mr-3 text-blue-400" />
              Reports & Analytics
            </h1>
            <p className="text-slate-400 mt-1">AI-generated business intelligence reports</p>
          </div>
          <div className="flex items-center space-x-4">
            <Button
              onClick={() => generateNewReport('daily')}
              disabled={isGenerating}
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-lg shadow-blue-500/20"
            >
              <Plus className="w-4 h-4 mr-2" />
              {isGenerating ? 'Generating...' : 'Generate Intelligence'}
            </Button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { title: 'Daily Report', desc: 'Last 24 hours', icon: Calendar, color: 'text-blue-400', bg: 'bg-blue-400/10' },
            { title: 'Weekly Report', desc: 'Last 7 days', icon: TrendingUp, color: 'text-green-400', bg: 'bg-green-400/10' },
            { title: 'Monthly Report', desc: 'Last 30 days', icon: BarChart3, color: 'text-purple-400', bg: 'bg-purple-400/10' },
            { title: 'Email Reports', desc: 'Automated delivery', icon: Mail, color: 'text-orange-400', bg: 'bg-orange-400/10' }
          ].map((action, i) => (
            <motion.div key={i} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Card className="cursor-pointer bg-slate-800/90 backdrop-blur-md border border-slate-700 hover:border-slate-500 transition-all duration-300">
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <div className={`${action.bg} p-2 rounded-lg`}>
                      <action.icon className={`w-5 h-5 ${action.color}`} />
                    </div>
                    <div>
                      <div className="font-medium text-white">{action.title}</div>
                      <div className="text-sm text-slate-500">{action.desc}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Filters and Search */}
        <div className="flex items-center justify-between bg-slate-800/90 backdrop-blur-md p-4 rounded-xl border border-slate-700 shadow-xl">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-slate-400" />
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="bg-slate-900/50 border border-slate-700 text-white rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20"
              >
                <option value="all" className="bg-slate-900">All Reports</option>
                <option value="daily" className="bg-slate-900">Daily</option>
                <option value="weekly" className="bg-slate-900">Weekly</option>
                <option value="monthly" className="bg-slate-900">Monthly</option>
                <option value="custom" className="bg-slate-900">Custom</option>
              </select>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Search className="w-4 h-4 text-slate-400" />
            <Input
              placeholder="Search intelligence..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-64 bg-slate-900/50 border-slate-700 text-white placeholder:text-slate-500"
            />
          </div>
        </div>

        {/* Reports List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredReports.map((report, index) => (
            <motion.div
              key={report.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300 overflow-hidden">
                <div className={`h-1 w-full bg-gradient-to-r ${
                  report.status === 'completed' ? 'from-green-500 to-emerald-500' :
                  report.status === 'processing' ? 'from-blue-500 to-indigo-500' :
                  'from-red-500 to-rose-500'
                }`} />
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      {report.status === 'completed' ? <CheckCircle className="w-5 h-5 text-green-400" /> :
                       report.status === 'processing' ? <RefreshCw className="w-5 h-5 text-blue-400 animate-spin" /> :
                       <AlertCircle className="w-5 h-5 text-red-400" />}
                      <div>
                        <CardTitle className="text-lg text-white">{report.title}</CardTitle>
                        <CardDescription className="text-slate-500">
                          Generated {new Date(report.generatedAt).toLocaleDateString()}
                        </CardDescription>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                       <Badge className={`${
                        report.status === 'completed' ? 'bg-green-500/20 text-green-400 border border-green-500/40' :
                        report.status === 'processing' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/40' :
                        'bg-red-500/20 text-red-400 border border-red-500/40'
                      }`}>
                        {report.status.charAt(0).toUpperCase() + report.status.slice(1)}
                      </Badge>
                      <Button variant="ghost" size="sm" className="text-slate-400 hover:text-white">
                        <MoreVertical className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-slate-300 mb-6">{report.summary}</p>

                  {/* Key Metrics */}
                  <div className="grid grid-cols-3 gap-4 mb-6 bg-slate-900/50 p-4 rounded-xl border border-slate-700">
                    <div className="text-center">
                      <div className="text-lg font-semibold text-white">
                        {report.metrics.totalPosts.toLocaleString()}
                      </div>
                      <div className="text-xs text-slate-500">Total Posts</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-semibold text-green-400">
                        {(report.metrics.avgSentiment * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-slate-500">Avg Sentiment</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-semibold text-blue-400">
                        {report.metrics.totalEngagement.toLocaleString()}
                      </div>
                      <div className="text-xs text-slate-500">Engagement</div>
                    </div>
                  </div>

                  {/* Insights */}
                  {report.insights.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-sm font-medium text-white mb-2 flex items-center">
                        <TrendingUp className="w-4 h-4 mr-2 text-blue-400" />
                        Intelligence Insights:
                      </h4>
                      <ul className="text-sm text-slate-400 space-y-2">
                        {report.insights.slice(0, 2).map((insight, idx) => (
                          <li key={idx} className="flex items-start bg-slate-900/30 p-2 rounded-lg border border-slate-800">
                            <span className="text-blue-400 mr-2">•</span>
                            {insight}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex items-center justify-between mt-4">
                    <div className="flex items-center space-x-3">
                      <Button variant="outline" size="sm" className="bg-slate-900/50 border-slate-700 text-white hover:bg-slate-800">
                        <Eye className="w-4 h-4 mr-2" />
                        Analyze
                      </Button>
                      <Button variant="outline" size="sm" className="bg-slate-900/50 border-slate-700 text-white hover:bg-slate-800">
                        <Download className="w-4 h-4 mr-2" />
                        Export
                      </Button>
                    </div>
                    <Button variant="ghost" size="sm" className="text-rose-500 hover:text-rose-400 hover:bg-rose-500/10">
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {filteredReports.length === 0 && (
          <div className="text-center py-20 bg-slate-800/50 backdrop-blur-md rounded-2xl border border-slate-700 border-dashed">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <FileText className="w-16 h-16 text-slate-600 mx-auto mb-4" />
              <h3 className="text-xl font-medium text-white mb-2">No intelligence reports found</h3>
              <p className="text-slate-500">Generate a new report to unlock AI-powered insights.</p>
            </motion.div>
          </div>
        )}
      </div>
    </div>

  );
}