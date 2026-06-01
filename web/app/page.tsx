"use client";

import { useState } from "react";

const features = [
  {
    icon: "⌘K",
    title: "OCR Prekladač",
    desc: "Stlač ⌘K, vyber oblasť na obrazovke a app automaticky rozpozná a preloží text.",
  },
  {
    icon: "2×C",
    title: "Prekladač textu",
    desc: "Označ text, stlač ⌘C dvakrát rýchlo za sebou — preklad sa objaví ihneď.",
  },
  {
    icon: "🌍",
    title: "20+ jazykov",
    desc: "Slovenčina, angličtina, nemčina, čeština, francúzština a ďalšie. Automatická detekcia.",
  },
  {
    icon: "📋",
    title: "História prekladov",
    desc: "Všetky preklady uložené lokálne. Vyhľadávaj, kopíruj, mazaj podľa potreby.",
  },
  {
    icon: "🔑",
    title: "Vlastný API kľúč",
    desc: "Používaš svoj vlastný Groq API kľúč — zadarmo, bez limitu na naše servery.",
  },
  {
    icon: "⚡",
    title: "Ultra rýchly",
    desc: "Groq je najrýchlejší AI provider. Preklady za menej ako 500ms.",
  },
];

const steps = [
  {
    num: "01",
    title: "Stiahni aplikáciu",
    desc: 'Stiahni GroqTranslate.zip, rozbaľ a presuň do Applications.',
  },
  {
    num: "02",
    title: "Získaj Groq API kľúč",
    desc: "Zaregistruj sa zadarmo na console.groq.com a vytvor API kľúč. Je to zdarma.",
  },
  {
    num: "03",
    title: "Nastav API kľúč",
    desc: "Klikni na ikonku v menu bare → Nastavenia → vlož API kľúč → Uložiť.",
  },
  {
    num: "04",
    title: "Prekladaj!",
    desc: "⌘K pre OCR alebo dvakrát ⌘C pre výber textu. Hotovo.",
  },
];

export default function Home() {
  const [copied, setCopied] = useState(false);

  const copyGroqLink = () => {
    navigator.clipboard.writeText("https://console.groq.com/keys");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <main className="min-h-screen bg-[#1e1e2e] text-[#e2e8f0]">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#1e1e2e]/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">⚡</span>
            <span className="font-bold text-lg">GroqTranslate</span>
          </div>
          <div className="flex items-center gap-4">
            <a href="#navod" className="text-sm text-[#94a3b8] hover:text-white transition-colors">
              Návod
            </a>
            <a
              href="#stiahnut"
              className="text-sm bg-[#6366f1] hover:bg-[#4f52d4] text-white px-4 py-2 rounded-lg transition-colors"
            >
              Stiahnuť
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-[#6366f1]/10 border border-[#6366f1]/20 rounded-full px-4 py-1.5 mb-8">
            <span className="text-[#6366f1] text-sm">✦</span>
            <span className="text-sm text-[#94a3b8]">Poháňaný Groq AI · Zadarmo · Open Source</span>
          </div>

          <h1 className="text-5xl sm:text-6xl font-bold mb-6 leading-tight">
            Prekladač pre macOS
            <span className="block text-[#6366f1]">jednou skratkou</span>
          </h1>

          <p className="text-xl text-[#94a3b8] mb-10 max-w-2xl mx-auto leading-relaxed">
            Prekladaj výber textu alebo čokoľvek na obrazovke pomocou OCR.
            Rýchly, súkromný, zadarmo — tvoj vlastný Groq API kľúč.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="#stiahnut"
              className="inline-flex items-center justify-center gap-3 bg-[#6366f1] hover:bg-[#4f52d4] text-white font-semibold px-8 py-4 rounded-xl text-lg transition-all hover:scale-105"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Stiahnuť pre macOS
            </a>
            <a
              href="https://github.com/micqej/groq-translate"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-3 bg-white/5 hover:bg-white/10 border border-white/10 text-white font-semibold px-8 py-4 rounded-xl text-lg transition-all"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
              </svg>
              GitHub
            </a>
          </div>

          {/* Shortcut pills */}
          <div className="mt-12 flex flex-wrap justify-center gap-4">
            {[
              { key: "⌘ K", label: "OCR snímka" },
              { key: "⌘ C C", label: "Preložiť výber" },
              { key: "20+", label: "Jazykov" },
              { key: "∞", label: "Prekladov/deň" },
            ].map((item) => (
              <div key={item.key} className="flex items-center gap-3 bg-[#2a2a3e] border border-white/5 rounded-lg px-4 py-3">
                <kbd className="bg-[#1e1e2e] text-[#6366f1] font-mono font-bold text-sm px-2 py-1 rounded">
                  {item.key}
                </kbd>
                <span className="text-sm text-[#94a3b8]">{item.label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-6 bg-[#16162a]">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-3">Všetko čo potrebuješ</h2>
          <p className="text-center text-[#94a3b8] mb-14">Žiadne predplatné. Žiadne limity. Len tvoj Groq kľúč.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <div
                key={f.title}
                className="bg-[#2a2a3e] border border-white/5 rounded-2xl p-6 hover:border-[#6366f1]/30 transition-colors"
              >
                <div className="text-3xl mb-4 font-mono font-bold text-[#6366f1]">{f.icon}</div>
                <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
                <p className="text-[#94a3b8] text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Steps */}
      <section id="navod" className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-3">Ako začať</h2>
          <p className="text-center text-[#94a3b8] mb-14">Nastavenie zaberie menej ako 2 minúty</p>
          <div className="space-y-6">
            {steps.map((step, i) => (
              <div
                key={step.num}
                className="flex gap-6 bg-[#2a2a3e] border border-white/5 rounded-2xl p-6"
              >
                <div className="text-4xl font-black text-[#6366f1]/30 font-mono leading-none pt-1">
                  {step.num}
                </div>
                <div>
                  <h3 className="font-semibold text-lg mb-1">{step.title}</h3>
                  <p className="text-[#94a3b8] text-sm leading-relaxed">{step.desc}</p>
                  {i === 1 && (
                    <button
                      onClick={copyGroqLink}
                      className="mt-3 inline-flex items-center gap-2 text-xs bg-[#6366f1]/10 hover:bg-[#6366f1]/20 text-[#6366f1] border border-[#6366f1]/20 px-3 py-1.5 rounded-lg transition-colors"
                    >
                      {copied ? "✓ Skopírované!" : "console.groq.com/keys"}
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Download */}
      <section id="stiahnut" className="py-20 px-6 bg-[#16162a]">
        <div className="max-w-2xl mx-auto text-center">
          <div className="bg-[#2a2a3e] border border-[#6366f1]/20 rounded-3xl p-10">
            <div className="text-6xl mb-6 animate-float inline-block">⚡</div>
            <h2 className="text-3xl font-bold mb-3">Stiahnuť GroqTranslate</h2>
            <p className="text-[#94a3b8] mb-2">Verzia 1.0 · macOS 12+ · Apple Silicon &amp; Intel</p>
            <p className="text-[#94a3b8] text-sm mb-8">
              Open source · MIT licencia ·{" "}
              <a
                href="https://github.com/micqej/groq-translate"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#6366f1] hover:underline"
              >
                Zdrojový kód na GitHub
              </a>
            </p>

            <a
              href="/GroqTranslate.zip"
              className="inline-flex items-center justify-center gap-3 bg-[#6366f1] hover:bg-[#4f52d4] text-white font-bold px-10 py-4 rounded-xl text-lg transition-all hover:scale-105 mb-6"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Stiahnuť .zip (macOS)
            </a>

            <div className="border-t border-white/5 pt-6 text-left space-y-2">
              <p className="text-xs text-[#94a3b8] font-semibold uppercase tracking-wider mb-3">Požiadavky</p>
              {[
                "macOS 12 Monterey alebo novší",
                "Python 3.10+ (súčasť inštalátora)",
                "Accessibility permission (pre skratky)",
                "Screen Recording permission (pre OCR)",
                "Groq API kľúč (zadarmo na console.groq.com)",
              ].map((r) => (
                <p key={r} className="text-sm text-[#94a3b8] flex items-start gap-2">
                  <span className="text-[#6366f1] mt-0.5">✓</span> {r}
                </p>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-10 px-6 border-t border-white/5">
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="text-xl">⚡</span>
            <span className="font-semibold">GroqTranslate</span>
            <span className="text-[#94a3b8] text-sm">by alukim.sk</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-[#94a3b8]">
            <a href="https://github.com/micqej/groq-translate" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
              GitHub
            </a>
            <a href="https://console.groq.com" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
              Groq Console
            </a>
          </div>
        </div>
      </footer>
    </main>
  );
}
