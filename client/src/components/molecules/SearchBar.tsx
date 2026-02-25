"use client";
import { useState } from "react";
import { Input } from "@/components/atoms";
import { Button } from "@heroui/react";
interface SearchBarProps {
  onSubmit: (text: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}
export function SearchBar({ onSubmit, isLoading = false, placeholder = "Describe your 3D model..." }: SearchBarProps) {
  const [value, setValue] = useState("");
  const handleSubmit = () => {
    if (value.trim()) onSubmit(value.trim());
  };
  return (
    <div className="flex gap-2 w-full">
      <Input
        value={value}
        onValueChange={setValue}
        placeholder={placeholder}
        onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
        className="flex-1"
        isDisabled={isLoading}
      />
      <Button
        color="primary"
        onPress={handleSubmit}
        isLoading={isLoading}
        isDisabled={!value.trim() || isLoading}
      >
        {isLoading ? "Generating..." : "Generate"}
      </Button>
    </div>
  );
}