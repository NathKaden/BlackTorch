"use client";
import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Environment, useGLTF, Center } from "@react-three/drei";
interface ModelProps {
  url: string;
}
function Model({ url }: ModelProps) {
  const { scene } = useGLTF(url);
  return (
    <Center>
      <primitive object={scene} />
    </Center>
  );
}
interface ThreeCanvasProps {
  glbUrl: string | null;
}
export function ThreeCanvas({ glbUrl }: ThreeCanvasProps) {
  if (!glbUrl) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-zinc-900 rounded-xl">
        <p className="text-zinc-500 text-sm">No model loaded</p>
      </div>
    );
  }
  return (
    <div className="w-full h-full rounded-xl overflow-hidden bg-zinc-900">
      <Canvas camera={{ position: [0, 1, 3], fov: 45 }} gl={{ antialias: true }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <Suspense fallback={null}>
          <Model url={glbUrl} />
          <Environment preset="city" />
        </Suspense>
        <OrbitControls autoRotate autoRotateSpeed={1.5} enablePan enableZoom />
      </Canvas>
    </div>
  );
}