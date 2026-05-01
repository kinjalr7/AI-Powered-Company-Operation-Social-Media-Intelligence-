export function getApiBaseUrl() {
  // Keep a sensible default for local dev/demo.
  // You can override by setting NEXT_PUBLIC_API_URL (e.g. http://localhost:8001)
  return (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001").replace(/\/+$/, "");
}

export function apiUrl(path: string) {
  const base = getApiBaseUrl();
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${base}${normalizedPath}`;
}

