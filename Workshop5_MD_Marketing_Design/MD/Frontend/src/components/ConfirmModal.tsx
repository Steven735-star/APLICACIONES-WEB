// ==============================================================================
// MD Marketing & Diseño — src/components/ConfirmModal.tsx
// Modal reutilizable para confirmaciones.
// ==============================================================================

import { useEffect } from "react";
interface ConfirmModalProps {

  open: boolean;
  title: string;
  message: string;
  loading?: boolean;

  onConfirm: () => void;
  onCancel: () => void;
}

export default function ConfirmModal({
  open,
  title,
  message,
  loading = false,
  onConfirm,
  onCancel,
}: ConfirmModalProps) {

  useEffect(() => {
    if (!open) return;

    const handleKeyDown = (
      event: KeyboardEvent
    ) => {
      if (event.key === "Escape") {
        onCancel();
      }
    };

    window.addEventListener(
      "keydown",
      handleKeyDown
    );

    return () => {
      window.removeEventListener(
        "keydown",
        handleKeyDown
      );
    };
  }, [open, onCancel]);

  if (!open) return null;

  return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={onCancel} >
        <div onClick={(e) => e.stopPropagation()} className="bg-white rounded-xl shadow-xl w-full max-w-md p-6">

        <h2 className="text-lg font-semibold text-gray-900">
          {title}
        </h2>

        <p className="mt-2 text-sm text-gray-600">
          {message}
        </p>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onCancel}
            disabled={loading}
            className="
              px-4 py-2
              rounded-lg
              border border-gray-200
              hover:bg-gray-50
            "
          >
            Cancelar
          </button>

          <button
            onClick={onConfirm}
            disabled={loading}
            className="
              px-4 py-2
              rounded-lg
              bg-red-600
              text-white
              hover:bg-red-700
            "
          >
            {loading
              ? "Desactivando..."
              : "Desactivar"}
          </button>
        </div>
      </div>
    </div>
  );
}