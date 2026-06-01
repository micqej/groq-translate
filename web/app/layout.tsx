import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "GroqTranslate — Rýchly AI prekladač pre macOS",
  description:
    "Bezplatný macOS prekladač poháňaný Groq AI. Prekladaj výber textu skratkou alebo OCR snímkou obrazovky. Funguje s tvojim vlastným Groq API kľúčom.",
  openGraph: {
    title: "GroqTranslate — Rýchly AI prekladač pre macOS",
    description: "Prekladaj čokoľvek na obrazovke jednou klávesovou skratkou.",
    url: "https://preklad.alukim.sk",
    siteName: "GroqTranslate",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="sk">
      <body>{children}</body>
    </html>
  );
}
