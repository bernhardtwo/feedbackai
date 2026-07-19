export type Sentiment = "positive" | "neutral" | "negative";

export interface Topic {
  name: string;
}

export interface Analysis {
  id: string;
  text: string;
  sentiment: Sentiment;
  summary: string;
  topics: Topic[];
  created_at: string;
}