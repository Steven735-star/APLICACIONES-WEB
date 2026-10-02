// ==============================================================================
// src/features/crm/catalogo/useUpdateCatalogo.ts
// Actualizar item del catálogo.
// ==============================================================================

import { useMutation, useQueryClient } from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

import type { CatalogoForm } from "@/types/api.types";

export function useUpdateCatalogo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      id,
      data,
    }: {
      id: number;
      data: CatalogoForm;
    }) => {
      const response = await api.put(
        ENDPOINTS.CRM.CATALOGO_ITEM(id),
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