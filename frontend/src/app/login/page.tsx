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
    yearlyPrice: 0,
    description: "Perfect for getting started",
    features: [
      "5 social accounts monitoring",
      "Basic sentiment analysis",
      "Weekly reports",
      "Community support"
    ],
    icon: Users,
    color: "from-blue-500 to-cyan-500",
    buttonColor: "from-blue-500 to-cyan-500"
  },
  {
    id: "pro",
    name: "Pro",
    price: 29,
    yearlyPrice: 24,
    description: "Advanced analytics for growing businesses",
    features: [
      "25 social accounts monitoring",
      "Advanced NLP analysis",
      "Daily AI reports",
      "Priority support",
      "Real-time alerts",
      "Custom dashboards"
    ],
    trial: true,
    popular: true,
    icon: TrendingUp,
    color: "from-purple-500 to-pink-500",
    buttonColor: "from-purple-500 to-pink-500"
  },
  {
    id: "enterprise",
    name: "Enterprise",
    price: 99,
    yearlyPrice: 79,
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
    icon: Database,
    color: "from-orange-500 to-red-500",
    buttonColor: "from-orange-500 to-red-500"
  }
];

export default function LoginPage() {
  const [currentStep, setCurrentStep] = useState<"auth" | "plans">("auth");
  const [selectedPlan, setSelectedPlan] = useState<string>("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isYearly, setIsYearly] = useState(false);

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
      <div className="w-full max-w-6xl">
        <AnimatePresence mode="wait">
          {currentStep === "auth" ? (
            <motion.div
              key="auth"
              className="max-w-md mx-auto"
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
                    className="mx-auto mb-4 h-16 w-16 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/25"
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
                      className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white py-3 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40"
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
              className="py-10"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <div className="text-center mb-16">
                <h1 className="text-5xl font-bold text-white mb-6">
                  Choose Your Plan
                </h1>
                <p className="text-slate-400 text-xl font-light">
                  Select the perfect plan for your business intelligence needs
                </p>

                {/* Billing Toggle (Optional enhancement) */}
                <div className="mt-8 flex items-center justify-center gap-4">
                  <span className={`text-sm ${!isYearly ? 'text-white font-medium' : 'text-slate-500'}`}>Monthly</span>
                  <button
                    onClick={() => setIsYearly(!isYearly)}
                    className="relative w-12 h-6 rounded-full bg-slate-700 transition-colors focus:outline-none"
                  >
                    <div className={`absolute top-1 left-1 w-4 h-4 rounded-full bg-white transition-transform ${isYearly ? 'translate-x-6' : ''}`} />
                  </button>
                  <span className={`text-sm ${isYearly ? 'text-white font-medium' : 'text-slate-500'}`}>Yearly (Save 20%)</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch max-w-7xl mx-auto px-4">
                {plans.map((plan, index) => (
                  <motion.div
                    key={plan.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    className="relative"
                  >
                    {plan.popular && (
                      <div className="absolute -top-4 left-1/2 -translate-x-1/2 z-20">
                        <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-[11px] font-bold px-4 py-1.5 rounded-full shadow-lg border border-purple-400/20 tracking-wide">
                          Most Popular
                        </span>
                      </div>
                    )}

                    <Card
                      className={`h-full bg-slate-900/40 backdrop-blur-xl border border-slate-800 transition-all duration-500 flex flex-col hover:border-slate-700 group ${plan.popular ? "ring-1 ring-blue-500/20 shadow-2xl shadow-blue-500/10" : "shadow-xl"
                        } ${selectedPlan === plan.id ? "ring-2 ring-blue-500 border-blue-500/50 scale-[1.02]" : ""}`}
                      onClick={() => handlePlanSelection(plan.id)}
                    >
                      <CardHeader className="text-center pt-10 pb-6 px-6">
                        <div className={`inline-flex h-14 w-14 items-center justify-center rounded-xl bg-gradient-to-br ${plan.color} mx-auto mb-6 shadow-xl transform group-hover:scale-110 transition-transform duration-300`}>
                          <plan.icon className="h-7 w-7 text-white" />
                        </div>
                        <CardTitle className="text-3xl font-bold text-white mb-2">{plan.name}</CardTitle>
                        <div className="flex items-center justify-center gap-1 mt-4">
                          <span className="text-5xl font-bold text-white tracking-tighter">
                            ${isYearly ? plan.yearlyPrice : plan.price}
                          </span>
                          <span className="text-slate-500 text-lg">/month</span>
                        </div>
                        <CardDescription className="text-slate-400 text-lg mt-4 max-w-[240px] mx-auto min-h-[48px]">
                          {plan.description}
                        </CardDescription>
                      </CardHeader>

                      <CardContent className="flex-grow flex flex-col px-8 pb-10">
                        <div className="w-full h-px bg-slate-800/50 mb-8" />
                        <ul className="space-y-4 mb-10 flex-grow">
                          {plan.features.map((feature, featureIndex) => (
                            <li
                              key={featureIndex}
                              className="flex items-start text-slate-300 group"
                            >
                              <Check className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0 group-hover:scale-110 transition-transform" />
                              <span className="text-[15px] leading-relaxed group-hover:text-white transition-colors">
                                {feature}
                              </span>
                            </li>
                          ))}
                        </ul>

                        <Button
                          className={`w-full py-7 rounded-xl font-bold text-lg transition-all duration-300 bg-gradient-to-r ${plan.buttonColor} hover:opacity-90 hover:scale-[1.02] shadow-xl text-white`}
                          onClick={(e) => {
                            e.stopPropagation();
                            handlePlanSelection(plan.id);
                          }}
                        >
                          {selectedPlan === plan.id ? (
                            <span className="flex items-center gap-2">
                              Selected <Check className="h-6 w-6" />
                            </span>
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