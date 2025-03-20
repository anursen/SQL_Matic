import { create } from 'zustand';
import axios from 'axios';
import { EvaluationResult } from '../types';

interface EvaluationStore {
  isLoading: boolean;
  error: string | null;
  results: EvaluationResult | null;
  runEvaluation: (numQueries?: number) => Promise<void>;
}

export const useEvaluationStore = create<EvaluationStore>((set) => ({
  isLoading: false,
  error: null,
  results: null,
  
  runEvaluation: async (numQueries?: number) => {
    set({ isLoading: true, error: null });
    
    try {
      const endpoint = numQueries 
        ? `http://localhost:8000/evaluate?num_queries=${numQueries}`
        : 'http://localhost:8000/evaluate';
      
      const response = await axios.get(endpoint);
      
      // Ensure the response data has valid structure
      if (response.data) {
        // Initialize required arrays if they don't exist
        if (!response.data.similarities) {
          response.data.similarities = [];
        }
        if (!response.data.failed_cases) {
          response.data.failed_cases = [];
        }
      }
      
      set({ results: response.data, isLoading: false });
    } catch (error) {
      console.error('Error running evaluation:', error);
      set({ 
        error: error instanceof Error ? error.message : 'Unknown error occurred', 
        isLoading: false 
      });
    }
  }
}));
