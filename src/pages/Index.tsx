import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Dropzone } from "@/components/scanner/Dropzone";
import { PreviewCard } from "@/components/scanner/PreviewCard";
import { processDocument, API_URL } from "@/services/api";
import { toast } from "@/hooks/use-toast";
import { Download, Loader2, RotateCcw, ScanLine, Sparkles, Server } from "lucide-react";

const Index = () => {
  const [file, setFile] = useState<File | null>(null);
  const [originalUrl, setOriginalUrl] = useState<string | null>(null);
  const [outputUrl, setOutputUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    return () => {
      if (originalUrl) URL.revokeObjectURL(originalUrl);
      if (outputUrl) URL.revokeObjectURL(outputUrl);
    };
  }, [originalUrl, outputUrl]);

  const handleFile = (f: File) => {
    if (originalUrl) URL.revokeObjectURL(originalUrl);
    if (outputUrl) URL.revokeObjectURL(outputUrl);
    setFile(f);
    setOriginalUrl(URL.createObjectURL(f));
    setOutputUrl(null);
  };

  const handleProcess = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const blob = await processDocument(file);
      const url = URL.createObjectURL(blob);
      if (outputUrl) URL.revokeObjectURL(outputUrl);
      setOutputUrl(url);
      toast({ title: "Document scanned", description: "Your clean copy is ready." });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Something went wrong";
      toast({ title: "Could not process", description: message, variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    if (originalUrl) URL.revokeObjectURL(originalUrl);
    if (outputUrl) URL.revokeObjectURL(outputUrl);
    setFile(null);
    setOriginalUrl(null);
    setOutputUrl(null);
  };

  const handleDownload = () => {
    if (!outputUrl) return;
    const a = document.createElement("a");
    a.href = outputUrl;
    a.download = `autodoc-scan-${Date.now()}.jpg`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  };

  return (
    <div className="min-h-screen bg-[image:var(--gradient-subtle)]">
      {/* Header */}
      <header className="border-b border-border/60 bg-background/80 backdrop-blur-xl sticky top-0 z-10">
        <div className="container flex items-center justify-between py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[image:var(--gradient-hero)] text-primary-foreground shadow-[var(--shadow-elegant)]">
              <ScanLine className="h-5 w-5" />
            </div>
            <div>
              <p className="font-display text-base font-bold text-foreground leading-none">
                AutoDoc Align
              </p>
              <p className="text-[11px] text-muted-foreground mt-0.5">
                Document scanner · OpenCV
              </p>
            </div>
          </div>
          <a
            href="https://github.com"
            className="hidden sm:inline-flex items-center gap-2 rounded-full border border-border bg-background px-3 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
            title={`API: ${API_URL}`}
          >
            <Server className="h-3.5 w-3.5" />
            {API_URL.replace(/^https?:\/\//, "")}
          </a>
        </div>
      </header>

      <main className="container py-12 md:py-16">
        {/* Hero */}
        <section className="mx-auto max-w-2xl text-center animate-fade-in-up">
          <span className="inline-flex items-center gap-1.5 rounded-full border border-border bg-background px-3 py-1 text-xs font-medium text-muted-foreground shadow-[var(--shadow-soft)]">
            <Sparkles className="h-3 w-3 text-primary" />
            Powered by OpenCV perspective transform
          </span>
          <h1 className="mt-5 font-display text-4xl font-bold tracking-tight text-foreground md:text-5xl">
            Turn any photo into a{" "}
            <span className="bg-[image:var(--gradient-hero)] bg-clip-text text-transparent">
              clean scan
            </span>
          </h1>
          <p className="mt-4 text-base text-muted-foreground md:text-lg">
            Upload a tilted document. We auto-detect edges, warp it straight,
            and export an enhanced, aligned copy.
          </p>
        </section>

        {/* Workspace */}
        <section className="mx-auto mt-12 max-w-6xl">
          {!file ? (
            <Dropzone onFile={handleFile} />
          ) : (
            <div className="space-y-6">
              <div className="grid gap-6 md:grid-cols-2">
                <PreviewCard title="Original" badge="Input" src={originalUrl} />
                <PreviewCard
                  title="Scanned"
                  badge="Output"
                  src={outputUrl}
                  placeholder="Click 'Process' to generate"
                />
              </div>

              <div className="flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
                <Button
                  variant="hero"
                  size="lg"
                  onClick={handleProcess}
                  disabled={loading}
                  className="w-full sm:w-auto min-w-[200px]"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin" />
                      Processing…
                    </>
                  ) : (
                    <>
                      <ScanLine className="h-4 w-4" />
                      Process Document
                    </>
                  )}
                </Button>
                {outputUrl && (
                  <Button
                    variant="outline"
                    size="lg"
                    onClick={handleDownload}
                    className="w-full sm:w-auto"
                  >
                    <Download className="h-4 w-4" />
                    Download
                  </Button>
                )}
                <Button
                  variant="ghost"
                  size="lg"
                  onClick={handleReset}
                  className="w-full sm:w-auto"
                >
                  <RotateCcw className="h-4 w-4" />
                  New scan
                </Button>
              </div>
            </div>
          )}

          {/* How it works */}
          <div className="mt-20 grid gap-5 md:grid-cols-3">
            {[
              {
                step: "01",
                title: "Detect edges",
                desc: "Grayscale conversion, CLAHE contrast enhancement, Gaussian blur, and Canny edge detection isolate the page.",
              },
              {
                step: "02",
                title: "Find corners",
                desc: "Largest external contour is approximated to four document corners.",
              },
              {
                step: "03",
                title: "Warp & enhance",
                desc: "Perspective transform with dynamic sizing, then detail enhancement for clarity.",
              },
            ].map((s) => (
              <div
                key={s.step}
                className="rounded-2xl border border-border bg-card p-6 shadow-[var(--shadow-soft)] hover:shadow-[var(--shadow-elegant)] hover:-translate-y-1 transition-all duration-300"
              >
                <span className="font-display text-xs font-bold tracking-widest text-primary">
                  STEP {s.step}
                </span>
                <h3 className="mt-2 font-display text-lg font-semibold text-foreground">
                  {s.title}
                </h3>
                <p className="mt-1.5 text-sm text-muted-foreground">{s.desc}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="border-t border-border/60 mt-16">
        <div className="container py-6 text-center text-xs text-muted-foreground">
          AutoDoc Align · Frontend connects to your Flask + OpenCV backend at{" "}
          <code className="rounded bg-muted px-1.5 py-0.5 text-[11px]">{API_URL}</code>
        </div>
      </footer>
    </div>
  );
};

export default Index;
