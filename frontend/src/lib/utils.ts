import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(date);
}

export function formatNumber(num: number): string {
  return new Intl.NumberFormat("en-US", {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(num);
}

export function generateRandomData(length: number) {
  return Array.from({ length }, (_, i) => ({
    id: i + 1,
    value: Math.floor(Math.random() * 1000),
    date: new Date(Date.now() - i * 24 * 60 * 60 * 1000),
  }));
}

export function calculateSentimentScore(sentiment: string): number {
  switch (sentiment.toLowerCase()) {
    case "positive":
      return 1;
    case "negative":
      return -1;
    case "neutral":
    default:
      return 0;
  }
}