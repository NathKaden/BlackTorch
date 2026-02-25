import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import type { Job, Prompt } from "@/core/domain";
interface GenerateResponse {
  job_id: string;
}
export function useGenerateModel() {
  const queryClient = useQueryClient();
  return useMutation<GenerateResponse, Error, Prompt>({
    mutationFn: (prompt: Prompt) =>
      api.post<GenerateResponse>("/api/v1/generate", {
        text: prompt.text,
        negative_text: prompt.negativeText,
      }),
    onSuccess: (data) => {
      queryClient.setQueryData<Job>(["job", data.job_id], {
        id: data.job_id,
        promptText: "",
        status: "PENDING",
        progress: 0,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });
    },
  });
}