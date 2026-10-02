// ==============================================================================
// MD Marketing & Diseño — src/features/crm/clientes/useUpdateCliente.ts
//
// Hook React Query para actualización de clientes.
//
// Responsabilidades:
// - Enviar PATCH al backend.
// - Actualizar información de un cliente existente.
// - Invalidar caché de clientes.
// - Refrescar automáticamente la tabla.
//
// Uso:
//
// const updateCliente = useUpdateCliente();
//
// await updateCliente.mutateAsync({
//   id: cliente.id,
//   data,
// });
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

interface UpdateClientePayload {
  id: number;
  data: ClienteForm;
}

export function useUpdateCliente() {
  const queryClient =
    useQueryClient();

  return useMutation({
    mutationFn: async ({
      id,
      data,
    }: UpdateClientePayload) => {
      const response =
        await api.patch(
          ENDPOINTS.CRM.CLIENTE(id),
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