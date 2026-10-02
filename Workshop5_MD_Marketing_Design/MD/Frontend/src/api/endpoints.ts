// ==============================================================================
// MD Marketing & Diseño — src/api/endpoints.ts
// Constantes de todos los endpoints de la API
// ==============================================================================

export const ENDPOINTS = {
  // Auth
  AUTH: {
    TOKEN:     "/auth/token/",
    REFRESH:   "/auth/token/refresh/",
    BLACKLIST: "/auth/token/blacklist/",
  },

  // CRM
  CRM: {
    CLIENTES:       "/crm/clientes/",
    CLIENTE:        (id: number) => `/crm/clientes/${id}/`,
    BUSCAR_RUC:     "/crm/clientes/buscar_ruc/",
    CATALOGO:       "/crm/catalogo/",
    CATALOGO_ITEM:  (id: number) => `/crm/catalogo/${id}/`,
  },

  // Producción
  PRODUCCION: {
    ORDENES:          "/produccion/ordenes/",
    ORDEN:            (id: number) => `/produccion/ordenes/${id}/`,
    TRANSICION:       (id: number) => `/produccion/ordenes/${id}/transicion/`,
    HISTORIAL:        (id: number) => `/produccion/ordenes/${id}/historial/`,
    KANBAN:           "/produccion/kanban/",
    ITEMS:            "/produccion/items/",
    ITEM:             (id: number) => `/produccion/items/${id}/`,
  },

  // Finanzas
  FINANZAS: {
    TRANSACCIONES:    "/finanzas/transacciones/",
    TRANSACCION:      (id: number) => `/finanzas/transacciones/${id}/`,
    CATEGORIAS:       "/finanzas/categorias/",
    DASHBOARD:        "/finanzas/dashboard/",
    REPORTE_UTILIDAD: "/finanzas/reportes/utilidad/",
    REPORTE_IVA:      "/finanzas/reportes/iva/",
    REPORTE_TENDENCIA:"/finanzas/reportes/tendencia/",
    REPORTE_EGRESOS:  "/finanzas/reportes/egresos/",
  },

  // Inventario
  INVENTARIO: {
    MATERIAS_PRIMAS:  "/inventario/materias-primas/",
    MATERIA_PRIMA:    (id: number) => `/inventario/materias-primas/${id}/`,
    ALERTAS:          "/inventario/materias-primas/alertas/",
    CONSUMOS:         "/inventario/consumos/",
  },
} as const;