"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";

const LoginMiddleware = () => {
  const router = useRouter();
  const pathname = usePathname(); 

  useEffect(() => {
    const user = localStorage.getItem("currentUser");

    if (!user && pathname !== "/login") {
      router.push("/login");
    }
  }, [pathname, router]);  

  return null;
};

export default LoginMiddleware;
