"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Mail,
  Lock,
  User,
  Sparkles,
  Check,
  ArrowRight,
  Brain,
  TrendingUp,
  Users,
  Database,
  Zap
} from "lucide-react";
import Link from "next/link";

const plans = [
  {
    id: "free",
    name: "Free",
    price: 0,
    description: "Perfect for getting started",
    features: [
      "5 social accounts monitoring",
      "Basic sentiment analysis",
      "Weekly reports",
      "Community support"
    ],
    limits: {
      socialAccounts: 5,
      reports: 1,
      apiCalls: 1000,
      storage: "1GB"
    },
    icon: Users,
    color: "from-blue-500 to-cyan-500"
  },
  {
    id: "pro",
    name: "Pro",
    price: 29,
    description: "Advanced analytics for growing businesses",
    features: [
      "25 social accounts monitoring",
      "Advanced NLP analysis",
      "Daily AI reports",
      "Priority support",
      "Real-time alerts",
      "Custom dashboards"
    ],
    limits: {
      socialAccounts: 25,
      reports: 7,
      apiCalls: 10000,
      storage: "10GB"
    },
    icon: TrendingUp,
    color: "from-purple-500 to-pink-500",
    popular: true
  },
  {
    id: "enterprise",
    name: "Enterprise",
    price: 99,
    description: "Full-suite solution for large organizations",
    features: [
      "Unlimited social accounts",
      "Enterprise NLP models",
      "Real-time AI insights",
      "24/7 premium support",
      "Custom integrations",
      "Advanced security",
      "Multi-user access"
    ],
    limits: {
      socialAccounts: -1, // unlimited
      reports: -1, // unlimited
      apiCalls: -1, // unlimited
      storage: "Unlimited"
    },
    icon: Database,
    color: "from-orange-500 to-red-500"
  }
];

export default function LoginPage() {
  const [currentStep, setCurrentStep] = useState<"auth" | "plans">("auth");
  const [selectedPlan, setSelectedPlan] = useState<string>("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));

    setIsLoading(false);
    setCurrentStep("plans");
  };

  const handlePlanSelection = (planId: string) => {
    setSelectedPlan(planId);
    // Redirect to dashboard after selection
    setTimeout(() => {
      window.location.href = "/dashboard";
    }, 1000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-black via-gray-900 to-black">
      <div className="w-full max-w-4xl">
        <AnimatePresence mode="wait">
          {currentStep === "auth" ? (
            <motion.div
              key="auth"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <Card className="modern-card border border-slate-700/50 shadow-2xl shadow-blue-500/10">
                <CardHeader className="text-center pb-8">
                  <motion.div
                    initial={{ scale: 0.8 }}
                    animate={{ scale: 1 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                    className="mx-auto mb-4 h-16 w-16 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/25"
                  >
                    <Brain className="h-8 w-8 text-white" />
                  </motion.div>
                  <CardTitle className="text-3xl font-bold text-white">
                    Welcome to AI Social Intelligence
                  </CardTitle>
                  <CardDescription className="text-slate-300 text-lg">
                    Sign in to access your AI-powered analytics dashboard
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <form onSubmit={handleLogin} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="email" className="text-slate-300">Email</Label>
                      <div className="relative">
                        <Mail className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                        <Input
                          id="email"
                          type="email"
                          placeholder="Enter your email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          className="pl-10 bg-slate-800/70 border-slate-600 text-white placeholder-slate-400 focus:border-blue-400 focus:ring-blue-400/20 backdrop-blur-sm"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password" className="text-slate-300">Password</Label>
                      <div className="relative">
                        <Lock className="absolute left-3 top-3 h-5 w-5 text-slate-400" />
                        <Input
                          id="password"
                          type="password"
                          placeholder="Enter your password"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          className="pl-10 bg-slate-800/70 border-slate-600 text-white placeholder-slate-400 focus:border-blue-400 focus:ring-blue-400/20 backdrop-blur-sm"
                          required
                        />
                      </div>
                    </div>
                    <Button
                      type="submit"
                      className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40"
                      disabled={isLoading}
                    >
                      {isLoading ? (
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                          className="mr-2"
                        >
                          <Zap className="h-5 w-5" />
                        </motion.div>
                      ) : (
                        <>
                          Sign In
                          <ArrowRight className="ml-2 h-5 w-5" />
                        </>
                      )}
                    </Button>
                  </form>

                  <div className="text-center">
                    <p className="text-slate-400">
                      Don't have an account?{" "}
                      <button className="text-blue-400 hover:text-blue-300 font-semibold">
                        Sign up
                      </button>
                    </p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ) : (
            <motion.div
              key="plans"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <div className="text-center mb-8">
                <motion.div
                  initial={{ scale: 0.8 }}
                  animate={{ scale: 1 }}
                  transition={{ duration: 0.5 }}
                  className="mx-auto mb-4 h-16 w-16 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/25"
                >
                  <Sparkles className="h-8 w-8 text-white" />
                </motion.div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  Choose Your Plan
                </h1>
                <p className="text-slate-400">
                  Select the perfect plan for your business intelligence needs
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {plans.map((plan, index) => (
                  <motion.div
                    key={plan.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                  >
                    <Card
                      className={`relative modern-card border border-slate-700/50 shadow-xl cursor-pointer transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/10 ${
                        selectedPlan === plan.id ? "ring-2 ring-blue-400 border-blue-400" : ""
                      } ${plan.popular ? "neon-border" : ""}`}
                      onClick={() => handlePlanSelection(plan.id)}
                    >
                      {plan.popular && (
                        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                          <Badge className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-3 py-1">
                            Most Popular
                          </Badge>
                        </div>
                      )}

                      <CardHeader className="text-center pb-4">
                        <div className={`inline-flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-r ${plan.color} mx-auto mb-4 shadow-lg`}>
                          <plan.icon className="h-6 w-6 text-white" />
                        </div>
                        <CardTitle className="text-white text-xl">{plan.name}</CardTitle>
                        <div className="mt-2">
                          <span className="text-3xl font-bold text-white">
                            ${plan.price}
                          </span>
                          <span className="text-slate-400 text-sm">/month</span>
                        </div>
                        <CardDescription className="text-slate-300 mt-2">
                          {plan.description}
                        </CardDescription>
                      </CardHeader>

                      <CardContent className="space-y-4">
                        <ul className="space-y-3">
                          {plan.features.map((feature, featureIndex) => (
                            <motion.li
                              key={featureIndex}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ duration: 0.3, delay: featureIndex * 0.1 }}
                              className="flex items-center text-slate-300"
                            >
                              <Check className="h-4 w-4 text-green-400 mr-3 flex-shrink-0" />
                              {feature}
                            </motion.li>
                          ))}
                        </ul>

                        <Button
                          className={`w-full mt-6 bg-gradient-to-r ${plan.color} hover:opacity-90 text-white py-3 rounded-lg font-semibold transition-all duration-300 ${
                            selectedPlan === plan.id ? "ring-2 ring-white" : ""
                          }`}
                          onClick={(e) => {
                            e.stopPropagation();
                            handlePlanSelection(plan.id);
                          }}
                        >
                          {selectedPlan === plan.id ? (
                            <>
                              Selected
                              <Check className="ml-2 h-5 w-5" />
                            </>
                          ) : (
                            "Choose Plan"
                          )}
                        </Button>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}