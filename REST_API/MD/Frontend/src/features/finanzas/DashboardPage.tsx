// ==============================================================================
// MD Marketing & Diseño — src/features/finanzas/DashboardPage.tsx
// ==============================================================================

import { useQuery } from "@tanstack/react-query";
import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";
import type { DashboardData } from "@/types/api.types";
import {
  TrendingUp, TrendingDown, DollarSign,
  Percent, AlertTriangle, CheckCircle,
  ClipboardList, Paintbrush, Hammer, Package
} from "lucide-react";

// ── Componente de tarjeta KPI ─────────────────────────────────────────────────
function KpiCard({
  label, value, icon: Icon, color, sub,
}: {
  label:  string;
  value:  string;
  icon:   React.ElementType;
  color:  string;
  sub?:   string;
}) {
  return (
    <div className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
      <div className="flex items-start justify-between mb-3">
        <p className="text-xs font-medium text-gray-500">{label}</p>
        <div className={`p-1.5 rounded-lg ${color}`}>
          <Icon size={15} className="text-white" />
        </div>
      </div>
      <p className="text-xl font-bold text-gray-900">{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-0.5">{sub}</p>}
    </div>
  );
}

// ── Componente de estado de orden ─────────────────────────────────────────────
const ESTADO_CONFIG: Record<string, { label: string; icon: React.ElementType; color: string }> = {
  COTIZADO:       { label: "Cotizado",        icon: ClipboardList, color: "bg-gray-100 text-gray-700" },
  PENDIENTE_PAGO: { label: "Pend. Pago",      icon: DollarSign,    color: "bg-amber-100 text-amber-700" },
  EN_DISENIO:     { label: "En Diseño",       icon: Paintbrush,    color: "bg-blue-100 text-blue-700" },
  EN_PRODUCCION:  { label: "Producción",      icon: Hammer,        color: "bg-purple-100 text-purple-700" },
  LISTO_ENTREGA:  { label: "Listo",           icon: Package,       color: "bg-teal-100 text-teal-700" },
  ENTREGADO:      { label: "Entregado",       icon: CheckCircle,   color: "bg-green-100 text-green-700" },
  CANCELADO:      { label: "Cancelado",       icon: AlertTriangle, color: "bg-red-100 text-red-700" },
};

export default function DashboardPage() {
  const { data, isLoading, error } = useQuery<DashboardData>({
    queryKey:  ["dashboard"],
    queryFn:   () => api.get(ENDPOINTS.FINANZAS.DASHBOARD).then((r) => r.data),
    refetchInterval: 60_000,   // Refrescar cada minuto
  });

  if (isLoading) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
    </div>
  );

  if (error) return (
    <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700 text-sm">
      Error cargando el panel de control. Verifica tu conexión.
    </div>
  );

  if (!data) return null;

  const { finanzas, produccion, mes_actual } = data;
  const periodo = `${mes_actual.inicio} → ${mes_actual.fin}`;

  return (
    <div className="space-y-6">

      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-gray-900">Panel de control</h1>
        <p className="text-sm text-gray-500 mt-0.5">Período: {periodo}</p>
      </div>

      {/* KPIs financieros */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-3">
        <KpiCard
          label="Ingresos Brutos"
          value={`$${Number(finanzas.ingresos_brutos).toFixed(2)}`}
          icon={TrendingUp}
          color="bg-green-500"
          sub="flujo de caja real"
        />
        <KpiCard
          label="Egresos Totales"
          value={`$${Number(finanzas.egresos_totales).toFixed(2)}`}
          icon={TrendingDown}
          color="bg-red-500"
          sub="gastos operativos"
        />
        <KpiCard
          label="Utilidad Neta"
          value={`$${Number(finanzas.utilidad_neta).toFixed(2)}`}
          icon={DollarSign}
          color={Number(finanzas.utilidad_neta) >= 0 ? "bg-indigo-500" : "bg-red-600"}
          sub={`Margen: ${finanzas.margen_porcentaje}%`}
        />
        <KpiCard
          label="Saldo IVA (SRI)"
          value={`$${Number(finanzas.saldo_iva).toFixed(2)}`}
          icon={Percent}
          color={finanzas.a_pagar_sri ? "bg-orange-500" : "bg-teal-500"}
          sub={finanzas.a_pagar_sri ? "A pagar al SRI" : "Crédito tributario"}
        />
      </div>

      {/* Producción por estado */}
      <div>
        <h2 className="text-sm font-semibold text-gray-700 mb-3">
          Órdenes activas por estado
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
          {Object.entries(produccion).map(([estado, count]) => {
            const cfg = ESTADO_CONFIG[estado];
            if (!cfg) return null;
            const Icon = cfg.icon;
            return (
              <div
                key={estado}
                className={`flex items-center gap-2 px-3 py-2.5 rounded-lg ${cfg.color}`}
              >
                <Icon size={14} />
                <div className="min-w-0">
                  <p className="text-xs font-medium truncate">{cfg.label}</p>
                  <p className="text-lg font-bold leading-none">{count}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}