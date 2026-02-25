export interface Prompt {
  text: string;
  negativeText?: string;
}
export function createPrompt(text: string, negativeText?: string): Prompt {
  if (!text || text.trim().length === 0) {
    throw new Error("Prompt text cannot be empty");
  }
  if (text.length > 1000) {
    throw new Error("Prompt text cannot exceed 1000 characters");
  }
  return { text: text.trim(), negativeText: negativeText?.trim() };
}