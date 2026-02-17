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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <FileText className="w-8 h-8 mr-3 text-blue-600" />
              Reports & Analytics
            </h1>
            <p className="text-gray-600 mt-1">AI-generated business intelligence reports</p>
          </div>
          <div className="flex items-center space-x-4">
            <Button
              onClick={() => generateNewReport('daily')}
              disabled={isGenerating}
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
            >
              <Plus className="w-4 h-4 mr-2" />
              {isGenerating ? 'Generating...' : 'Generate Report'}
            </Button>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <motion.div whileHover={{ scale: 1.02 }}>
            <Card className="cursor-pointer hover:shadow-lg transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <Calendar className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">Daily Report</div>
                    <div className="text-sm text-gray-500">Last 24 hours</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div whileHover={{ scale: 1.02 }}>
            <Card className="cursor-pointer hover:shadow-lg transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="bg-green-100 p-2 rounded-lg">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">Weekly Report</div>
                    <div className="text-sm text-gray-500">Last 7 days</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div whileHover={{ scale: 1.02 }}>
            <Card className="cursor-pointer hover:shadow-lg transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="bg-purple-100 p-2 rounded-lg">
                    <BarChart3 className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">Monthly Report</div>
                    <div className="text-sm text-gray-500">Last 30 days</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div whileHover={{ scale: 1.02 }}>
            <Card className="cursor-pointer hover:shadow-lg transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="bg-orange-100 p-2 rounded-lg">
                    <Mail className="w-5 h-5 text-orange-600" />
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">Email Reports</div>
                    <div className="text-sm text-gray-500">Automated delivery</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Filters and Search */}
        <div className="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-gray-500" />
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-1 text-sm"
              >
                <option value="all">All Reports</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="custom">Custom</option>
              </select>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Search className="w-4 h-4 text-gray-500" />
            <Input
              placeholder="Search reports..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-64"
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
              <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(report.status)}
                      <div>
                        <CardTitle className="text-lg">{report.title}</CardTitle>
                        <CardDescription>
                          Generated {new Date(report.generatedAt).toLocaleDateString()}
                        </CardDescription>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusBadge(report.status)}
                      <Button variant="ghost" size="sm">
                        <MoreVertical className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-4">{report.summary}</p>

                  {/* Key Metrics */}
                  <div className="grid grid-cols-3 gap-4 mb-4">
                    <div className="text-center">
                      <div className="text-lg font-semibold text-gray-900">
                        {report.metrics.totalPosts.toLocaleString()}
                      </div>
                      <div className="text-xs text-gray-500">Total Posts</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-semibold text-green-600">
                        {(report.metrics.avgSentiment * 100).toFixed(0)}%
                      </div>
                      <div className="text-xs text-gray-500">Avg Sentiment</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-semibold text-blue-600">
                        {report.metrics.totalEngagement.toLocaleString()}
                      </div>
                      <div className="text-xs text-gray-500">Engagement</div>
                    </div>
                  </div>

                  {/* Insights */}
                  {report.insights.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-900 mb-2">Key Insights:</h4>
                      <ul className="text-sm text-gray-600 space-y-1">
                        {report.insights.slice(0, 2).map((insight, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-blue-500 mr-2">•</span>
                            {insight}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Button variant="outline" size="sm">
                        <Eye className="w-4 h-4 mr-2" />
                        View Details
                      </Button>
                      <Button variant="outline" size="sm">
                        <Download className="w-4 h-4 mr-2" />
                        Download
                      </Button>
                    </div>
                    <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {filteredReports.length === 0 && (
          <div className="text-center py-12">
            <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No reports found</h3>
            <p className="text-gray-500">Try adjusting your search or filter criteria.</p>
          </div>
        )}

        {/* Report Generation Modal would go here */}
      </div>
    </div>
  );
}