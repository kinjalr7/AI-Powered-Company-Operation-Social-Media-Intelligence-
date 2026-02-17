"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Users,
  Search,
  Filter,
  Calendar,
  TrendingUp,
  MessageCircle,
  Heart,
  Share2,
  Eye,
  Download,
  RefreshCw,
  ThumbsUp,
  ThumbsDown,
  Minus
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";

// Mock social media posts data
const mockPosts = [
  {
    id: 1,
    platform: 'Twitter',
    author: 'TechInnovator',
    content: 'Excited about the latest developments in AI and machine learning! The future of technology is looking bright. #AI #Tech #Innovation',
    postedAt: '2024-01-15T10:30:00Z',
    likes: 234,
    shares: 45,
    comments: 67,
    sentiment: 'positive',
    sentimentScore: 0.85,
    engagement: 346,
    topics: ['AI Technology', 'Innovation'],
    url: 'https://twitter.com/example/status/123'
  },
  {
    id: 2,
    platform: 'LinkedIn',
    author: 'DataScientistPro',
    content: 'Just published a new article on advanced sentiment analysis techniques for social media monitoring. The results are fascinating! Link in bio.',
    postedAt: '2024-01-15T09:15:00Z',
    likes: 156,
    shares: 89,
    comments: 34,
    sentiment: 'positive',
    sentimentScore: 0.78,
    engagement: 279,
    topics: ['Data Science', 'Sentiment Analysis'],
    url: 'https://linkedin.com/posts/example'
  },
  {
    id: 3,
    platform: 'Facebook',
    author: 'BusinessInsights',
    content: 'Concerned about data privacy regulations and how they might impact our ability to leverage customer insights effectively.',
    postedAt: '2024-01-15T08:45:00Z',
    likes: 98,
    shares: 23,
    comments: 45,
    sentiment: 'negative',
    sentimentScore: -0.32,
    engagement: 166,
    topics: ['Data Privacy', 'Business Intelligence'],
    url: 'https://facebook.com/posts/example'
  },
  {
    id: 4,
    platform: 'Instagram',
    author: 'StartupFounder',
    content: 'Amazing growth in our AI-powered analytics platform! User engagement up 40% this quarter. Grateful for the amazing team! 🚀 #Startups #AI',
    postedAt: '2024-01-15T07:20:00Z',
    likes: 445,
    shares: 67,
    comments: 89,
    sentiment: 'positive',
    sentimentScore: 0.92,
    engagement: 601,
    topics: ['AI Technology', 'Business Growth'],
    url: 'https://instagram.com/p/example'
  },
  {
    id: 5,
    platform: 'Twitter',
    author: 'IndustryAnalyst',
    content: 'Mixed feelings about the current state of digital transformation initiatives. Some companies are excelling while others are struggling to keep up.',
    postedAt: '2024-01-14T16:30:00Z',
    likes: 123,
    shares: 34,
    comments: 56,
    sentiment: 'neutral',
    sentimentScore: 0.05,
    engagement: 213,
    topics: ['Digital Transformation', 'Business Strategy'],
    url: 'https://twitter.com/example/status/456'
  }
];

const getSentimentIcon = (sentiment: string) => {
  switch (sentiment) {
    case 'positive':
      return <ThumbsUp className="w-4 h-4 text-green-600" />;
    case 'negative':
      return <ThumbsDown className="w-4 h-4 text-red-600" />;
    default:
      return <Minus className="w-4 h-4 text-yellow-600" />;
  }
};

const getSentimentBadge = (sentiment: string) => {
  switch (sentiment) {
    case 'positive':
      return <Badge className="bg-green-100 text-green-800">Positive</Badge>;
    case 'negative':
      return <Badge className="bg-red-100 text-red-800">Negative</Badge>;
    default:
      return <Badge className="bg-yellow-100 text-yellow-800">Neutral</Badge>;
  }
};

const getPlatformIcon = (platform: string) => {
  const iconClass = "w-4 h-4";
  switch (platform.toLowerCase()) {
    case 'twitter':
      return <span className={`text-blue-500 ${iconClass}`}>🐦</span>;
    case 'linkedin':
      return <span className={`text-blue-700 ${iconClass}`}>💼</span>;
    case 'facebook':
      return <span className={`text-blue-600 ${iconClass}`}>📘</span>;
    case 'instagram':
      return <span className={`text-pink-500 ${iconClass}`}>📷</span>;
    default:
      return <Users className={iconClass} />;
  }
};

export default function SocialDataPage() {
  const [posts, setPosts] = useState(mockPosts);
  const [filteredPosts, setFilteredPosts] = useState(mockPosts);
  const [searchTerm, setSearchTerm] = useState('');
  const [platformFilter, setPlatformFilter] = useState('all');
  const [sentimentFilter, setSentimentFilter] = useState('all');
  const [sortBy, setSortBy] = useState('engagement');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let filtered = posts.filter(post => {
      const matchesSearch = post.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           post.author.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           post.topics.some(topic => topic.toLowerCase().includes(searchTerm.toLowerCase()));
      const matchesPlatform = platformFilter === 'all' || post.platform.toLowerCase() === platformFilter;
      const matchesSentiment = sentimentFilter === 'all' || post.sentiment === sentimentFilter;

      return matchesSearch && matchesPlatform && matchesSentiment;
    });

    // Sort posts
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'engagement':
          return b.engagement - a.engagement;
        case 'sentiment':
          return b.sentimentScore - a.sentimentScore;
        case 'date':
          return new Date(b.postedAt).getTime() - new Date(a.postedAt).getTime();
        case 'likes':
          return b.likes - a.likes;
        default:
          return 0;
      }
    });

    setFilteredPosts(filtered);
  }, [posts, searchTerm, platformFilter, sentimentFilter, sortBy]);

  const refreshData = () => {
    setIsLoading(true);
    // Simulate API call
    setTimeout(() => setIsLoading(false), 1000);
  };

  const exportData = () => {
    // Simulate export functionality
    console.log('Exporting social data...');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <Users className="w-8 h-8 mr-3 text-blue-600" />
              Social Media Data
            </h1>
            <p className="text-gray-600 mt-1">Real-time social media posts and sentiment analysis</p>
          </div>
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              size="sm"
              onClick={refreshData}
              disabled={isLoading}
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            <Button variant="outline" size="sm" onClick={exportData}>
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Total Posts</CardTitle>
                <MessageCircle className="h-4 w-4 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-gray-900">{posts.length}</div>
                <p className="text-xs text-green-600 mt-1">
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
            <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Total Engagement</CardTitle>
                <Heart className="h-4 w-4 text-red-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-gray-900">
                  {posts.reduce((sum, post) => sum + post.engagement, 0).toLocaleString()}
                </div>
                <p className="text-xs text-green-600 mt-1">
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
            <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Avg Sentiment</CardTitle>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">
                  {(posts.reduce((sum, post) => sum + post.sentimentScore, 0) / posts.length * 100).toFixed(1)}%
                </div>
                <p className="text-xs text-green-600 mt-1">
                  Positive sentiment dominant
                </p>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Active Platforms</CardTitle>
                <Users className="h-4 w-4 text-purple-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-gray-900">
                  {new Set(posts.map(post => post.platform)).size}
                </div>
                <p className="text-xs text-gray-600 mt-1">
                  Twitter, LinkedIn, Facebook, Instagram
                </p>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Filters and Search */}
        <Card className="bg-white shadow-sm">
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              <div className="lg:col-span-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                  <Input
                    placeholder="Search posts, authors, or topics..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>

              <div>
                <select
                  value={platformFilter}
                  onChange={(e) => setPlatformFilter(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm bg-white"
                >
                  <option value="all">All Platforms</option>
                  <option value="twitter">Twitter</option>
                  <option value="linkedin">LinkedIn</option>
                  <option value="facebook">Facebook</option>
                  <option value="instagram">Instagram</option>
                </select>
              </div>

              <div>
                <select
                  value={sentimentFilter}
                  onChange={(e) => setSentimentFilter(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm bg-white"
                >
                  <option value="all">All Sentiments</option>
                  <option value="positive">Positive</option>
                  <option value="neutral">Neutral</option>
                  <option value="negative">Negative</option>
                </select>
              </div>

              <div>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm bg-white"
                >
                  <option value="engagement">Sort by Engagement</option>
                  <option value="sentiment">Sort by Sentiment</option>
                  <option value="date">Sort by Date</option>
                  <option value="likes">Sort by Likes</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Posts List */}
        <div className="space-y-4">
          {filteredPosts.map((post, index) => (
            <motion.div
              key={post.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      {getPlatformIcon(post.platform)}
                      <div>
                        <div className="font-semibold text-gray-900">@{post.author}</div>
                        <div className="text-sm text-gray-500">
                          {post.platform} • {new Date(post.postedAt).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getSentimentIcon(post.sentiment)}
                      {getSentimentBadge(post.sentiment)}
                    </div>
                  </div>

                  <p className="text-gray-700 mb-4 leading-relaxed">{post.content}</p>

                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.topics.map((topic, idx) => (
                      <Badge key={idx} variant="outline" className="text-xs">
                        {topic}
                      </Badge>
                    ))}
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-6 text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <Heart className="w-4 h-4" />
                        <span>{post.likes.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Share2 className="w-4 h-4" />
                        <span>{post.shares.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MessageCircle className="w-4 h-4" />
                        <span>{post.comments.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Eye className="w-4 h-4" />
                        <span>{post.engagement.toLocaleString()}</span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2">
                      <div className="text-sm text-gray-500">
                        Sentiment: {(post.sentimentScore * 100).toFixed(1)}%
                      </div>
                      <Button variant="outline" size="sm">
                        <Eye className="w-4 h-4 mr-2" />
                        View Details
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {filteredPosts.length === 0 && (
          <div className="text-center py-12">
            <MessageCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No posts found</h3>
            <p className="text-gray-500">Try adjusting your search or filter criteria.</p>
          </div>
        )}
      </div>
    </div>
  );
}