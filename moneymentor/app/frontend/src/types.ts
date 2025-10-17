export interface Message {
  id: string;
  role: 'user' | 'mentor';
  content: string;
  sources?: Source[];
  timestamp: Date;
  tool?: 'calculator' | 'rag';
}

export interface Source {
  source: string;
  chunk_id?: number;        // Optional - RAG provides this
  score?: number;           // Optional - RAG provides this
  relevance_score?: number; // Optional - Calculator provides this
  text: string;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
  query: string;
  model: string;
  tool: 'calculator' | 'rag';
}

