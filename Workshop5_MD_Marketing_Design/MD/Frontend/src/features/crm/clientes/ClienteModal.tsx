// ==============================================================================
// MD Marketing & Diseño — src/features/crm/clientes/ClienteModal.tsx
//
// Modal reutilizable para creación y edición de clientes.
//
// Responsabilidades:
// - Mostrar formulario de cliente.
// - Crear nuevos clientes.
// - Editar clientes existentes.
// - Mostrar errores devueltos por la API.
// - Gestionar estados de carga.
//
// Flujo:
//
// ClientesPage
//      │
//      ▼
// ClienteModal
//      │
//      ▼
// ClienteForm
//      │
//      ▼
// useCreateCliente / useUpdateCliente
//      │
//      ▼
// Django REST API
//
// Notas:
// - Si recibe un cliente, entra en modo edición.
// - Si no recibe cliente, entra en modo creación.
// - Los errores del backend se muestran dentro del formulario.
// ==============================================================================


import ClienteForm from "./ClienteForm";
import { useEffect, useState } from "react";
import { useCreateCliente } from "./useCreateCliente";
import { useUpdateCliente } from "./useUpdateCliente";

import type {
  Cliente,
  ClienteForm as ClienteFormData,
} from "@/types/api.types";

interface ClienteModalProps {
  open: boolean;
  onClose: () => void;
  cliente?: Cliente | null;
}

export default function ClienteModal({
  open,
  onClose,
  cliente = null,
}: ClienteModalProps) {
  const createMutation = useCreateCliente();
  const updateMutation = useUpdateCliente();

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) {
      setError(null);
    }
  }, [open]);


  if (!open) return null;

  const isEditing = !!cliente;

  const handleSubmit = async (
    data: ClienteFormData
  ) => {
    setError(null);
    try {
      if (isEditing && cliente) {
        await updateMutation.mutateAsync({
          id: cliente.id,
          data,
        });
      } else {
        await createMutation.mutateAsync(data);
      }

      onClose();
    } catch (err: unknown) {
        console.error(err);
        const apiError = (err as any)?.response?.data;
        if (typeof apiError === "object") {
            const firstKey = Object.keys(apiError)[0];
            if (
            firstKey &&
            Array.isArray(apiError[firstKey])
            ) {
            setError(apiError[firstKey][0]);
            return;
            }
        }

        setError("No se pudo guardar el cliente.");
    }
  };

  const loading =
    createMutation.isPending ||
    updateMutation.isPending;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-3xl p-6 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold">
            {isEditing
              ? "Editar Cliente"
              : "Nuevo Cliente"}
          </h2>

          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-800"
          >
            ✕
          </button>
        </div>

        <ClienteForm
            initialData={cliente}
            loading={loading}
            error={error}
            onSubmit={handleSubmit}
        />
      </div>
    </div>
  );
}