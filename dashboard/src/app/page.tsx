"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.push("/login");
  }, [router]);

  return (
    <div className="flex h-screen items-center justify-center bg-background text-white">
      <div className="animate-pulse text-xl font-light tracking-widest uppercase">
        Engram
      </div>
    </div>
  );
}
