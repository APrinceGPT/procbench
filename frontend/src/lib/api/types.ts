// API Types for ProcBench Frontend

export interface HealthResponse {
  status: string;
  version: string;
  ai_enabled: boolean;
}

export interface SupportedFormatsResponse {
  formats: string[];
  max_file_size_mb: number;
}

export interface AnalysisStartResponse {
  analysis_id: string;
  status: string;
  message: string;
}

export interface ProcessSummary {
  pid: number;
  process_name: string;
  image_path: string | null;
  command_line: string | null;
  parent_pid: number | null;
  parent_name: string | null;
  risk_score: number;
  legitimacy: 'legitimate' | 'suspicious' | 'malicious' | 'unknown';
  behavior_tags: string[];
  is_flagged: boolean;
  matched_rules: string[];
  ai_reasoning: string | null;
  event_count: number;
  file_operations: number;
  registry_operations: number;
  network_operations: number;
}

export interface AnalysisResult {
  analysis_id: string;
  filename: string;
  status: string;
  total_events: number;
  total_processes: number;
  flagged_processes: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  analysis_duration_seconds: number;
  top_threats: ProcessSummary[];
}

export interface ProcessTreeNode {
  process: {
    pid: number;
    process_name: string;
    image_path: string | null;
    risk_score: number;
    legitimacy: string;
    behavior_tags: string[];
    event_count: number;
  };
  depth: number;
  children: ProcessTreeNode[];
}

export interface TimelineEntry {
  timestamp: string | null;
  process_name: string;
  pid: number;
  risk_score: number;
  is_anomaly: boolean;
  description: string;
}

export interface TimelineResponse {
  total: number;
  timeline: TimelineEntry[];
}

export interface ProcessesResponse {
  total: number;
  flagged: number;
  processes: ProcessSummary[];
}

export interface PathHeatmapEntry {
  path: string;
  access_count: number;
  operation_types: Record<string, number>;
  processes: string[];
}

export interface PathHeatmapResponse {
  total_paths: number;
  returned_paths: number;
  total_accesses: number;
  heatmap: PathHeatmapEntry[];
}

// Risk level helpers
export type RiskLevel = 'high' | 'medium' | 'low' | 'none';

export function getRiskLevel(score: number): RiskLevel {
  if (score >= 50) return 'high';
  if (score >= 20) return 'medium';
  if (score > 0) return 'low';
  return 'none';
}

export function getRiskColor(level: RiskLevel): string {
  switch (level) {
    case 'high':
      return 'text-red-600 bg-red-50';
    case 'medium':
      return 'text-orange-600 bg-orange-50';
    case 'low':
      return 'text-yellow-600 bg-yellow-50';
    default:
      return 'text-gray-600 bg-gray-50';
  }
}

export function getLegitimacyColor(legitimacy: string): string {
  switch (legitimacy) {
    case 'malicious':
      return 'text-red-700 bg-red-100';
    case 'suspicious':
      return 'text-orange-700 bg-orange-100';
    case 'legitimate':
      return 'text-green-700 bg-green-100';
    default:
      return 'text-gray-700 bg-gray-100';
  }
}
