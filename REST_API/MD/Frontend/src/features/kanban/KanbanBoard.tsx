// ==============================================================================
// MD Marketing & Diseño — src/features/kanban/KanbanBoard.tsx
// Tablero Kanban de órdenes de producción
// ==============================================================================

import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";
import type { KanbanData, OrdenList } from "@/types/api.types";
import { Clock, AlertTriangle, DollarSign } from "lucide-react";

// ── Colores por prioridad ─────────────────────────────────────────────────────
const PRIORIDAD_BADGE: Record<string, string> = {
  NORMAL:  "bg-gray-100 text-gray-600",
  URGENTE: "bg-orange-100 text-orange-700",
  CRITICA: "bg-red-100 text-red-700",
};

// ── Colores del header de columna ─────────────────────────────────────────────
const COLUMNA_COLOR: Record<string, string> = {
  COTIZADO:       "border-t-gray-400",
  PENDIENTE_PAGO: "border-t-amber-400",
  EN_DISENIO:     "border-t-blue-400",
  EN_PRODUCCION:  "border-t-purple-500",
  LISTO_ENTREGA:  "border-t-teal-400",
};

// ── Tarjeta de Orden ──────────────────────────────────────────────────────────
function OrdenCard({ orden }: { orden: OrdenList }) {
  const vencida = orden.fecha_compromiso
    ? new Date(orden.fecha_compromiso) < new Date()
    : false;

  return (
    <Link
      to={`/ordenes/${orden.id}`}
      className="block bg-white rounded-lg border border-gray-200 p-3
                 hover:border-indigo-300 hover:shadow-sm transition-all"
    >
      <div className="flex items-start justify-between mb-1.5">
        <span className="text-xs font-mono text-gray-500">{orden.numero_orden}</span>
        <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${PRIORIDAD_BADGE[orden.prioridad]}`}>
          {orden.prioridad}
        </span>
      </div>

      <p className="text-sm font-medium text-gray-900 truncate mb-2">
        {orden.cliente_nombre}
      </p>

      <div className="flex items-center justify-between text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <DollarSign size={11} />
          ${Number(orden.total_orden).toFixed(2)}
        </span>

        {orden.fecha_compromiso && (
          <span className={`flex items-center gap-1 ${vencida ? "text-red-500" : ""}`}>
            {vencida && <AlertTriangle size={11} />}
            <Clock size={11} />
            {orden.fecha_compromiso}
          </span>
        )}
      </div>

      {orden.dias_en_estado > 3 && (
        <div className="mt-2 text-xs text-orange-600 bg-orange-50 rounded px-2 py-0.5">
          {orden.dias_en_estado} días en este estado
        </div>
      )}
    </Link>
  );
}

// ── Tablero principal ─────────────────────────────────────────────────────────
export default function KanbanBoard() {
  const { data, isLoading, refetch } = useQuery<KanbanData>({
    queryKey:        ["kanban"],
    queryFn:         () => api.get(ENDPOINTS.PRODUCCION.KANBAN).then((r) => r.data),
    refetchInterval: 30_000,   // Polling cada 30s (WebSocket en Fase 5)
  });

  if (isLoading) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
    </div>
  );

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900">Producción</h1>
          <p className="text-sm text-gray-500">
            {data?.total_activas ?? 0} órdenes activas
          </p>
        </div>
        <button
          onClick={() => refetch()}
          className="text-xs text-indigo-600 hover:text-indigo-800 font-medium"
        >
          Actualizar
        </button>
      </div>

      {/* Columnas Kanban — scroll horizontal en mobile */}
      <div className="flex gap-3 overflow-x-auto pb-4">
        {data?.columnas.map((col) => (
          <div
            key={col.estado}
            className={`flex-shrink-0 w-64 bg-gray-50 rounded-xl
                        border-t-4 ${COLUMNA_COLOR[col.estado] ?? "border-t-gray-300"}`}
          >
            {/* Header columna */}
            <div className="px-3 py-2.5 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <p className="text-sm font-semibold text-gray-700">{col.label}</p>
                <span className="text-xs bg-white border border-gray-200
                                 text-gray-600 rounded-full px-2 py-0.5 font-medium">
                  {col.total}
                </span>
              </div>
            </div>

            {/* Tarjetas */}
            <div className="p-2 space-y-2 min-h-[120px]">
              {col.ordenes.length === 0 ? (
                <p className="text-xs text-gray-400 text-center pt-4">
                  Sin órdenes
                </p>
              ) : (
                col.ordenes.map((orden) => (
                  <OrdenCard key={orden.id} orden={orden} />
                ))
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}