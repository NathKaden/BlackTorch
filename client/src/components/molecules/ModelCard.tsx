"use client";
import { Card, CardBody, CardFooter } from "@heroui/react";
import { ModelBadge } from "@/components/atoms";
import type { ThreeDModel } from "@/core/domain";
interface ModelCardProps {
  model: ThreeDModel;
  onClick?: () => void;
}
export function ModelCard({ model, onClick }: ModelCardProps) {
  return (
    <Card
      isPressable={!!onClick}
      onPress={onClick}
      className="w-full max-w-sm hover:scale-[1.02] transition-transform"
    >
      <CardBody className="p-0">
        {model.thumbnailUrl ? (
          <img
            src={model.thumbnailUrl}
            alt={model.promptText}
            className="w-full h-48 object-cover rounded-t-xl"
          />
        ) : (
          <div className="w-full h-48 bg-zinc-800 rounded-t-xl flex items-center justify-center">
            <span className="text-zinc-500 text-sm">No preview</span>
          </div>
        )}
      </CardBody>
      <CardFooter className="flex flex-col items-start gap-1">
        <p className="text-sm font-medium line-clamp-2">{model.promptText}</p>
        <ModelBadge status="DONE" />
        <p className="text-xs text-zinc-500">
          {new Date(model.createdAt).toLocaleDateString()}
        </p>
      </CardFooter>
    </Card>
  );
}