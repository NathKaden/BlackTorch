export type JobStatus = "PENDING" | "RUNNING" | "DONE" | "FAILED";
export interface Job {
  id: string;
  promptText: string;
  status: JobStatus;
  progress: number;
  createdAt: string;
  updatedAt: string;
  errorMessage?: string;
}
export interface ThreeDModel {
  id: string;
  jobId: string;
  glbUrl: string;
  thumbnailUrl?: string;
  promptText: string;
  createdAt: string;
}