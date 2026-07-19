import type { Analysis, Sentiment } from "../types";

const SENTIMENT_STYLES: Record<Sentiment, string> = {
  positive: "bg-emerald-500/15 text-emerald-300 ring-emerald-500/30",
  neutral: "bg-slate-500/15 text-slate-300 ring-slate-500/30",
  negative: "bg-rose-500/15 text-rose-300 ring-rose-500/30",
};

interface Props {
  analysis: Analysis;
  onDelete: (id: string) => void;
}

export default function AnalysisCard({ analysis, onDelete }: Props) {
  return (
    <article className="rounded-xl border border-slate-700 bg-slate-800/50 p-5">
      <header className="mb-3 flex items-start justify-between gap-4">
        <span
          className={`rounded-full px-2.5 py-1 text-xs font-medium capitalize ring-1 ${
            SENTIMENT_STYLES[analysis.sentiment]
          }`}
        >
          {analysis.sentiment}
        </span>
        <button
          onClick={() => onDelete(analysis.id)}
          className="text-xs text-slate-500 hover:text-rose-400"
        >
          Delete
        </button>
      </header>

      <p className="mb-3 text-slate-200">{analysis.summary}</p>

      <ul className="mb-4 flex flex-wrap gap-2">
        {analysis.topics.map((topic) => (
          <li
            key={topic.name}
            className="rounded-md bg-slate-700/60 px-2 py-1 text-xs text-slate-300"
          >
            {topic.name}
          </li>
        ))}
      </ul>

      <p className="border-t border-slate-700 pt-3 text-sm text-slate-500 italic">
        "{analysis.text}"
      </p>
    </article>
  );
}