// ==============================================================================
// MD Marketing & Diseño — src/router.tsx
// Configuración de rutas con React Router v6
// ==============================================================================

import { createBrowserRouter, Navigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";

// Layouts
import Layout from "@/components/Layout";

// Páginas públicas
import LoginPage from "@/features/auth/LoginPage";

// Páginas protegidas
import DashboardPage     from "@/features/finanzas/DashboardPage";
import KanbanBoard       from "@/features/kanban/KanbanBoard";
import ClientesPage      from "@/features/crm/clientes/ClientesPage";
import CatalogoPage from "@/features/crm/catalogo/CatalogoPage";
import OrdenDetailPage   from "@/features/crm/ordenes/OrdenDetailPage";
import TransaccionesPage from "@/features/finanzas/TransaccionesPage";

// Guard: redirige a /login si no hay token
function RequireAuth({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

// Guard: redirige al dashboard si ya está autenticado
function RequireGuest({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  if (isAuthenticated) return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
}

export const router = createBrowserRouter([
  // ── Ruta pública ────────────────────────────────────────────────────────────
  {
    path: "/login",
    element: (
      <RequireGuest>
        <LoginPage />
      </RequireGuest>
    ),
  },

  // ── Rutas protegidas (dentro del Layout con sidebar) ───────────────────────
  {
    path: "/",
    element: (
      <RequireAuth>
        <Layout />
      </RequireAuth>
    ),
    children: [
      // Redirect raíz → dashboard
      { index: true, element: <Navigate to="/dashboard" replace /> },

      // Dashboard financiero
      { path: "dashboard", element: <DashboardPage /> },

      // Kanban de producción
      { path: "kanban", element: <KanbanBoard /> },

      // CRM
      { path: "clientes",          element: <ClientesPage /> },
      { path: "catalogo",          element: <CatalogoPage /> },
      { path: "ordenes/:id",       element: <OrdenDetailPage /> },

      // Finanzas
      { path: "transacciones",     element: <TransaccionesPage /> },
    ],
  },

  // Ruta catch-all
  { path: "*", element: <Navigate to="/dashboard" replace /> },
]);