import { useQuery } from "@tanstack/react-query";

import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";

import type { Orden } from "@/types/api.types";

export function useOrden(id: number | undefined) {
return useQuery({
queryKey: ["orden", id],

enabled: !!id,

queryFn: async () => {
  const response = await api.get<Orden>(
    ENDPOINTS.PRODUCCION.ORDEN(id!)
  );

  return response.data;
},

});
}