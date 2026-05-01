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
  const [posts, setPosts] = useState([]);
  const [filteredPosts, setFilteredPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [platformFilter, setPlatformFilter] = useState('all');
  const [sentimentFilter, setSentimentFilter] = useState('all');
  const [sortBy, setSortBy] = useState('engagement');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await fetch('/api/social-data/posts');
      if (!response.ok) {
        throw new Error('Failed to fetch posts');
      }
      const data = await response.json();
      setPosts(data || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setPosts([]);
    } finally {
      setIsLoading(false);
    }
  };

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
    fetchPosts();
  };

  const exportData = () => {
    // Simulate export functionality
    console.log('Exporting social data...');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white flex items-center">
              <Users className="w-8 h-8 mr-3 text-blue-400" />
              Social Media Data
            </h1>
            <p className="text-slate-400 mt-1">Real-time social media posts and sentiment analysis</p>
          </div>
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              size="sm"
              onClick={refreshData}
              disabled={isLoading}
              className="hover:bg-blue-500/10 hover:border-blue-400/50 transition-all duration-300"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={exportData}
              className="hover:bg-purple-500/10 hover:border-purple-400/50 transition-all duration-300"
            >
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
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Total Posts</CardTitle>
                <MessageCircle className="h-4 w-4 text-blue-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">{posts.length}</div>
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
                <div className="text-2xl font-bold text-white">
                  {posts.reduce((sum, post) => sum + post.engagement, 0).toLocaleString()}
                </div>
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
                <CardTitle className="text-sm font-medium text-slate-400">Avg Sentiment</CardTitle>
                <TrendingUp className="h-4 w-4 text-green-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-400">
                  {(posts.reduce((sum, post) => sum + post.sentimentScore, 0) / posts.length * 100).toFixed(1)}%
                </div>
                <p className="text-xs text-green-400 mt-1">
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
            <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-slate-400">Active Platforms</CardTitle>
                <Users className="h-4 w-4 text-purple-400" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-white">
                  {new Set(posts.map(post => post.platform)).size}
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Twitter, LinkedIn, Facebook, Instagram
                </p>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Filters and Search */}
        <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl">
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              <div className="lg:col-span-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
                  <Input
                    placeholder="Search posts, authors, or topics..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 bg-slate-900/50 border-slate-700 text-white placeholder:text-slate-500 focus:ring-blue-500/20"
                  />
                </div>
              </div>

              <div>
                <select
                  value={platformFilter}
                  onChange={(e) => setPlatformFilter(e.target.value)}
                  className="w-full border border-slate-700 rounded-lg px-3 py-2 text-sm bg-slate-900/50 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-300"
                >
                  <option value="all" className="bg-slate-900">All Platforms</option>
                  <option value="twitter" className="bg-slate-900">Twitter</option>
                  <option value="linkedin" className="bg-slate-900">LinkedIn</option>
                  <option value="facebook" className="bg-slate-900">Facebook</option>
                  <option value="instagram" className="bg-slate-900">Instagram</option>
                </select>
              </div>

              <div>
                <select
                  value={sentimentFilter}
                  onChange={(e) => setSentimentFilter(e.target.value)}
                  className="w-full border border-slate-700 rounded-lg px-3 py-2 text-sm bg-slate-900/50 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-300"
                >
                  <option value="all" className="bg-slate-900">All Sentiments</option>
                  <option value="positive" className="bg-slate-900">Positive</option>
                  <option value="neutral" className="bg-slate-900">Neutral</option>
                  <option value="negative" className="bg-slate-900">Negative</option>
                </select>
              </div>

              <div>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full border border-slate-700 rounded-lg px-3 py-2 text-sm bg-slate-900/50 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all duration-300"
                >
                  <option value="engagement" className="bg-slate-900">Sort by Engagement</option>
                  <option value="sentiment" className="bg-slate-900">Sort by Sentiment</option>
                  <option value="date" className="bg-slate-900">Sort by Date</option>
                  <option value="likes" className="bg-slate-900">Sort by Likes</option>
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
              <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl hover:shadow-2xl hover:shadow-blue-500/10 transition-all duration-300 overflow-hidden">
                <div className={`h-1 w-full bg-gradient-to-r ${
                  post.sentiment === 'positive' ? 'from-green-500 to-emerald-500' :
                  post.sentiment === 'negative' ? 'from-red-500 to-rose-500' :
                  'from-yellow-500 to-amber-500'
                }`} />
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      {getPlatformIcon(post.platform)}
                      <div>
                        <div className="font-semibold text-white">@{post.author}</div>
                        <div className="text-sm text-slate-400">
                          {post.platform} • {new Date(post.postedAt).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge className={`${
                        post.sentiment === 'positive' ? 'bg-green-500/20 text-green-400 border border-green-500/40' :
                        post.sentiment === 'negative' ? 'bg-red-500/20 text-red-400 border border-red-500/40' :
                        'bg-yellow-500/20 text-yellow-400 border border-yellow-500/40'
                      }`}>
                        {post.sentiment.charAt(0).toUpperCase() + post.sentiment.slice(1)}
                      </Badge>
                    </div>
                  </div>

                  <p className="text-slate-200 mb-4 leading-relaxed">{post.content}</p>

                  <div className="flex flex-wrap gap-2 mb-4">
                    {post.topics.map((topic, idx) => (
                      <Badge key={idx} variant="outline" className="text-xs border-slate-700 text-slate-400 hover:text-white hover:border-slate-500 transition-colors">
                        {topic}
                      </Badge>
                    ))}
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-6 text-sm text-slate-400">
                      <div className="flex items-center space-x-1 group cursor-pointer hover:text-red-400 transition-colors">
                        <Heart className="w-4 h-4 group-hover:fill-red-400 transition-colors" />
                        <span>{post.likes.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center space-x-1 group cursor-pointer hover:text-blue-400 transition-colors">
                        <Share2 className="w-4 h-4" />
                        <span>{post.shares.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center space-x-1 group cursor-pointer hover:text-indigo-400 transition-colors">
                        <MessageCircle className="w-4 h-4" />
                        <span>{post.comments.toLocaleString()}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Eye className="w-4 h-4" />
                        <span>{post.engagement.toLocaleString()}</span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-4">
                      <div className="text-sm text-slate-500">
                        Reliability: <span className="text-slate-300">{(post.sentimentScore * 100).toFixed(1)}%</span>
                      </div>
                      <Button 
                        variant="outline" 
                        size="sm"
                        className="bg-slate-900/50 border-slate-700 text-white hover:bg-slate-800"
                      >
                        <Eye className="w-4 h-4 mr-2" />
                        Insights
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {filteredPosts.length === 0 && !isLoading && (
          <div className="text-center py-20 bg-slate-800/50 backdrop-blur-md rounded-2xl border border-slate-700 border-dashed">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
            >
              <MessageCircle className="w-16 h-16 text-slate-600 mx-auto mb-4" />
              <h3 className="text-xl font-medium text-white mb-2">
                {error ? 'Error loading posts' : 'No posts yet. Add a social account to begin.'}
              </h3>
              <p className="text-slate-500">
                {error ? error : 'Connect your social media accounts to start collecting data.'}
              </p>
            </motion.div>
          </div>
        )}
      </div>
    </div>

  );
}