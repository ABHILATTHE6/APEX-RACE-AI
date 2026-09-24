import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "APEX-RACE AI",
  description: "Real-time motorsport digital twin and telemetry intelligence.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
