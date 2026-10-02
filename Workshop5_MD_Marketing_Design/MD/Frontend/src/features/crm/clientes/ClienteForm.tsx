import { useEffect, useState } from "react";

import type {
  Cliente,
  ClienteForm as ClienteFormData,
} from "@/types/api.types";

interface ClienteFormProps {
  initialData?: Cliente | null;
  loading?: boolean;
  error?: string | null;
  onSubmit: (data: ClienteFormData) => void;
}

export default function ClienteForm({
  initialData,
  loading = false,
  error = null,
  onSubmit,
}: ClienteFormProps) {
  const [form, setForm] = useState<ClienteFormData>({
    tipo_identificacion: "CED",
    numero_identificacion: "",
    razon_social: "",
    nombre_comercial: "",
    correo_electronico: "",
    telefono_principal: "",
    telefono_secundario: "",
    direccion: "",
    ciudad: "",
    aplica_retencion_fuente: false,
    porcentaje_retencion_fuente: "0.00",
  });

  useEffect(() => {
    if (!initialData) return;

    setForm({
      tipo_identificacion: initialData.tipo_identificacion,
      numero_identificacion: initialData.numero_identificacion,
      razon_social: initialData.razon_social,
      nombre_comercial: initialData.nombre_comercial,
      correo_electronico: initialData.correo_electronico,
      telefono_principal: initialData.telefono_principal,
      telefono_secundario: initialData.telefono_secundario,
      direccion: initialData.direccion,
      ciudad: initialData.ciudad,
      aplica_retencion_fuente:
        initialData.aplica_retencion_fuente,
      porcentaje_retencion_fuente:
        initialData.porcentaje_retencion_fuente,
    });
  }, [initialData]);

  const updateField = (
    field: keyof ClienteFormData,
    value: string | boolean
  ) => {
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">
            Tipo de Identificación
            <span className="text-red-500 ml-1">*</span>
          </label>

          <select
            value={form.tipo_identificacion}
            onChange={(e) =>
              updateField(
                "tipo_identificacion",
                e.target.value
              )
            }
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="CED">Cédula</option>
            <option value="RUC">RUC</option>
            <option value="PAS">Pasaporte</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Número de Identificación
            <span className="text-red-500 ml-1">*</span>
          </label>

          <input
            required
            value={form.numero_identificacion}
            onChange={(e) =>
              updateField(
                "numero_identificacion",
                e.target.value
              )
            }
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">
          Nombre Completo / Razón Social
          <span className="text-red-500 ml-1">*</span>
        </label>

        <input
          required
          value={form.razon_social}
          onChange={(e) =>
            updateField(
              "razon_social",
              e.target.value
            )
          }
          className="w-full border border-gray-300 rounded-lg px-3 py-2"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">
          Nombre Comercial
        </label>

        <input
          value={form.nombre_comercial}
          onChange={(e) =>
            updateField(
              "nombre_comercial",
              e.target.value
            )
          }
          className="w-full border border-gray-300 rounded-lg px-3 py-2"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          type="email"
          placeholder="Correo electrónico"
          value={form.correo_electronico}
          onChange={(e) =>
            updateField(
              "correo_electronico",
              e.target.value
            )
          }
          className="border border-gray-300 rounded-lg px-3 py-2"
        />

        <input
          placeholder="Teléfono principal"
          value={form.telefono_principal}
          onChange={(e) =>
            updateField(
              "telefono_principal",
              e.target.value
            )
          }
          className="border border-gray-300 rounded-lg px-3 py-2"
        />
      </div>

      <input
        placeholder="Teléfono secundario"
        value={form.telefono_secundario}
        onChange={(e) =>
          updateField(
            "telefono_secundario",
            e.target.value
          )
        }
        className="w-full border border-gray-300 rounded-lg px-3 py-2"
      />

      <textarea
        placeholder="Dirección"
        value={form.direccion}
        onChange={(e) =>
          updateField(
            "direccion",
            e.target.value
          )
        }
        className="w-full border border-gray-300 rounded-lg px-3 py-2"
        rows={3}
      />

      <input
        placeholder="Ciudad"
        value={form.ciudad}
        onChange={(e) =>
          updateField(
            "ciudad",
            e.target.value
          )
        }
        className="w-full border border-gray-300 rounded-lg px-3 py-2"
      />

      <div className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={
            form.aplica_retencion_fuente ?? false
          }
          onChange={(e) =>
            updateField(
              "aplica_retencion_fuente",
              e.target.checked
            )
          }
        />

        <span className="text-sm">
          Aplica retención en la fuente
        </span>
      </div>

      {form.aplica_retencion_fuente && (
        <input
          placeholder="Porcentaje de retención"
          value={
            form.porcentaje_retencion_fuente ?? ""
          }
          onChange={(e) =>
            updateField(
              "porcentaje_retencion_fuente",
              e.target.value
            )
          }
          className="w-full border border-gray-300 rounded-lg px-3 py-2"
        />
      )}

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading
            ? "Guardando..."
            : "Guardar Cliente"}
        </button>
      </div>
    </form>
  );
}