// ==============================================================================
// MD Marketing & Diseño — src/features/crm/clientes/ClientesPage.tsx
// Pantalla principal de gestión de clientes.
//
// Funcionalidades:
// - Listado de clientes.
// - Búsqueda en tiempo real.
// - Apertura de modal para crear clientes.
// - Consumo centralizado mediante useClientes().
// - Próximamente:
//   • editar cliente
//   • desactivar cliente
//   • paginación avanzada
// ==============================================================================


import { useState } from "react";

import ClienteModal from "./ClienteModal";
import { useClientes } from "./useClientes";
import { useDeleteCliente } from "./useDeleteCliente";

import { useDebounce } from "@/hooks/useDebounce";
import ConfirmModal from "@/components/ConfirmModal";

import { Search, UserPlus, Pencil, Trash2 } from "lucide-react";

export default function ClientesPage() {
  const [search, setSearch] = useState("");
  const [openModal, setOpenModal] = useState(false);

  const [selectedCliente, setSelectedCliente] = useState<any>(null);
  const [clienteToDelete, setClienteToDelete] = useState<any>(null);
  
  

  const debouncedSearch =
    useDebounce(search, 400);

  // Consulta de clientes mediante React Query
  const { data, isLoading } = useClientes(debouncedSearch);
  const deleteCliente = useDeleteCliente();

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">
          Clientes
        </h1>

        <button
          onClick={() => {
            setSelectedCliente(null);
            setOpenModal(true);
          }}
          className="
            flex items-center gap-1.5
            bg-indigo-600 text-white
            text-sm px-3 py-2 rounded-lg
            hover:bg-indigo-700
          "
        >
          <UserPlus size={15} />
          Nuevo cliente
        </button>
      </div>

      {/* Buscador */}
      <div className="relative">
        <Search
          size={15}
          className="
            absolute left-3 top-1/2
            -translate-y-1/2
            text-gray-400
          "
        />

        <input
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
          placeholder="Buscar por nombre, RUC o cédula..."
          className="
            w-full
            pl-9 pr-4 py-2.5
            text-sm
            border border-gray-200
            rounded-lg
            focus:outline-none
            focus:border-indigo-400
            bg-white
          "
        />
      </div>

      {/* Tabla */}
      {isLoading ? (
        <div className="flex justify-center py-12">
          <div
            className="
              animate-spin
              rounded-full
              h-7 w-7
              border-b-2
              border-indigo-600
            "
          />
        </div>
      ) : (
        <div
          className="
            bg-white
            rounded-xl
            border border-gray-100
            overflow-hidden
            shadow-sm
          "
        >
          <table className="w-full text-sm">
            <thead
              className="
                bg-gray-50
                border-b
                border-gray-100
              "
            >
              <tr>
                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">
                  Identificación
                </th>

                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">
                  Razón Social
                </th>

                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 hidden sm:table-cell">
                  Teléfono
                </th>

                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 hidden lg:table-cell">
                  Ciudad
                </th>

                <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500">
                  Estado
                </th>
                <th className="text-center px-4 py-3 text-xs font-semibold text-gray-500">
                  Acciones
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-gray-50">
              {data?.results.length ===
                0 && (
                <tr>
                  <td
                    colSpan={6}
                    className="
                      text-center
                      py-8
                      text-gray-400
                      text-sm
                    "
                  >
                    No hay clientes
                    registrados
                  </td>
                </tr>
              )}

              {data?.results.map(
                (cliente) => (
                  <tr
                    key={cliente.id}
                    className="
                      hover:bg-gray-50
                      cursor-pointer
                      transition-colors
                    "
                  >
                    <td
                      className="
                        px-4 py-3
                        font-mono
                        text-xs
                        text-gray-600
                      "
                    >
                      <span className="text-xs text-gray-400 mr-1">
                        {
                          cliente.tipo_identificacion
                        }
                      </span>

                      {
                        cliente.numero_identificacion
                      }
                    </td>

                    <td className="px-4 py-3 font-medium text-gray-900">
                      {
                        cliente.razon_social
                      }
                    </td>

                    <td className="px-4 py-3 text-gray-600 hidden sm:table-cell">
                      {cliente.telefono_principal ||
                        "—"}
                    </td>

                    <td className="px-4 py-3 text-gray-600 hidden lg:table-cell">
                      {cliente.ciudad ||
                        "—"}
                    </td>

                    <td className="px-4 py-3">
                      <span
                        className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                          cliente.activo
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-600"
                        }`}
                      >
                        {cliente.activo
                          ? "Activo"
                          : "Inactivo"}
                      </span>
                    </td>

                    <td className="px-4 py-3">
                      <div className="flex items-center justify-center gap-2">

                        <button
                          onClick={(e) => {
                            e.stopPropagation();

                            setSelectedCliente(cliente);
                            setOpenModal(true);
                          }}
                          className="
                            p-2 rounded-lg
                            text-indigo-600
                            hover:bg-indigo-50
                          "
                          title="Editar cliente"
                        >
                          <Pencil size={16} />
                        </button>

                        <button
                          onClick={(e) => {
                            e.stopPropagation();

                            setClienteToDelete(cliente);
                          }}
                          className="
                            p-2 rounded-lg
                            text-red-600
                            hover:bg-red-50
                          "
                          title="Desactivar cliente"
                        >
                          <Trash2 size={16} />
                        </button>

                      </div>
                    </td>

                  </tr>
                )
              )}
            </tbody>
          </table>

          {/* Contador */}
          {data &&
            data.count > 0 && (
              <div
                className="
                  px-4 py-3
                  border-t border-gray-100
                  text-xs text-gray-500
                "
              >
                {data.count} cliente
                {data.count !== 1
                  ? "s"
                  : ""}{" "}
                en total
              </div>
            )}
        </div>
      )}

      <ClienteModal
        open={openModal}
        cliente={selectedCliente}
        onClose={() => {
          setOpenModal(false);
          setSelectedCliente(null);
        }}
      />

      <ConfirmModal
        open={!!clienteToDelete}
        title="Desactivar cliente"
        message={
          clienteToDelete
            ? `¿Desea desactivar al cliente "${clienteToDelete.razon_social}"?`
            : ""
        }
        loading={deleteCliente.isPending}
        onConfirm={async () => {
          if (!clienteToDelete) return;

          try {
            await deleteCliente.mutateAsync(
              clienteToDelete.id
            );

            setClienteToDelete(null);
          } catch (error) {
            console.error(error);

            alert(
              "No se pudo desactivar el cliente."
            );
          }
        }}
        onCancel={() =>
          setClienteToDelete(null)
        }
      />
      
    </div>
  );
}