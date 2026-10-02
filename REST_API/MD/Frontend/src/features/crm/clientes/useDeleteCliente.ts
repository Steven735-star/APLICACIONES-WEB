// ==============================================================================
// MD Marketing & Diseño — src/features/crm/clientes/useDeleteCliente.ts
//
// Hook React Query para desactivación de clientes.
//
// IMPORTANTE:
// El backend utiliza Soft Delete.
// El registro NO se elimina físicamente.
//
// DELETE /clientes/{id}/
//
// Resultado:
// activo = false
//
// Responsabilidades:
// - Solicitar desactivación.
// - Invalidar caché.
// - Refrescar listado.
//
// Uso:
//
// const deleteCliente = useDeleteCliente();
//
// await deleteCliente.mutateAsync(cliente.id);
//
// ==============================================================================

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

export function useDeleteCliente() {
  const queryClient =
    useQueryClient();

  return useMutation({
    mutationFn: async (
      id: number
    ) => {
      await api.delete(
        ENDPOINTS.CRM.CLIENTE(id)
      );
    },

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["clientes"],
      });
    },
  });
}