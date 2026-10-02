// ==============================================================================
// src/features/crm/catalogo/CatalogoPage.tsx
// Pantalla principal de gestión del catálogo.
// ==============================================================================

import { useState } from "react";

import {
  Search,
  Plus,
  Pencil,
  Trash2,
} from "lucide-react";

import CatalogoModal from "./CatalogoModal";
import { useCatalogo } from "./useCatalogo";
import { useDeleteCatalogo } from "./useDeleteCatalogo";

import ConfirmModal from "@/components/ConfirmModal";
import { useDebounce } from "@/hooks/useDebounce";

export default function CatalogoPage() {
  const [search, setSearch] =
    useState("");

  const [openModal, setOpenModal] =
    useState(false);

  const [selectedItem, setSelectedItem] =
    useState<any>(null);

  const [itemToDelete, setItemToDelete] =
    useState<any>(null);

  const debouncedSearch =
    useDebounce(search, 400);

  const {
    data,
    isLoading,
  } = useCatalogo(
    debouncedSearch
  );

  const deleteItem =
    useDeleteCatalogo();

  return (
    <div className="space-y-4">

      {/* Header */}

      <div className="flex items-center justify-between">

        <h1 className="text-xl font-bold">

          Catálogo

        </h1>

        <button
          onClick={() => {
            setSelectedItem(null);
            setOpenModal(true);
          }}
          className="
            flex items-center gap-2
            bg-indigo-600
            text-white
            px-3 py-2
            rounded-lg
            hover:bg-indigo-700
          "
        >
          <Plus size={16} />

          Nuevo ítem

        </button>

      </div>

      {/* Buscador */}

      <div className="relative">

        <Search
          size={16}
          className="
            absolute
            left-3
            top-1/2
            -translate-y-1/2
            text-gray-400
          "
        />

        <input
          value={search}
          onChange={(e) =>
            setSearch(
              e.target.value
            )
          }
          placeholder="Buscar..."
          className="
            w-full
            pl-10
            py-2.5
            border
            rounded-lg
          "
        />

      </div>

      {/* Tabla */}

      {isLoading ? (

        <div className="py-20 flex justify-center">

          Cargando...

        </div>

      ) : (

        <div
          className="
            bg-white
            rounded-xl
            shadow-sm
            overflow-hidden
          "
        >

          <table className="w-full text-sm">

            <thead className="bg-gray-50">

              <tr>

                <th className="px-4 py-3 text-left">

                  Código

                </th>

                <th className="px-4 py-3 text-left">

                  Nombre

                </th>

                <th className="px-4 py-3 text-left">

                  Naturaleza

                </th>

                <th className="px-4 py-3 text-left">

                  Precio

                </th>

                <th className="px-4 py-3 text-center">

                  Acciones

                </th>

              </tr>

            </thead>

            <tbody>

              {data?.results.map(
                (item) => (

                  <tr
                    key={item.id}
                    className="border-t"
                  >

                    <td className="px-4 py-3">

                      {item.codigo}

                    </td>

                    <td className="px-4 py-3">

                      {item.nombre}

                    </td>

                    <td className="px-4 py-3">

                      {item.naturaleza_display}

                    </td>

                    <td className="px-4 py-3">

                      ${item.precio_base_unitario}

                    </td>

                    <td className="px-4 py-3">

                      <div className="flex justify-center gap-2">

                        <button
                          onClick={() => {
                            setSelectedItem(
                              item
                            );

                            setOpenModal(
                              true
                            );
                          }}
                        >
                          <Pencil
                            size={16}
                          />
                        </button>

                        <button
                          onClick={() =>
                            setItemToDelete(
                              item
                            )
                          }
                        >
                          <Trash2
                            size={16}
                          />
                        </button>

                      </div>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      )}

      <CatalogoModal
        open={openModal}
        item={selectedItem}
        onClose={() => {
          setOpenModal(false);
          setSelectedItem(null);
        }}
      />

      <ConfirmModal
        open={
          !!itemToDelete
        }
        title="Desactivar ítem"
        message={
          itemToDelete
            ? `¿Desea desactivar "${itemToDelete.nombre}"?`
            : ""
        }
        loading={
          deleteItem.isPending
        }
        onConfirm={async () => {
          await deleteItem.mutateAsync(
            itemToDelete.id
          );

          setItemToDelete(
            null
          );
        }}
        onCancel={() =>
          setItemToDelete(
            null
          )
        }
      />

    </div>
  );
}