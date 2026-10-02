// ==============================================================================
// MD Marketing & Diseño — src/main.tsx
// Punto de entrada — registra todos los providers globales
// ==============================================================================

import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { router } from "./router";
import "./index.css";

// React Query — configuración global de caché y reintentos
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry:              1,          // Reintentar 1 vez ante error de red
      staleTime:          1000 * 30,  // 30s antes de refetch en background
      refetchOnWindowFocus: false,    // No refetch al volver a la pestaña
    },
    mutations: {
      retry: 0,
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
);