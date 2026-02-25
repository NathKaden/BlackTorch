"use client";
import { Chip } from "@heroui/react";
import type { JobStatus } from "@/core/domain";
const statusConfig: Record<JobStatus, { color: "default" | "warning" | "success" | "danger"; label: string }> = {
  PENDING: { color: "default", label: "Pending" },
  RUNNING: { color: "warning", label: "Generating..." },
  DONE:    { color: "success", label: "Done" },
  FAILED:  { color: "danger",  label: "Failed" },
};
interface ModelBadgeProps {
  status: JobStatus;
}
export function ModelBadge({ status }: ModelBadgeProps) {
  const { color, label } = statusConfig[status];
  return (
    <Chip color={color} variant="flat" size="sm">
      {label}
    </Chip>
  );
}