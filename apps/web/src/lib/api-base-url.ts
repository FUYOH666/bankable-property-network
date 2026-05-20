export function getApiBaseUrl(): string {
  return (
    process.env.NEXT_PUBLIC_SEABW_API_URL ??
    process.env.NEXT_PUBLIC_BANKABLE_API_URL ??
    "http://localhost:8080"
  );
}
