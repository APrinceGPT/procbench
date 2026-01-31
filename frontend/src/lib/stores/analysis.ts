// Analysis State Store

import { writable, derived } from 'svelte/store';
import type { AnalysisResult, ProcessSummary, ProcessTreeNode, TimelineEntry } from '$lib/api/types';

// Analysis state
interface AnalysisState {
  currentAnalysisId: string | null;
  result: AnalysisResult | null;
  processes: ProcessSummary[];
  processTree: ProcessTreeNode[];
  timeline: TimelineEntry[];
  loading: boolean;
  error: string | null;
  uploadProgress: number;
}

const initialState: AnalysisState = {
  currentAnalysisId: null,
  result: null,
  processes: [],
  processTree: [],
  timeline: [],
  loading: false,
  error: null,
  uploadProgress: 0,
};

function createAnalysisStore() {
  const { subscribe, set, update } = writable<AnalysisState>(initialState);

  return {
    subscribe,
    
    // Set analysis ID
    setAnalysisId: (id: string) => {
      update(state => ({ ...state, currentAnalysisId: id }));
    },
    
    // Set analysis result
    setResult: (result: AnalysisResult) => {
      update(state => ({
        ...state,
        result,
        currentAnalysisId: result.analysis_id,
        error: null,
      }));
    },
    
    // Set processes
    setProcesses: (processes: ProcessSummary[]) => {
      update(state => ({ ...state, processes }));
    },
    
    // Set process tree
    setProcessTree: (tree: ProcessTreeNode[]) => {
      update(state => ({ ...state, processTree: tree }));
    },
    
    // Set timeline
    setTimeline: (timeline: TimelineEntry[]) => {
      update(state => ({ ...state, timeline }));
    },
    
    // Set loading state
    setLoading: (loading: boolean) => {
      update(state => ({ ...state, loading }));
    },
    
    // Set error
    setError: (error: string | null) => {
      update(state => ({ ...state, error, loading: false }));
    },
    
    // Set upload progress
    setUploadProgress: (progress: number) => {
      update(state => ({ ...state, uploadProgress: progress }));
    },
    
    // Reset state
    reset: () => {
      set(initialState);
    },
  };
}

export const analysisStore = createAnalysisStore();

// Derived stores for convenience
export const analysisResult = derived(
  analysisStore,
  $state => $state.result
);

export const isLoading = derived(
  analysisStore,
  $state => $state.loading
);

export const hasAnalysis = derived(
  analysisStore,
  $state => $state.result !== null
);

export const flaggedProcesses = derived(
  analysisStore,
  $state => $state.processes.filter(p => p.is_flagged)
);

export const topThreats = derived(
  analysisStore,
  $state => $state.result?.top_threats ?? []
);
