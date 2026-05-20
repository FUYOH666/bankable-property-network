import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Bankable Property OS",
  description: "Closing Passport demo for bankable Thai property settlement.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
