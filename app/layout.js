import { Manrope } from "next/font/google";
import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "Taller 4 · Arquitectura AWS segura, disponible y escalable",
  description:
    "Presentación del taller: 8 actividades de AWS — Well-Architected, EC2, ALB, CloudWatch, Trusted Advisor y Auto Scaling.",
};

const manrope = Manrope({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800"],
  variable: "--font-manrope",
});

export default function RootLayout({ children }) {
  return (
    <html
      lang="es"
      data-scroll-behavior="smooth"
      className={`${manrope.variable} dark`}
      data-theme="dark"
    >
      <body>
        <header className="site-header">
          <Link href="/" className="brand">
            <span className="logo-mark">
              <span className="mi">bolt</span>
            </span>
            taller 4
          </Link>
          <nav className="nav">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
              <Link key={n} href={`/actividades/${n}`} className="nav-link">
                {n}
              </Link>
            ))}
          </nav>
          <Link href="/" className="btn-white">
            Inicio
          </Link>
        </header>
        <main className="main">{children}</main>
        <footer className="site-footer">
          <Link href="/" className="footer-brand">
            <span className="logo-mark sm">
              <span className="mi">bolt</span>
            </span>{" "}
            taller 4 · aws
          </Link>
          <span className="footer-links">
            <Link href="/actividades/1">Actividades</Link>
            <span>·</span>
            <span>© 2026 Taller 4</span>
          </span>
        </footer>
      </body>
    </html>
  );
}
