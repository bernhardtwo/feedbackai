import { useEffect, useState } from "react";
import AnalysisCard from "./components/AnalysisCard";
import AnalysisForm from "./components/AnalysisForm";
import { createAnalysis, deleteAnalysis, listAnalyses } from "./api";
import type { Analysis } from "./types";

export default function App() {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listAnalyses()
      .then(setAnalyses)
      .catch(() => setError("Could not load analyses. Is the API running?"))
      .finally(() => setIsLoading(false));
  }, []);

  const handleCreate = async (text: string) => {
    setIsSubmitting(true);
    setError(null);
    try {
      const created = await createAnalysis(text);
      setAnalyses((current) => [created, ...current]);
    } catch {
      setError("The analysis failed. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    const previous = analyses;
    setAnalyses((current) => current.filter((item) => item.id !== id));
    try {
      await deleteAnalysis(id);
    } catch {
      setAnalyses(previous);
      setError("Could not delete that analysis.");
    }
  };

  return (
    <main className="mx-auto min-h-screen max-w-3xl bg-slate-900 px-6 py-12">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-100">FeedbackAI</h1>
        <p className="mt-1 text-slate-400">
          Paste customer feedback and let AI classify sentiment, extract topics, and summarize it.
        </p>
      </header>

      <AnalysisForm onSubmit={handleCreate} isSubmitting={isSubmitting} />

      {error && (
        <p className="mt-4 rounded-lg border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-300">
          {error}
        </p>
      )}

      <section className="mt-10">
        <h2 className="mb-4 text-lg font-semibold text-slate-200">
          Previous analyses
        </h2>

        {isLoading ? (
          <p className="text-slate-500">Loading…</p>
        ) : analyses.length === 0 ? (
          <p className="text-slate-500">No analyses yet. Submit some feedback above.</p>
        ) : (
          <div className="space-y-4">
            {analyses.map((analysis) => (
              <AnalysisCard
                key={analysis.id}
                analysis={analysis}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}