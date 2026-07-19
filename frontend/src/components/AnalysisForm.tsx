import { useState } from "react";

interface Props {
  onSubmit: (text: string) => Promise<void>;
  isSubmitting: boolean;
}

export default function AnalysisForm({ onSubmit, isSubmitting }: Props) {
  const [text, setText] = useState("");

  const handleSubmit = async () => {
    if (!text.trim()) return;
    await onSubmit(text);
    setText("");
  };

  return (
    <div className="rounded-xl border border-slate-700 bg-slate-800/50 p-5">
      <label htmlFor="feedback" className="mb-2 block text-sm font-medium text-slate-300">
        Customer feedback
      </label>
      <textarea
        id="feedback"
        value={text}
        onChange={(event) => setText(event.target.value)}
        rows={4}
        maxLength={5000}
        placeholder="Paste a review, support ticket, or survey answer…"
        className="w-full resize-y rounded-lg border border-slate-600 bg-slate-900 p-3 text-slate-100 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
      />
      <div className="mt-3 flex items-center justify-between">
        <span className="text-xs text-slate-500">{text.length}/5000</span>
        <button
          onClick={handleSubmit}
          disabled={isSubmitting || !text.trim()}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {isSubmitting ? "Analyzing…" : "Analyze"}
        </button>
      </div>
    </div>
  );
}