import { useParams } from "react-router-dom";
import { Calendar, DollarSign, User } from "lucide-react";

import { useOrden } from "./useOrdenes";
import StatusBadge from "@/components/StatusBadge";

export default function OrdenDetailPage() {
  const { id } = useParams();

  const ordenId = id ? Number(id) : undefined;

  const {
    data: orden,
    isLoading,
    error,
  } = useOrden(ordenId);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600" />
      </div>
    );
  }

  if (error || !orden) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-red-700 text-sm">
        Error cargando la orden.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
        <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">
              {orden.numero_orden}
            </h1>

            <div className="flex items-center gap-2 mt-2 text-sm text-gray-600">
              <User size={14} />
              {orden.cliente_nombre}
            </div>

            <div className="flex items-center gap-2 mt-1 text-sm text-gray-500">
              <Calendar size={14} />
              Creado: {orden.creado_en}
            </div>
          </div>

          <div className="flex flex-col items-start md:items-end gap-2">
            <StatusBadge
              estado={orden.estado}
              label={orden.estado_display}
            />

            <span
              className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                orden.prioridad === "CRITICA"
                  ? "bg-red-100 text-red-700"
                  : orden.prioridad === "URGENTE"
                  ? "bg-orange-100 text-orange-700"
                  : "bg-gray-100 text-gray-700"
              }`}
            >
              {orden.prioridad}
            </span>
          </div>
        </div>
      </div>

      {/* Resumen financiero */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
          <p className="text-xs font-medium text-gray-500">
            Subtotal
          </p>

          <p className="text-xl font-bold mt-2">
            ${Number(orden.subtotal_neto).toFixed(2)}
          </p>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
          <p className="text-xs font-medium text-gray-500">
            IVA
          </p>

          <p className="text-xl font-bold mt-2">
            ${Number(orden.total_iva).toFixed(2)}
          </p>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4">
          <p className="text-xs font-medium text-gray-500">
            Total
          </p>

          <p className="text-xl font-bold mt-2 flex items-center gap-1">
            <DollarSign size={18} />
            {Number(orden.total_orden).toFixed(2)}
          </p>
        </div>
      </div>

      {/* Descripción */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
        <h2 className="font-semibold text-gray-800 mb-3">
          Descripción General
        </h2>

        <p className="text-sm text-gray-600 whitespace-pre-wrap">
          {orden.descripcion_general || "Sin descripción"}
        </p>
      </div>

      {/* Items */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="px-4 py-3 border-b border-gray-100">
          <h2 className="font-semibold text-gray-800">
            Items de la Orden
          </h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b border-gray-100">
              <tr>
                <th className="text-left px-4 py-3">Código</th>
                <th className="text-left px-4 py-3">Descripción</th>
                <th className="text-right px-4 py-3">Cant.</th>
                <th className="text-right px-4 py-3">Precio</th>
                <th className="text-right px-4 py-3">Total</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-gray-50">
              {orden.items.map((item) => (
                <tr key={item.id}>
                  <td className="px-4 py-3 font-mono text-xs">
                    {item.catalogo_item_codigo}
                  </td>

                  <td className="px-4 py-3">
                    {item.catalogo_item_nombre}
                  </td>

                  <td className="px-4 py-3 text-right">
                    {item.cantidad}
                  </td>

                  <td className="px-4 py-3 text-right">
                    ${Number(item.precio_unitario_neto).toFixed(2)}
                  </td>

                  <td className="px-4 py-3 text-right font-semibold">
                    ${Number(item.monto_total).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Historial */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
        <h2 className="font-semibold text-gray-800 mb-4">
          Historial de Estados
        </h2>

        <div className="space-y-3">
          {orden.historial_estados.map((evento) => (
            <div
              key={evento.id}
              className="border border-gray-100 rounded-lg p-3"
            >
              <div className="font-medium text-sm">
                {evento.estado_anterior || "INICIO"}
                {" → "}
                {evento.estado_nuevo}
              </div>

              <div className="text-xs text-gray-500 mt-1">
                {evento.timestamp}
              </div>

              <div className="text-xs text-gray-600 mt-1">
                {evento.cambiado_por_nombre}
              </div>

              {evento.notas && (
                <div className="text-sm text-gray-700 mt-2">
                  {evento.notas}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Acciones */}
      {orden.transiciones_disponibles.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <h2 className="font-semibold text-gray-800 mb-4">
            Acciones Disponibles
          </h2>

          <div className="flex flex-wrap gap-2">
            {orden.transiciones_disponibles.map((t) => (
              <button
                key={t.accion}
                className="bg-indigo-600 text-white text-sm px-3 py-2 rounded-lg hover:bg-indigo-700"
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}