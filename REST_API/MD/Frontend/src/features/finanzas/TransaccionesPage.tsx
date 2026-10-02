// ==============================================================================
// MD Marketing & Diseño — src/features/finanzas/TransaccionesPage.tsx
// ==============================================================================

import { useQuery } from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

import type {
  PaginatedResponse,
  Transaccion,
} from "@/types/api.types";

export default function TransaccionesPage() {
  const { data, isLoading } = useQuery<
    PaginatedResponse<Transaccion>
  >({
    queryKey: ["transacciones"],
    queryFn: () =>
      api
        .get(ENDPOINTS.FINANZAS.TRANSACCIONES)
        .then((r) => r.data),
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">
          Transacciones
        </h1>

        <button
          className="bg-indigo-600 text-white text-sm px-3 py-2 rounded-lg hover:bg-indigo-700"
        >
          + Nueva transacción
        </button>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-7 w-7 border-b-2 border-indigo-600" />
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-gray-100 overflow-hidden shadow-sm">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b border-gray-100">
              <tr>
                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">
                  Referencia
                </th>

                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">
                  Tipo
                </th>

                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 hidden sm:table-cell">
                  Categoría
                </th>

                <th className="text-right px-4 py-3 text-xs font-semibold text-gray-500">
                  Monto
                </th>

                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 hidden lg:table-cell">
                  Fecha
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-gray-50">
              {data?.results.length === 0 && (
                <tr>
                  <td
                    colSpan={5}
                    className="text-center py-8 text-gray-400 text-sm"
                  >
                    No hay transacciones registradas
                  </td>
                </tr>
              )}

              {data?.results.map((tx) => (
                <tr
                  key={tx.id}
                  className="hover:bg-gray-50 transition-colors"
                >
                  <td className="px-4 py-3 font-mono text-xs">
                    {tx.referencia}
                  </td>

                  <td className="px-4 py-3">
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                        tx.tipo === "ING"
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >
                      {tx.tipo_display}
                    </span>
                  </td>

                  <td className="px-4 py-3 text-gray-600 hidden sm:table-cell">
                    {tx.categoria_nombre}
                  </td>

                  <td className="px-4 py-3 text-right font-semibold text-gray-900">
                    ${Number(tx.monto_flujo_caja).toFixed(2)}
                  </td>

                  <td className="px-4 py-3 text-gray-500 text-xs hidden lg:table-cell">
                    {tx.fecha_emision}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}