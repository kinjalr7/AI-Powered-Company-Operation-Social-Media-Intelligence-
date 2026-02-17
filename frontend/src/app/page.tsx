import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LiveDemo } from "@/components/live-demo";
// import { motion, AnimatePresence } from "framer-motion";
import {
  BarChart3,
  Brain,
  TrendingUp,
  Users,
  Zap,
  Shield,
  Mail,
  Database,
  ArrowRight,
  Sparkles
} from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "AI-Powered Analytics",
    description: "Advanced NLP and sentiment analysis for deep insights into social media conversations.",
    color: "text-blue-400"
  },
  {
    icon: TrendingUp,
    title: "Real-Time Monitoring",
    description: "Live tracking of social media trends, engagement metrics, and brand mentions.",
    color: "text-green-400"
  },
  {
    icon: Users,
    title: "Hiring Intelligence",
    description: "Track tech skills demand, company culture insights, and recruitment trends.",
    color: "text-purple-400"
  },
  {
    icon: Mail,
    title: "Automated Reports",
    description: "Daily AI-generated business reports delivered directly to your inbox.",
    color: "text-orange-400"
  },
  {
    icon: Database,
    title: "Smart Data Pipeline",
    description: "Seamless integration with PostgreSQL for robust data storage and processing.",
    color: "text-cyan-400"
  },
  {
    icon: Shield,
    title: "Enterprise Security",
    description: "Bank-level security with encrypted data and secure API endpoints.",
    color: "text-red-400"
  }
];

const stats = [
  { value: "10K+", label: "Social Posts Analyzed" },
  { value: "95%", label: "Accuracy Rate" },
  { value: "24/7", label: "Real-Time Monitoring" },
  { value: "500+", label: "Companies Served" }
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 sm:py-32 floating-particles">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-cyan-500/10" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(59,130,246,0.15),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(139,92,246,0.1),transparent_50%)]" />
        <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-4xl text-center">
            <div className="mb-8">
              <Badge variant="secondary" className="mb-4 px-4 py-2 text-sm font-medium bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-400/30 text-blue-200 backdrop-blur-sm">
                <Sparkles className="mr-2 h-4 w-4 text-blue-400" />
                Powered by AI & Machine Learning
              </Badge>
            </div>

            <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl lg:text-7xl">
              AI Social Media
              <span className="block bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent drop-shadow-lg animate-shimmer">
                Intelligence System
              </span>
            </h1>

            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-300">
              Transform your business operations with AI-powered social media monitoring,
              real-time analytics, and automated intelligence reports. Monitor trends,
              track hiring insights, and stay ahead of the competition.
            </p>

            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link href="/login">
                <Button size="lg" className="bg-gradient-to-r from-blue-500 via-purple-600 to-blue-600 hover:from-blue-600 hover:via-purple-700 hover:to-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 border border-blue-400/30 backdrop-blur-sm pulse-glow">
                  Get Started
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Button variant="outline" size="lg" className="border-slate-600/50 text-slate-300 hover:bg-slate-800/70 hover:text-white hover:border-slate-500/50 px-8 py-3 rounded-lg font-semibold backdrop-blur-sm transition-all duration-300 hover:shadow-lg hover:shadow-slate-500/20">
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gradient-to-r from-slate-900/80 via-slate-800/60 to-slate-900/80 backdrop-blur-sm border-y border-slate-700/30">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {stats.map((stat, index) => (
              <div key={stat.label} className="text-center group">
                <div className="text-3xl font-bold text-white md:text-4xl bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent group-hover:scale-110 transition-transform duration-300 animate-shimmer">
                  {stat.value}
                </div>
                <div className="mt-2 text-sm text-slate-400 md:text-base group-hover:text-slate-300 transition-colors duration-300">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gradient-to-b from-slate-900/20 via-slate-800/30 to-slate-900/20 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white sm:text-4xl bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
              Powerful Features for Modern Businesses
            </h2>
            <p className="mt-4 text-lg text-slate-400">
              Everything you need to monitor, analyze, and act on social media intelligence
            </p>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <div key={feature.title} style={{ animationDelay: `${index * 0.1}s` }} className="animate-fade-in-up">
                <Card className="h-full bg-slate-800/40 backdrop-blur-lg border border-slate-700/30 hover:bg-slate-800/60 hover:border-slate-600/40 transition-all duration-500 transform hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/15 group dark-glass">
                  <CardHeader>
                    <div className={`inline-flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-r from-slate-700 to-slate-600 border border-slate-600/30 backdrop-blur-sm group-hover:scale-110 transition-transform duration-300`}>
                      <feature.icon className={`h-6 w-6 ${feature.color} group-hover:brightness-110`} />
                    </div>
                    <CardTitle className="text-white group-hover:text-blue-200 transition-colors duration-300">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-slate-300 group-hover:text-slate-200 transition-colors duration-300">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Analytics Dashboard Preview */}
      <section className="py-20 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900">
        <div className="mx-auto max-w-6xl px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
              Live Analytics Dashboard
            </h2>
            <p className="text-slate-400 max-w-2xl mx-auto">
              Real-time social media intelligence with interactive charts and automated insights
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Live Demo */}
            <div className="bg-slate-800/50 backdrop-blur-lg rounded-lg p-6 border border-slate-700/30">
              <LiveDemo />
            </div>

            {/* Platform Distribution */}
            <div className="bg-slate-800/50 backdrop-blur-lg rounded-lg p-6 border border-slate-700/30">
              <h3 className="text-white text-lg font-semibold mb-4">Platform Distribution</h3>
              <div className="space-y-4">
                {[
                  { platform: 'Twitter', percentage: 45, color: 'bg-blue-500' },
                  { platform: 'LinkedIn', percentage: 30, color: 'bg-blue-600' },
                  { platform: 'Facebook', percentage: 15, color: 'bg-blue-700' },
                  { platform: 'Instagram', percentage: 10, color: 'bg-purple-500' }
                ].map((item) => (
                  <div key={item.platform} className="flex items-center justify-between">
                    <span className="text-slate-300 text-sm">{item.platform}</span>
                    <div className="flex items-center space-x-2 flex-1 ml-4">
                      <div className="flex-1 bg-slate-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${item.color} transition-all duration-1000`}
                          style={{ width: `${item.percentage}%` }}
                        ></div>
                      </div>
                      <span className="text-slate-400 text-xs w-8">{item.percentage}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(59,130,246,0.05),transparent_70%)]" />
        <div className="mx-auto max-w-4xl px-6 lg:px-8 text-center relative">
          <div className="rounded-2xl bg-gradient-to-r from-slate-800/60 via-slate-700/70 to-slate-800/60 p-8 md:p-12 border border-slate-600/20 backdrop-blur-xl shadow-2xl shadow-blue-500/10 gradient-border">
            <h2 className="text-3xl font-bold text-white sm:text-4xl mb-4 bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
              Ready to Transform Your Business Intelligence?
            </h2>
            <p className="text-lg text-slate-300 mb-8">
              Join hundreds of companies already using our AI-powered platform to stay ahead of social media trends and business opportunities.
            </p>
            <Link href="/login">
              <Button size="lg" className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-3 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl shadow-blue-500/25 hover:shadow-blue-500/40 border border-blue-400/30 backdrop-blur-sm">
                Start Your Free Trial
                <Zap className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}