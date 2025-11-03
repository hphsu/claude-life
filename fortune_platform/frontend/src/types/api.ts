// Profile types
export interface Profile {
  id: string;
  name: string;
  birth_date: string; // YYYY-MM-DD
  birth_time: string; // HH:MM
  birth_location: string;
  gender: 'M' | 'F' | 'O';
  timezone: string;
  created_at: string;
  updated_at: string;
}

export interface CreateProfileInput {
  name: string;
  birth_date: string;
  birth_time: string;
  birth_location: string;
  gender: 'M' | 'F' | 'O';
  timezone?: string;
}

export interface UpdateProfileInput extends Partial<CreateProfileInput> {
  id: string;
}

// Expert system types
export type ExpertSystem =
  | 'bazi'
  | 'ziwei'
  | 'astrology'
  | 'numerology'
  | 'plum_blossom'
  | 'qimen'
  | 'liuyao'
  | 'name_analysis';

export interface ExpertSystemInfo {
  id: ExpertSystem;
  name: string;
  description: string;
  price: number;
  estimated_time: number; // in seconds
}

// Order types
export interface Order {
  id: string;
  profile_id: string;
  expert_systems: ExpertSystem[];
  total_price: number;
  discount_applied: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
}

export interface CreateOrderInput {
  profile_id: string;
  expert_systems: ExpertSystem[];
}

// Job types
export interface Job {
  id: string;
  order_id: string;
  expert_system: ExpertSystem;
  status: 'queued' | 'running' | 'completed' | 'failed';
  progress: number; // 0-100
  started_at?: string;
  completed_at?: string;
  error_message?: string;
}

export interface JobStatus {
  job_id: string;
  status: Job['status'];
  progress: number;
  result_available: boolean;
}

// Report types
export interface Report {
  id: string;
  job_id: string;
  profile_id: string;
  expert_system: ExpertSystem;
  created_at: string;
}

export interface ReportContent {
  report_id: string;
  expert_system: ExpertSystem;
  html_content: string; // Sanitized HTML from backend
  metadata: {
    generated_at: string;
    version: string;
    [key: string]: any;
  };
}

// Pagination types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiErrorResponse {
  detail?: string;
  message?: string;
  errors?: Record<string, string[]>;
}
