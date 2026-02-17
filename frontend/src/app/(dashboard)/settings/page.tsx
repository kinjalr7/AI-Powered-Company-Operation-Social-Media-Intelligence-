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
      case 'twitter': return 'text-blue-500';
      case 'linkedin': return 'text-blue-700';
      case 'facebook': return 'text-blue-600';
      case 'instagram': return 'text-pink-500';
      case 'youtube': return 'text-red-500';
      case 'tiktok': return 'text-black';
      default: return 'text-gray-500';
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
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600 mt-2">Manage your account settings and social media profiles</p>
        </div>

        {/* Profile Information */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Profile Information
            </CardTitle>
            <CardDescription>
              {user?.id ? "Your basic account information" : "Guest settings - sign in to save permanently"}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  value={user?.email || ""}
                  disabled
                  className="mt-1"
                />
              </div>
              <div>
                <Label htmlFor="full_name">Full Name</Label>
                <Input
                  id="full_name"
                  value={user?.full_name || ""}
                  disabled
                  className="mt-1"
                />
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="capitalize">
                {user?.plan || 'free'} Plan
              </Badge>
              {!user?.id && (
                <Badge variant="outline" className="text-blue-600 border-blue-600">
                  Guest Mode
                </Badge>
              )}
            </div>
            {!user?.id && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                <div className="flex items-start gap-3">
                  <User className="h-5 w-5 text-blue-600 mt-0.5" />
                  <div>
                    <h4 className="text-sm font-medium text-blue-900">Sign In to Save Permanently</h4>
                    <p className="text-sm text-blue-700 mt-1">
                      Your social media profiles are currently saved locally. Sign in to sync with your account and access all features.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Social Media Profiles */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Social Media Profiles
            </CardTitle>
            <CardDescription>
              Connect your social media accounts for personalized analysis and insights
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {socialPlatforms.map((platform) => {
                const Icon = getPlatformIcon(platform.icon);
                const hasValue = socialProfiles[platform.key as keyof SocialProfileForm]?.trim();

                return (
                  <div key={platform.key} className="space-y-2">
                    <Label htmlFor={platform.key} className="flex items-center gap-2">
                      <Icon className={`h-4 w-4 ${getPlatformColor(platform.icon)}`} />
                      {platform.name}
                      {hasValue && <CheckCircle className="h-4 w-4 text-green-500" />}
                    </Label>
                    <Input
                      id={platform.key}
                      placeholder={platform.placeholder}
                      value={socialProfiles[platform.key as keyof SocialProfileForm]}
                      onChange={(e) => setSocialProfiles(prev => ({
                        ...prev,
                        [platform.key]: e.target.value
                      }))}
                      className="mt-1"
                    />
                  </div>
                );
              })}

              <Separator />

              <div className="flex gap-4">
                <Button
                  onClick={handleSaveSocialProfiles}
                  disabled={saving}
                  className="flex items-center gap-2"
                >
                  {saving ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Save className="h-4 w-4" />
                  )}
                  Save Profiles
                </Button>

                {hasAnySocialProfiles && (
                  <Button
                    variant="outline"
                    onClick={handleClearSocialProfiles}
                    className="text-red-600 hover:text-red-700 hover:bg-red-50"
                  >
                    Clear All
                  </Button>
                )}
              </div>

              {!hasAnySocialProfiles && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                    <div>
                      <h4 className="text-sm font-medium text-blue-900">Add Your Social Media Profiles</h4>
                      <p className="text-sm text-blue-700 mt-1">
                        Connect your social media accounts to unlock personalized AI analysis and insights about your online presence.
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Account Actions */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Account Actions
            </CardTitle>
            <CardDescription>
              Additional account management options
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Button variant="outline" className="w-full justify-start">
                <Mail className="h-4 w-4 mr-2" />
                Change Email
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Shield className="h-4 w-4 mr-2" />
                Change Password
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}