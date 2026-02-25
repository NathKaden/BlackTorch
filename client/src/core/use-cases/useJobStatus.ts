"use client";
import { useEffect, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import type { Job } from "@/core/domain";
const WS_BASE = process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000";
export function useJobStatus(jobId: string | null) {
  const queryClient = useQueryClient();
  const wsRef = useRef<WebSocket | null>(null);
  const [job, setJob] = useState<Job | null>(null);
  useEffect(() => {
    if (!jobId) return;
    const ws = new WebSocket(`${WS_BASE}/api/v1/ws/jobs/${jobId}`);
    wsRef.current = ws;
    ws.onmessage = (event) => {
      const updatedJob: Job = JSON.parse(event.data);
      setJob(updatedJob);
      queryClient.setQueryData<Job>(["job", jobId], updatedJob);
      if (updatedJob.status === "DONE" || updatedJob.status === "FAILED") {
        ws.close();
      }
    };
    ws.onerror = () => {
      setJob((prev) =>
        prev ? { ...prev, status: "FAILED", errorMessage: "WebSocket error" } : null
      );
    };
    return () => { ws.close(); };
  }, [jobId, queryClient]);
  return job;
}