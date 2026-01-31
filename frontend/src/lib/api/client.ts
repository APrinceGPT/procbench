// API Client for ProcBench Backend

import type {
  HealthResponse,
  SupportedFormatsResponse,
  AnalysisStartResponse,
  AnalysisResult,
  ProcessesResponse,
  ProcessTreeNode,
  TimelineResponse,
} from './types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Fetch wrapper with error handling
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Accept': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

/**
 * API Client class for all backend interactions
 */
export class ApiClient {
  /**
   * Check backend health status
   */
  async getHealth(): Promise<HealthResponse> {
    return fetchApi<HealthResponse>('/health');
  }

  /**
   * Get supported file formats
   */
  async getSupportedFormats(): Promise<SupportedFormatsResponse> {
    return fetchApi<SupportedFormatsResponse>('/supported-formats');
  }

  /**
   * Upload and analyze a Process Monitor log file
   */
  async analyzeFile(file: File): Promise<AnalysisStartResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE}/analyze`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  /**
   * Get analysis results by ID
   */
  async getAnalysis(analysisId: string): Promise<AnalysisResult> {
    return fetchApi<AnalysisResult>(`/analysis/${analysisId}`);
  }

  /**
   * Get all processes from an analysis
   */
  async getProcesses(
    analysisId: string,
    options: {
      flaggedOnly?: boolean;
      minRisk?: number;
      limit?: number;
    } = {}
  ): Promise<ProcessesResponse> {
    const params = new URLSearchParams();
    if (options.flaggedOnly) params.set('flagged_only', 'true');
    if (options.minRisk !== undefined) params.set('min_risk', options.minRisk.toString());
    if (options.limit !== undefined) params.set('limit', options.limit.toString());

    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchApi<ProcessesResponse>(`/analysis/${analysisId}/processes${query}`);
  }

  /**
   * Get process tree from an analysis
   */
  async getProcessTree(analysisId: string): Promise<{ tree: ProcessTreeNode[] }> {
    return fetchApi<{ tree: ProcessTreeNode[] }>(`/analysis/${analysisId}/tree`);
  }

  /**
   * Get timeline from an analysis
   */
  async getTimeline(
    analysisId: string,
    options: { anomaliesOnly?: boolean; limit?: number } = {}
  ): Promise<TimelineResponse> {
    const params = new URLSearchParams();
    if (options.anomaliesOnly !== undefined) {
      params.set('anomalies_only', options.anomaliesOnly.toString());
    }
    if (options.limit !== undefined) {
      params.set('limit', options.limit.toString());
    }

    const query = params.toString() ? `?${params.toString()}` : '';
    return fetchApi<TimelineResponse>(`/analysis/${analysisId}/timeline${query}`);
  }

  /**
   * Download PDF report for an analysis
   */
  async downloadReport(analysisId: string): Promise<Blob> {
    const response = await fetch(`${API_BASE}/analysis/${analysisId}/report`);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Download failed' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.blob();
  }

  /**
   * Delete an analysis
   */
  async deleteAnalysis(analysisId: string): Promise<void> {
    await fetchApi<{ status: string }>(`/analysis/${analysisId}`, {
      method: 'DELETE',
    });
  }
}

// Export a singleton instance
export const api = new ApiClient();
