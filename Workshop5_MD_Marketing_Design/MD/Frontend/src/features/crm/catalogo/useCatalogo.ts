// ==============================================================================
// src/features/crm/catalogo/useCatalogo.ts
// Consulta del catálogo mediante React Query.
// ==============================================================================

import { useQuery } from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

import type {
  CatalogoItem,
  PaginatedResponse,
} from "@/types/api.types";

export function useCatalogo(search = "") {
  return useQuery({
    queryKey: ["catalogo", search],

    queryFn: async () => {
      const { data } = await api.get<
        PaginatedResponse<CatalogoItem>
      >(ENDPOINTS.CRM.CATALOGO, {
        params: {
          search,
        },
      });

      return data;
    },
  });
}