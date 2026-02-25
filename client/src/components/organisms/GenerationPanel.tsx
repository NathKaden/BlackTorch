"use client";
import { useState } from "react";
import { Progress, Card, CardBody } from "@heroui/react";
import { SearchBar } from "@/components/molecules";
import { ModelBadge } from "@/components/atoms";
import { ThreeCanvas } from "./ThreeCanvas";
import { useGenerateModel } from "@/core/use-cases/useGenerateModel";
import { useJobStatus } from "@/core/use-cases/useJobStatus";
import { createPrompt } from "@/core/domain";
export function GenerationPanel() {
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [glbUrl, setGlbUrl] = useState<string | null>(null);
  const generateMutation = useGenerateModel();
  const job = useJobStatus(activeJobId);
  if (job?.status === "DONE" && activeJobId && !glbUrl) {
    const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    setGlbUrl(`${apiBase}/api/v1/models/${activeJobId}/download`);
  }
  const handleSubmit = async (text: string) => {
    setGlbUrl(null);
    try {
      const prompt = createPrompt(text);
      const result = await generateMutation.mutateAsync(prompt);
      setActiveJobId(result.job_id);
    } catch (e) {
      console.error(e);
    }
  };
  const isGenerating = job?.status === "PENDING" || job?.status === "RUNNING";
  return (
    <div className="flex flex-col gap-6 w-full h-full">
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-orange-400 to-red-600 bg-clip-text text-transparent">
          BlackTorch
        </h1>
        <p className="text-zinc-400 text-sm mt-1">
          3D model generation by AI - optimized RTX
        </p>
      </div>
      <SearchBar
        onSubmit={handleSubmit}
        isLoading={generateMutation.isPending || isGenerating}
      />
      {job && (
        <Card className="bg-zinc-900 border border-zinc-800">
          <CardBody className="flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <span className="text-sm text-zinc-400">Job #{job.id.slice(0, 8)}</span>
              <ModelBadge status={job.status} />
            </div>
            {isGenerating && (
              <Progress value={job.progress} color="warning" size="sm" className="mt-1" />
            )}
            {job.errorMessage && (
              <p className="text-red-400 text-xs">{job.errorMessage}</p>
            )}
          </CardBody>
        </Card>
      )}
      <div className="flex-1 min-h-[400px]">
        <ThreeCanvas glbUrl={glbUrl} />
      </div>
    </div>
  );
}