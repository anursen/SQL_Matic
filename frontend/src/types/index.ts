export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: number;
}

export interface Chat {
  id: string;
  title: string;
  timestamp: number;
  messages: Message[];
}

export interface BackendMetrics {
  tokenUsage: number;
  inferenceSpeed: number;
  activeTools: string[];
}

export interface EvaluationCase {
  query_id: number;
  query: string;
  ground_truth_sql: string;
  assistant_sql: string;
  similarity: number;
  error?: string;
}

export interface EvaluationResult {
  total_queries: number;
  successful_queries: number;
  failed_queries: number;
  average_similarity: number;
  median_similarity: number;
  min_similarity: number;
  max_similarity: number;
  success_rate: number;
  similarities: EvaluationCase[];
  failed_cases: EvaluationCase[];
  execution_time: number;
  error?: string;
}
