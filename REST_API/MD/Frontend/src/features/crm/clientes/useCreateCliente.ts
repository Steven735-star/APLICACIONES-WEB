// ==============================================================================
// MD Marketing & Diseño — src/features/crm/clientes/useCreateCliente.ts
//
// Hook React Query para creación de clientes.
//
// Responsabilidades:
// - Enviar POST al backend.
// - Crear nuevo cliente.
// - Invalidar caché de clientes.
// - Refrescar automáticamente la tabla.
//
// Uso:
//
// const createCliente = useCreateCliente();
//
// await createCliente.mutateAsync(data);
//
// ==============================================================================

import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

import type {
  ClienteForm,
} from "@/types/api.types";

export function useCreateCliente() {
  const queryClient =
    useQueryClient();

  return useMutation({
    mutationFn: async (
      data: ClienteForm
    ) => {
      const response =
        await api.post(
          ENDPOINTS.CRM.CLIENTES,
          data
        );

      return response.data;
    },

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["clientes"],
      });
    },
  });
}