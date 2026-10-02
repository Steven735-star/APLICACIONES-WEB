// ==============================================================================
// src/features/crm/catalogo/CatalogoModal.tsx
// Modal para crear y editar ítems del catálogo.
// ==============================================================================

import { useState, useEffect } from "react";

import CatalogoForm from "./CatalogoForm";
import { useCreateCatalogo } from "./useCreateCatalogo";
import { useUpdateCatalogo } from "./useUpdateCatalogo";

import type {
  CatalogoItem,
  CatalogoForm as CatalogoFormType,
} from "@/types/api.types";

interface Props {
  open: boolean;

  item: CatalogoItem | null;

  onClose: () => void;
}

export default function CatalogoModal({
  open,
  item,
  onClose,
}: Props) {
  const createMutation =
    useCreateCatalogo();

  const updateMutation =
    useUpdateCatalogo();

  const [form, setForm] =
    useState<CatalogoFormType>({
      codigo: "",

      nombre: "",

      descripcion: "",

      naturaleza: "SVC_DIG",

      unidad_medida: "UND",

      tarifa_iva: "15.00",

      precio_base_unitario: "0.00",

      requiere_dimensiones: false,

      activo: true,
    });

    const [errors, setErrors] = useState<
        Partial<Record<keyof CatalogoFormType, string>>
    >({});

  useEffect(() => {
    if (item) {
      setForm({
        codigo: item.codigo,

        nombre: item.nombre,

        descripcion:
          item.descripcion,

        naturaleza:
          item.naturaleza,

        unidad_medida:
          item.unidad_medida,

        tarifa_iva:
          item.tarifa_iva,

        precio_base_unitario:
          item.precio_base_unitario,

        requiere_dimensiones:
          item.requiere_dimensiones,

        activo:
          item.activo,
      });
    } else {
      setForm({
        codigo: "",

        nombre: "",

        descripcion: "",

        naturaleza: "SVC_DIG",

        unidad_medida: "UND",

        tarifa_iva: "15.00",

        precio_base_unitario:
          "0.00",

        requiere_dimensiones:
          false,

        activo: true,
      });
    }
  }, [item, open]);

  if (!open) return null;

  async function handleSave() {
        const newErrors: Partial<
    Record<keyof CatalogoFormType, string>
    > = {};

    if (!form.codigo.trim()) {
    newErrors.codigo = "El código es obligatorio.";
    }

    if (!form.nombre.trim()) {
    newErrors.nombre = "El nombre es obligatorio.";
    }

    if (!form.naturaleza) {
    newErrors.naturaleza =
        "Seleccione una naturaleza.";
    }

    if (!form.unidad_medida) {
    newErrors.unidad_medida =
        "Seleccione una unidad.";
    }

    if (!form.tarifa_iva) {
    newErrors.tarifa_iva =
        "Seleccione una tarifa IVA.";
    }

    if (
    !form.precio_base_unitario ||
    Number(form.precio_base_unitario) <= 0
    ) {
    newErrors.precio_base_unitario =
        "Ingrese un precio válido.";
    }

    setErrors(newErrors);

    if (Object.keys(newErrors).length > 0) {
    return;
    }
    try {
      if (item) {
        await updateMutation.mutateAsync({
          id: item.id,
          data: form,
        });
      } else {
        await createMutation.mutateAsync(
          form
        );
      }

      onClose();
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div
      className="
        fixed inset-0
        bg-black/40
        flex items-center
        justify-center
        z-50
      "
    >
      <div
        className="
            bg-white
            rounded-2xl
            shadow-2xl
            w-full
            max-w-5xl
            mx-4
            max-h-[92vh]
            overflow-hidden
            flex
            flex-col
        "
        >
        
        <div
            className="
                flex
                items-center
                justify-between
                px-8
                py-6
                border-b
                border-gray-100
            "
            >
            <h2 className="text-2xl font-semibold text-gray-900">
                {item
                ? "Editar ítem"
                : "Nuevo ítem"}
            </h2>

            <button
                onClick={onClose}
                className="
                text-gray-400
                hover:text-gray-700
                text-2xl
                transition-colors
                "
            >
                ×
            </button>
        </div>

        <div
            className="
                flex-1
                overflow-y-auto
                px-8
                py-6
            "
        >

            <CatalogoForm
                form={form}
                setForm={setForm}
                errors={errors}
            />
        </div>

        <div
            className="
                flex
                justify-end
                gap-3
                px-8
                py-5
                border-t
                border-gray-100
                bg-white
            "
        >

          <button
            onClick={onClose}
            className="
              px-4 py-2
              rounded-lg
              border
            "
          >
            Cancelar
          </button>

          <button
            onClick={handleSave}
            className="
              px-4 py-2
              rounded-lg
              bg-indigo-600
              text-white
            "
          >
            {item
              ? "Guardar cambios"
              : "Crear ítem"}

          </button>

        </div>

      </div>
    </div>
  );
}