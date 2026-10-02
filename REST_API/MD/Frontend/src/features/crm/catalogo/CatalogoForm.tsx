// ==============================================================================
// src/features/crm/catalogo/CatalogoForm.tsx
// Formulario reutilizable para crear y editar ítems del catálogo.
// ==============================================================================

import type { CatalogoForm } from "@/types/api.types";

interface Props {
  form: CatalogoForm;

  setForm: React.Dispatch<
    React.SetStateAction<CatalogoForm>
  >;

  errors: Partial<
    Record<keyof CatalogoForm, string>
  >;
}

export default function CatalogoForm({
  form,
  setForm,
  errors,
}: Props) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

      {/* Código */}

      <div>

        <label className="block text-sm font-medium text-gray-700 mb-1">
          Código
          <span className="text-red-500 ml-1">*</span>
        </label>

        <input
          value={form.codigo}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              codigo: e.target.value,
            }))
          }
          className={`
            w-full
            rounded-lg
            px-3
            py-2.5
            border
            focus:outline-none
            focus:ring-2
            focus:ring-indigo-200
            ${
              errors.codigo
                ? "border-red-500"
                : "border-gray-300"
            }
          `}
        />

        {errors.codigo && (
          <p className="mt-1 text-xs text-red-600">
            {errors.codigo}
          </p>
        )}

      </div>

      {/* Nombre */}

      <div>

        <label className="block text-sm font-medium text-gray-700 mb-1">
          Nombre
          <span className="text-red-500 ml-1">*</span>
        </label>

        <input
          value={form.nombre}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              nombre: e.target.value,
            }))
          }
          className={`
            w-full
            rounded-lg
            px-3
            py-2.5
            border
            focus:outline-none
            focus:ring-2
            focus:ring-indigo-200
            ${
              errors.nombre
                ? "border-red-500"
                : "border-gray-300"
            }
          `}
        />

        {errors.nombre && (
          <p className="mt-1 text-xs text-red-600">
            {errors.nombre}
          </p>
        )}

      </div>

      {/* Descripción */}

      <div className="md:col-span-2">

        <label className="block text-sm font-medium text-gray-700 mb-1">
          Descripción
        </label>

        <textarea
          rows={4}
          value={form.descripcion}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              descripcion: e.target.value,
            }))
          }
          className="
            w-full
            rounded-lg
            px-3
            py-2.5
            border
            border-gray-300
            focus:outline-none
            focus:ring-2
            focus:ring-indigo-200
          "
        />

      </div>

      {/* Naturaleza */}

      <div>

        <label className="block text-sm font-medium text-gray-700 mb-1">
          Naturaleza
          <span className="text-red-500 ml-1">*</span>
        </label>

        <select
          value={form.naturaleza}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              naturaleza: e.target.value as any,
            }))
          }
          className={`
            w-full
            rounded-lg
            px-3
            py-2.5
            border
            focus:outline-none
            focus:ring-2
            focus:ring-indigo-200
            ${
              errors.naturaleza
                ? "border-red-500"
                : "border-gray-300"
            }
          `}
        >
          <option value="SVC_DIG">
            Servicio Digital
          </option>

          <option value="PROD_FIS">
            Producto Físico
          </option>
        </select>

        {errors.naturaleza && (
          <p className="mt-1 text-xs text-red-600">
            {errors.naturaleza}
          </p>
        )}

      </div>

      {/* Unidad */}

      <div>

        <label className="block text-sm font-medium text-gray-700 mb-1">
          Unidad de medida
          <span className="text-red-500 ml-1">*</span>
        </label>

        <select
          value={form.unidad_medida}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              unidad_medida: e.target.value as any,
            }))
          }
          className={`
            w-full
            rounded-lg
            px-3
            py-2.5
            border
            focus:outline-none
            focus:ring-2
            focus:ring-indigo-200
            ${
              errors.unidad_medida
                ? "border-red-500"
                : "border-gray-300"
            }
          `}
        >
          <option value="UND">Unidad</option>
          <option value="MIL">Mil</option>
          <option value="M2">Metro cuadrado</option>
          <option value="ML">Metro lineal</option>
          <option value="HR">Hora</option>
          <option value="MES">Mes</option>
          <option value="GLOB">Global</option>
        </select>

        {errors.unidad_medida && (
          <p className="mt-1 text-xs text-red-600">
            {errors.unidad_medida}
          </p>
        )}

      </div>

      {/* IVA */}

      <div>

        <label className="block text-sm font-medium text-gray-700 mb-1">
          Tarifa IVA
          <span className="text-red-500 ml-1">*</span>
        </label>

        <select
          value={form.tarifa_iva}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              tarifa_iva: e.target.value as any,
            }))
          }
          className={`
            w-full
            rounded-lg
            px-3
            py-2.5
            border
            focus:outline-none
            focus:ring-2
            focus:ring-indigo-200
            ${
              errors.tarifa_iva
                ? "border-red-500"
                : "border-gray-300"
            }
          `}
        >
          <option value="15.00">15%</option>
          <option value="5.00">5%</option>
          <option value="0.00">0%</option>
        </select>

        {errors.tarifa_iva && (
          <p className="mt-1 text-xs text-red-600">
            {errors.tarifa_iva}
          </p>
        )}

      </div>

      {/* Precio */}

      <div>

        <label className="block text-sm font-medium text-gray-700 mb-1">
          Precio base
          <span className="text-red-500 ml-1">*</span>
        </label>

        <input
          type="number"
          step="0.01"
          value={form.precio_base_unitario}
          onChange={(e) =>
            setForm((prev) => ({
              ...prev,
              precio_base_unitario:
                e.target.value,
            }))
          }
          className={`
            w-full
            rounded-lg
            px-3
            py-2.5
            border
            focus:outline-none
            focus:ring-2
            focus:ring-indigo-200
            ${
              errors.precio_base_unitario
                ? "border-red-500"
                : "border-gray-300"
            }
          `}
        />

        {errors.precio_base_unitario && (
          <p className="mt-1 text-xs text-red-600">
            {errors.precio_base_unitario}
          </p>
        )}

      </div>

      {/* Checkbox */}

      <div className="md:col-span-2 pt-2">

        <label className="flex items-center gap-2 cursor-pointer">

          <input
            type="checkbox"
            checked={
              form.requiere_dimensiones
            }
            onChange={(e) =>
              setForm((prev) => ({
                ...prev,
                requiere_dimensiones:
                  e.target.checked,
              }))
            }
          />

          <span className="text-sm text-gray-700">
            Requiere dimensiones
          </span>

        </label>

      </div>

    </div>
  );
}