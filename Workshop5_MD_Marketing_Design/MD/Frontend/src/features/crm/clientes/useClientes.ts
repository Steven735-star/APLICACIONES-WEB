// ==============================================================================
// MD Marketing & Diseño — src/features/crm/clientes/useClientes.ts
// Hook React Query para consultar clientes desde el backend.
//
// Responsabilidades:
// - Obtener listado paginado de clientes.
// - Aplicar búsqueda por texto.
// - Cachear resultados mediante React Query.
// - Reutilizable en cualquier pantalla del CRM.
// ==============================================================================

import { useQuery } from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

import type {
  PaginatedResponse,
  ClienteList,
} from "@/types/api.types";

export function useClientes(
  search?: string
) {
  return useQuery<
    PaginatedResponse<ClienteList>
  >({
    queryKey: ["clientes", search],

    queryFn: async () => {
      const response = await api.get(
        ENDPOINTS.CRM.CLIENTES,
        {
          params: {
            search:
              search || undefined,
          },
        }
      );

      return response.data;
    },
  });
}