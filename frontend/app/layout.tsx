import "./globals.css";
import { APP_NAME } from "@/lib/constants/app";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <div className="container">
          <h1>{APP_NAME}</h1>
          {children}
        </div>
      </body>
    </html>
  );
}
