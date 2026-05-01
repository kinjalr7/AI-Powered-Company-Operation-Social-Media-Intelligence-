"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  BarChart3,
  Brain,
  TrendingUp,
  Users,
  FileText,
  PieChart,
  Settings,
  LogOut,
  Menu,
  X
} from "lucide-react";
import { useState } from "react";

const navigation = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: BarChart3,
    description: "Real-time analytics overview"
  },
  {
    name: "Analytics",
    href: "/analytics",
    icon: Brain,
    description: "Advanced AI analytics"
  },
  {
    name: "Reports",
    href: "/reports",
    icon: FileText,
    description: "Generated reports & insights"
  },
  {
    name: "Charts",
    href: "/charts",
    icon: PieChart,
    description: "Interactive visualizations"
  },
  {
    name: "Social Data",
    href: "/social-data",
    icon: Users,
    description: "Social media monitoring"
  }
];

export function Navbar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-slate-900/95 backdrop-blur-md border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-2 rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI Social Intelligence
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 group",
                    isActive
                      ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/25"
                      : "text-slate-300 hover:bg-slate-800/50 hover:text-white"
                  )}
                >
                  <Icon className={cn(
                    "h-4 w-4",
                    isActive ? "text-white" : "text-slate-400 group-hover:text-blue-400"
                  )} />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>

          {/* Desktop Settings & Logout */}
          <div className="hidden md:flex items-center space-x-4">
            <Link
              href="/settings"
              className={cn(
                "p-2 rounded-lg text-sm font-medium transition-all duration-200 group",
                pathname === "/settings"
                  ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/25"
                  : "text-slate-400 hover:text-blue-400 hover:bg-slate-800/50"
              )}
            >
              <Settings className="h-5 w-5" />
            </Link>
            <button className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-800/50 rounded-lg transition-colors">
              <LogOut className="h-5 w-5" />
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-800/50 rounded-lg transition-colors"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      {isOpen && (
        <div className="md:hidden bg-slate-900/95 backdrop-blur-md border-t border-slate-700">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className={cn(
                    "flex items-center space-x-3 px-3 py-3 rounded-lg text-base font-medium transition-all duration-200",
                    isActive
                      ? "bg-gradient-to-r from-blue-500 to-purple-600 text-white"
                      : "text-slate-300 hover:bg-slate-800/50 hover:text-white"
                  )}
                >
                  <Icon className={cn(
                    "h-5 w-5",
                    isActive ? "text-white" : "text-slate-400"
                  )} />
                  <div>
                    <div className={isActive ? "text-white" : "text-white"}>
                      {item.name}
                    </div>
                    <div className={cn(
                      "text-sm",
                      isActive ? "text-blue-200" : "text-slate-400"
                    )}>
                      {item.description}
                    </div>
                  </div>
                </Link>
              );
            })}
            <div className="border-t border-slate-700 mt-4 pt-4 flex space-x-4">
              <Link
                href="/settings"
                onClick={() => setIsOpen(false)}
                className="flex items-center space-x-2 p-2 text-slate-400 hover:text-blue-400 hover:bg-slate-800/50 rounded-lg transition-colors flex-1"
              >
                <Settings className="h-5 w-5" />
                <span>Settings</span>
              </Link>
              <button className="flex items-center space-x-2 p-2 text-slate-400 hover:text-red-400 hover:bg-slate-800/50 rounded-lg transition-colors flex-1">
                <LogOut className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}