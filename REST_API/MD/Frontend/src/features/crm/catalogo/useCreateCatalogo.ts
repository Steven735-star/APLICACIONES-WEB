// ==============================================================================
// src/features/crm/catalogo/useCreateCatalogo.ts
// Crear item del catálogo.
// ==============================================================================

import { useMutation, useQueryClient } from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

import type { CatalogoForm } from "@/types/api.types";

export function useCreateCatalogo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CatalogoForm) => {
      const response = await api.post(
        ENDPOINTS.CRM.CATALOGO,
        data
      );

      return response.data;
    },

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["catalogo"],
      });
    },
  });
}