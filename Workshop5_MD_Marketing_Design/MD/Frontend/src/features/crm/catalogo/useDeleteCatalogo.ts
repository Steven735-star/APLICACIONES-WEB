// ==============================================================================
// src/features/crm/catalogo/useDeleteCatalogo.ts
// Desactivar item del catálogo.
// ==============================================================================

import { useMutation, useQueryClient } from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

export function useDeleteCatalogo() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const response = await api.delete(
        ENDPOINTS.CRM.CATALOGO_ITEM(id)
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