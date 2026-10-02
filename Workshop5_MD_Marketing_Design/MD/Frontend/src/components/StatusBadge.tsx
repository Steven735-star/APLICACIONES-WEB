import type { EstadoOrden } from "@/types/api.types";

const STYLES: Record<EstadoOrden, string> = {
COTIZADO:       "bg-gray-100 text-gray-700",
PENDIENTE_PAGO: "bg-amber-100 text-amber-700",
EN_DISENIO:     "bg-blue-100 text-blue-700",
EN_PRODUCCION:  "bg-purple-100 text-purple-700",
LISTO_ENTREGA:  "bg-teal-100 text-teal-700",
ENTREGADO:      "bg-green-100 text-green-700",
CANCELADO:      "bg-red-100 text-red-700",
};

interface Props {
estado: EstadoOrden;
label?: string;
}

export default function StatusBadge({
estado,
label,
}: Props) {
return (
<span
className={`text-xs px-2 py-0.5 rounded-full font-medium ${STYLES[estado]}`}
>
{label ?? estado} </span>
);
}
