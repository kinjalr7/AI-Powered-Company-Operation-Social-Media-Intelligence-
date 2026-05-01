"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Twitter,
  Linkedin,
  Facebook,
  Instagram,
  Youtube,
  Music,
  Save,
  User,
  Mail,
  Shield,
  Loader2,
  CheckCircle,
  AlertCircle
} from "lucide-react";
import { toast } from "sonner";

interface UserProfile {
  id: number;
  email: string;
  full_name: string;
  plan: string;
  avatar_url?: string;
  social_profiles?: {
    twitter_handle?: string;
    linkedin_profile?: string;
    facebook_profile?: string;
    instagram_handle?: string;
    youtube_channel?: string;
    tiktok_handle?: string;
  };
}

interface SocialProfileForm {
  twitter_handle: string;
  linkedin_profile: string;
  facebook_profile: string;
  instagram_handle: string;
  youtube_channel: string;
  tiktok_handle: string;
}

export default function SettingsPage() {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [socialProfiles, setSocialProfiles] = useState<SocialProfileForm>({
    twitter_handle: "",
    linkedin_profile: "",
    facebook_profile: "",
    instagram_handle: "",
    youtube_channel: "",
    tiktok_handle: ""
  });

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const token = localStorage.getItem("token");

      // Load social profiles from localStorage first
      const savedProfiles = localStorage.getItem("social_profiles");
      if (savedProfiles) {
        setSocialProfiles(JSON.parse(savedProfiles));
      }

      // If user is logged in, try to fetch profile data
      if (token) {
        try {
          const response = await fetch("http://localhost:8001/api/users/profile", {
            headers: {
              "Authorization": `Bearer ${token}`,
            },
          });

          if (response.ok) {
            const userData = await response.json();
            setUser(userData);
            if (userData.social_profiles) {
              setSocialProfiles({
                twitter_handle: userData.social_profiles.twitter_handle || "",
                linkedin_profile: userData.social_profiles.linkedin_profile || "",
                facebook_profile: userData.social_profiles.facebook_profile || "",
                instagram_handle: userData.social_profiles.instagram_handle || "",
                youtube_channel: userData.social_profiles.youtube_channel || "",
                tiktok_handle: userData.social_profiles.tiktok_handle || ""
              });
            }
          } else {
            // Use demo data if API fails
            setUser({
              id: 1,
              email: "demo@example.com",
              full_name: "Demo User",
              plan: "free",
              social_profiles: {}
            });
          }
        } catch (apiError) {
          // Use demo data if API not available
          console.warn("API not available, using demo data:", apiError);
          setUser({
            id: 1,
            email: "demo@example.com",
            full_name: "Demo User",
            plan: "free",
            social_profiles: {}
          });
          toast.info("Using demo data - backend API not available");
        }
      } else {
        // No token - use guest/demo mode
        setUser({
          id: 0,
          email: "guest@example.com",
          full_name: "Guest User",
          plan: "free",
          social_profiles: {}
        });
      }
    } catch (error) {
      console.error("Failed to load profile:", error);
      // Even on error, allow access to settings
      setUser({
        id: 0,
        email: "guest@example.com",
        full_name: "Guest User",
        plan: "free",
        social_profiles: {}
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSocialProfiles = async () => {
    setSaving(true);
    try {
      const token = localStorage.getItem("token");

      // Always save to localStorage
      localStorage.setItem("social_profiles", JSON.stringify(socialProfiles));

      if (token) {
        try {
          const response = await fetch("http://localhost:8001/api/users/social-profiles", {
            method: "PUT",
            headers: {
              "Authorization": `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(socialProfiles),
          });

          if (response.ok) {
            toast.success("Social profiles updated successfully!");
            fetchUserProfile(); // Refresh data
          } else {
            const error = await response.json();
            toast.error(error.detail || "Failed to update social profiles on server");
            toast.info("Profiles saved locally");
          }
        } catch (apiError) {
          // API not available, but localStorage save succeeded
          console.warn("API not available, saved locally:", apiError);
          toast.success("Social profiles saved locally");
        }
      } else {
        // Not logged in - just save locally
        toast.success("Social profiles saved locally");
      }
    } catch (error) {
      toast.error("Failed to save social profiles");
    } finally {
      setSaving(false);
    }
  };

  const handleClearSocialProfiles = async () => {
    if (!confirm("Are you sure you want to clear all social media profiles?")) {
      return;
    }

    try {
      const token = localStorage.getItem("token");

      // Always clear from localStorage
      localStorage.removeItem("social_profiles");
      setSocialProfiles({
        twitter_handle: "",
        linkedin_profile: "",
        facebook_profile: "",
        instagram_handle: "",
        youtube_channel: "",
        tiktok_handle: ""
      });

      if (token) {
        try {
          const response = await fetch("http://localhost:8001/api/users/social-profiles", {
            method: "DELETE",
            headers: {
              "Authorization": `Bearer ${token}`,
            },
          });

          if (response.ok) {
            toast.success("Social profiles cleared");
            fetchUserProfile();
          } else {
            toast.error("Failed to clear social profiles on server");
            toast.info("Profiles cleared locally");
          }
        } catch (apiError) {
          // API not available, but localStorage clear succeeded
          console.warn("API not available, cleared locally:", apiError);
          toast.success("Social profiles cleared locally");
        }
      } else {
        // Not logged in - just clear locally
        toast.success("Social profiles cleared locally");
      }
    } catch (error) {
      toast.error("Failed to clear social profiles");
    }
  };

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'twitter': return Twitter;
      case 'linkedin': return Linkedin;
      case 'facebook': return Facebook;
      case 'instagram': return Instagram;
      case 'youtube': return Youtube;
      case 'tiktok': return Music;
      default: return User;
    }
  };

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case 'twitter': return 'text-blue-400';
      case 'linkedin': return 'text-blue-600';
      case 'facebook': return 'text-blue-500';
      case 'instagram': return 'text-pink-400';
      case 'youtube': return 'text-red-400';
      case 'tiktok': return 'text-slate-400';
      default: return 'text-slate-400';
    }
  };

  const socialPlatforms = [
    { key: 'twitter_handle', name: 'Twitter', placeholder: '@username', icon: 'twitter' },
    { key: 'linkedin_profile', name: 'LinkedIn', placeholder: 'https://linkedin.com/in/username', icon: 'linkedin' },
    { key: 'facebook_profile', name: 'Facebook', placeholder: 'https://facebook.com/username', icon: 'facebook' },
    { key: 'instagram_handle', name: 'Instagram', placeholder: '@username', icon: 'instagram' },
    { key: 'youtube_channel', name: 'YouTube', placeholder: 'https://youtube.com/@channel', icon: 'youtube' },
    { key: 'tiktok_handle', name: 'TikTok', placeholder: '@username', icon: 'tiktok' }
  ];

  const hasAnySocialProfiles = Object.values(socialProfiles).some(value => value.trim() !== "");

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">System Settings</h1>
          <p className="text-slate-400 mt-2">Manage your account configuration and intelligence node connections</p>
        </div>

        {/* Profile Information */}
        <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl overflow-hidden">
          <div className="h-1 w-full bg-gradient-to-r from-blue-500 to-indigo-500" />
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <User className="h-5 w-5 text-blue-400" />
              Node Identity
            </CardTitle>
            <CardDescription className="text-slate-500">
              {user?.id ? "Your core system identity" : "Guest node - updates saved to local buffer only"}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-slate-400">Registry Email</Label>
                <Input
                  id="email"
                  value={user?.email || ""}
                  disabled
                  className="bg-slate-900/50 border-slate-700 text-slate-300 pointer-events-none"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="full_name" className="text-slate-400">Operator Name</Label>
                <Input
                  id="full_name"
                  value={user?.full_name || ""}
                  disabled
                  className="bg-slate-900/50 border-slate-700 text-slate-300 pointer-events-none"
                />
              </div>
            </div>
            <div className="flex items-center gap-3">
              <Badge variant="outline" className="capitalize border-blue-500/30 bg-blue-500/10 text-blue-400 px-3">
                {user?.plan || 'Standard'} Protocol
              </Badge>
              {!user?.id && (
                <Badge variant="outline" className="text-amber-400 border-amber-500/30 bg-amber-500/10 px-3">
                  Volatile Session
                </Badge>
              )}
            </div>
            {!user?.id && (
              <div className="bg-blue-500/5 border border-blue-500/20 rounded-xl p-4 mt-4">
                <div className="flex items-start gap-4">
                  <div className="p-2 bg-blue-500/10 rounded-lg mt-0.5">
                    <User className="h-5 w-5 text-blue-400" />
                  </div>
                  <div>
                    <h4 className="text-sm font-medium text-white">Persistent Sync Required</h4>
                    <p className="text-sm text-slate-400 mt-1 leading-relaxed">
                      Your identity configurations are currently buffered locally. Sign in to synchronize with the main-frame and enable multi-node persistence.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Social Media Profiles */}
        <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl overflow-hidden">
          <div className="h-1 w-full bg-gradient-to-r from-purple-500 to-pink-500" />
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Shield className="h-5 w-5 text-purple-400" />
              Intelligence Connections
            </CardTitle>
            <CardDescription className="text-slate-500">
              Configure external data nodes for deep-stream intelligence analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {socialPlatforms.map((platform) => {
                  const Icon = getPlatformIcon(platform.icon);
                  const hasValue = socialProfiles[platform.key as keyof SocialProfileForm]?.trim();

                  return (
                    <div key={platform.key} className="space-y-2">
                      <Label htmlFor={platform.key} className="flex items-center gap-2 text-slate-300 font-medium">
                        <div className={`p-1.5 rounded-md bg-slate-900/50 border border-slate-700`}>
                          <Icon className={`h-4 w-4 ${getPlatformColor(platform.icon)}`} />
                        </div>
                        {platform.name}
                        {hasValue && <CheckCircle className="h-3.5 w-3.5 text-green-400 ml-auto" />}
                      </Label>
                      <Input
                        id={platform.key}
                        placeholder={platform.placeholder}
                        value={socialProfiles[platform.key as keyof SocialProfileForm]}
                        onChange={(e) => setSocialProfiles(prev => ({
                          ...prev,
                          [platform.key]: e.target.value
                        }))}
                        className="bg-slate-900/50 border-slate-700 text-white placeholder:text-slate-600 focus:ring-purple-500/20"
                      />
                    </div>
                  );
                })}
              </div>

              <Separator className="bg-slate-700" />

              <div className="flex gap-4">
                <Button
                  onClick={handleSaveSocialProfiles}
                  disabled={saving}
                  className="flex items-center gap-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white shadow-lg shadow-purple-500/20 border-none"
                >
                  {saving ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Save className="h-4 w-4" />
                  )}
                  Apply Node Changes
                </Button>

                {hasAnySocialProfiles && (
                  <Button
                    variant="outline"
                    onClick={handleClearSocialProfiles}
                    className="border-slate-700 text-slate-400 hover:text-rose-400 hover:border-rose-500/50 hover:bg-rose-500/5"
                  >
                    Wipe Node Config
                  </Button>
                )}
              </div>

              {!hasAnySocialProfiles && (
                <div className="bg-purple-500/5 border border-purple-500/20 rounded-xl p-4 mt-4">
                  <div className="flex items-start gap-4">
                    <div className="p-2 bg-purple-500/10 rounded-lg mt-0.5">
                      <AlertCircle className="h-5 w-5 text-purple-400" />
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-white">Node Deconfigured</h4>
                      <p className="text-sm text-slate-400 mt-1 leading-relaxed">
                        No external intelligence nodes are currently connected. Data streams will be limited to public datasets only.
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Account Actions */}
        <Card className="bg-slate-800/90 backdrop-blur-md border border-slate-700 shadow-xl overflow-hidden">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-white">
              <Shield className="h-5 w-5 text-emerald-400" />
              Security Protocols
            </CardTitle>
            <CardDescription className="text-slate-500">
              Manage system authentication and access security
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Button variant="outline" className="w-full justify-start border-slate-700 text-slate-300 hover:bg-slate-700/50 hover:text-white transition-all">
                <Mail className="h-4 w-4 mr-2 text-blue-400" />
                Update Communication Relay
              </Button>
              <Button variant="outline" className="w-full justify-start border-slate-700 text-slate-300 hover:bg-slate-700/50 hover:text-white transition-all">
                <Shield className="h-4 w-4 mr-2 text-emerald-400" />
                Initialize Password Reset
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}