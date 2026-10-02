// ==============================================================================
// MD Marketing & Diseño — src/types/api.types.ts
// Interfaces TypeScript que espejean los serializers de Django REST Framework
// ==============================================================================

// ── Paginación DRF ────────────────────────────────────────────────────────────
export interface PaginatedResponse<T> {
  count:    number;
  next:     string | null;
  previous: string | null;
  results:  T[];
}

// ── Auth / JWT ────────────────────────────────────────────────────────────────
export interface TokenPair {
  access:  string;
  refresh: string;
}

export interface TokenRefresh {
  access: string;
}

// ── CRM: Clientes ─────────────────────────────────────────────────────────────
export type TipoIdentificacion = "CED" | "RUC" | "PAS";

export interface Cliente {
  id:                          number;
  tipo_identificacion:         TipoIdentificacion;
  numero_identificacion:       string;
  razon_social:                string;
  nombre_comercial:            string;
  correo_electronico:          string;
  telefono_principal:          string;
  telefono_secundario:         string;
  direccion:                   string;
  ciudad:                      string;
  aplica_retencion_fuente:     boolean;
  porcentaje_retencion_fuente: string;
  activo:                      boolean;
  creado_en:                   string;
  actualizado:                 string;
}

export interface ClienteList {
  id:                    number;
  tipo_identificacion:   TipoIdentificacion;
  numero_identificacion: string;
  razon_social:          string;
  nombre_comercial:      string;
  telefono_principal:    string;
  ciudad:                string;
  activo:                boolean;
}

// ── CRM: Catálogo ─────────────────────────────────────────────────────────────
export type NaturalezaItem = "SVC_DIG" | "PROD_FIS";
export type TarifaIVA     = "15.00" | "0.00" | "5.00";
export type UnidadMedida  = "UND" | "MIL" | "M2" | "ML" | "HR" | "MES" | "GLOB";

export interface CatalogoItem {
  id:                    number;
  codigo:                string;
  nombre:                string;
  descripcion:           string;
  naturaleza:            NaturalezaItem;
  naturaleza_display:    string;
  unidad_medida:         UnidadMedida;
  unidad_medida_display: string;
  tarifa_iva:            TarifaIVA;
  tarifa_iva_display:    string;
  precio_base_unitario:  string;
  requiere_dimensiones:  boolean;
  activo:                boolean;
}

// ── Producción: Órdenes FSM ───────────────────────────────────────────────────
export type EstadoOrden =
  | "COTIZADO"
  | "PENDIENTE_PAGO"
  | "EN_DISENIO"
  | "EN_PRODUCCION"
  | "LISTO_ENTREGA"
  | "ENTREGADO"
  | "CANCELADO";

export type PrioridadOrden = "NORMAL" | "URGENTE" | "CRITICA";

export interface TransicionDisponible {
  accion: string;
  label:  string;
  color:  "blue" | "green" | "orange" | "teal" | "red";
}

export interface OrdenItem {
  id:                      number;
  orden:                   number;
  catalogo_item:           number;
  catalogo_item_nombre:    string;
  catalogo_item_codigo:    string;
  descripcion_personalizada: string;
  cantidad:                string;
  ancho_m:                 string | null;
  alto_m:                  string | null;
  precio_unitario_neto:    string;
  descuento_porcentaje:    string;
  tarifa_iva:              TarifaIVA;
  monto_neto:              string;
  monto_iva:               string;
  monto_total:             string;
  orden_linea:             number;
  notas:                   string;
}

export interface HistorialEstado {
  id:                 number;
  estado_anterior:    EstadoOrden | "";
  estado_nuevo:       EstadoOrden;
  cambiado_por:       number | null;
  cambiado_por_nombre: string;
  timestamp:          string;
  notas:              string;
  duracion_minutos:   number | null;
}

export interface OrdenList {
  id:              number;
  numero_orden:    string;
  cliente:         number;
  cliente_nombre:  string;
  cliente_ruc:     string;
  estado:          EstadoOrden;
  estado_display:  string;
  prioridad:       PrioridadOrden;
  total_orden:     string;
  fecha_compromiso: string | null;
  creado_en:       string;
  dias_en_estado:  number;
}

export interface Orden extends OrdenList {
  descripcion_general:      string;
  asignado_a:               number | null;
  subtotal_neto:            string;
  total_iva:                string;
  items:                    OrdenItem[];
  historial_estados:        HistorialEstado[];
  transiciones_disponibles: TransicionDisponible[];
  actualizado:              string;
}

// ── Producción: Kanban ────────────────────────────────────────────────────────
export interface KanbanColumna {
  estado:  EstadoOrden;
  label:   string;
  total:   number;
  ordenes: OrdenList[];
}

export interface KanbanData {
  columnas:      KanbanColumna[];
  total_activas: number;
}

// ── Finanzas ──────────────────────────────────────────────────────────────────
export type TipoMovimiento = "ING" | "EGR";
export type MetodoPago = "EFEC" | "TRANSF" | "T_DEB" | "T_CRED" | "CHQ" | "OTRO";

export interface CategoriaFinanciera {
  id:          number;
  codigo:      string;
  nombre:      string;
  tipo:        TipoMovimiento;
  tipo_display: string;
  descripcion: string;
  activa:      boolean;
}

export interface Transaccion {
  id:                   number;
  referencia:           string;
  tipo:                 TipoMovimiento;
  tipo_display:         string;
  categoria:            number;
  categoria_nombre:     string;
  descripcion:          string;
  orden:                number | null;
  orden_numero:         string | null;
  cliente:              number | null;
  cliente_nombre:       string | null;
  monto_neto:           string;
  base_iva:             string;
  tarifa_iva_aplicada:  string;
  monto_iva:            string;
  retencion_fuente:     string;
  retencion_iva:        string;
  monto_flujo_caja:     string;
  metodo_pago:          MetodoPago;
  metodo_pago_display:  string;
  fecha_emision:        string;
  fecha_registro:       string;
  anulada:              boolean;
}

// ── Dashboard ─────────────────────────────────────────────────────────────────
export interface DashboardFinanzas {
  ingresos_brutos:   string;
  egresos_totales:   string;
  utilidad_neta:     string;
  margen_porcentaje: number;
  saldo_iva:         string;
  a_pagar_sri:       boolean;
}

export interface DashboardData {
  mes_actual:  { inicio: string; fin: string };
  finanzas:    DashboardFinanzas;
  produccion:  Record<EstadoOrden, number>;
}

// ── Inventario ────────────────────────────────────────────────────────────────
export interface MateriaPrima {
  id:              number;
  codigo:          string;
  nombre:          string;
  unidad_medida:   UnidadMedida;
  unidad_medida_display: string;
  stock_actual:    string;
  stock_minimo:    string;
  costo_unitario:  string;
  proveedor:       string;
  activo:          boolean;
  alerta_stock:    boolean;
}

// ── Formularios (payloads de POST/PATCH) ──────────────────────────────────────
export interface LoginForm {
  username: string;
  password: string;
}

export interface ClienteForm {
  tipo_identificacion: TipoIdentificacion;
  numero_identificacion: string;
  razon_social: string;
  nombre_comercial?: string;
  correo_electronico?: string;
  telefono_principal?: string;
  telefono_secundario?: string;
  direccion?: string;
  ciudad?: string;
  aplica_retencion_fuente?: boolean;
  porcentaje_retencion_fuente?: string;
}

export interface CatalogoForm {
  codigo: string;
  nombre: string;
  descripcion?: string;
  naturaleza: NaturalezaItem;
  unidad_medida: UnidadMedida;
  tarifa_iva: TarifaIVA;
  precio_base_unitario: string;
  requiere_dimensiones: boolean;
  activo?: boolean;
}

export interface CatalogoForm {
  codigo: string;
  nombre: string;
  descripcion?: string;
  naturaleza: NaturalezaItem;
  unidad_medida: UnidadMedida;
  tarifa_iva: TarifaIVA;
  precio_base_unitario: string;
  requiere_dimensiones: boolean;
  activo?: boolean;
}

export interface TransicionForm {
  accion: string;
  notas?: string;
}