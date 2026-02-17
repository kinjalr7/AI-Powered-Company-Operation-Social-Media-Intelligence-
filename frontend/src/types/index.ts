export interface User {
  id: string;
  email: string;
  name: string;
  plan: UserPlan;
  avatar?: string;
  createdAt: Date;
  lastLogin?: Date;
}

export type UserPlan = "free" | "pro" | "enterprise";

export interface PlanFeatures {
  name: string;
  price: number;
  features: string[];
  limits: {
    socialAccounts: number;
    reports: number;
    apiCalls: number;
    storage: string;
  };
}

export interface SocialPost {
  id: string;
  platform: "twitter" | "linkedin" | "facebook" | "instagram";
  content: string;
  author: string;
  date: Date;
  engagement: {
    likes: number;
    shares: number;
    comments: number;
    views: number;
  };
  sentiment: "positive" | "negative" | "neutral";
  topics: string[];
  url: string;
}

export interface AnalyticsData {
  totalPosts: number;
  sentimentDistribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
  platformBreakdown: Record<string, number>;
  engagementTrends: Array<{
    date: Date;
    engagement: number;
    sentiment: number;
  }>;
  topTopics: Array<{
    topic: string;
    count: number;
    sentiment: number;
  }>;
}

export interface Report {
  id: string;
  title: string;
  type: "daily" | "weekly" | "monthly";
  generatedAt: Date;
  data: AnalyticsData;
  insights: string[];
  recommendations: string[];
}

export interface NotificationSettings {
  emailReports: boolean;
  realTimeAlerts: boolean;
  sentimentThreshold: number;
  keywords: string[];
}

export interface DashboardConfig {
  widgets: Array<{
    id: string;
    type: "sentiment-chart" | "engagement-chart" | "platform-breakdown" | "recent-posts";
    position: { x: number; y: number; w: number; h: number };
    settings: Record<string, any>;
  }>;
}