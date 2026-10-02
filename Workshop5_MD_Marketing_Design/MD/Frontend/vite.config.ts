// ==============================================================================
// MD Marketing & Diseño — Frontend/vite.config.ts
// ==============================================================================

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      // Permite imports como: import { useAuth } from "@/hooks/useAuth"
      "@": path.resolve(__dirname, "./src"),
    },
  },

  server: {
    host: "0.0.0.0",   // Necesario para Docker
    port: 5173,
    proxy: {
      // Redirige /api/* → Django en puerto 8000
      // Esto elimina problemas de CORS en desarrollo
      "/api": {
        target: "http://web:8000",
        changeOrigin: true,
      },
      // WebSocket Kanban (Fase 5)
      "/ws": {
        target: "ws://web:8000",
        ws: true,
        changeOrigin: true,
      },
    },
  },
});