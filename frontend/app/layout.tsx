import "./globals.css";

export const metadata = {
  title: "BMCI AIPro",
  description: "BIST Master Cycle Intelligence",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
      <body>{children}</body>
    </html>
  );
}
