// ==============================================================================
// MD Marketing & Diseño — src/components/Layout.tsx
// Componente de layout principal con sidebar y header responsive
// ==============================================================================

import { Outlet, NavLink } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { LayoutDashboard, Kanban, Users, Package, Receipt, LogOut, Menu, X } from "lucide-react";
import { useState } from "react";

const NAV_ITEMS = [
  { to: "/dashboard",     icon: LayoutDashboard, label: "Panel de Control" },
  { to: "/kanban",        icon: Kanban,           label: "Producción" },
  { to: "/catalogo",      icon: Package,          label: "Catálogo" },
  { to: "/clientes",      icon: Users,            label: "Clientes" },
  { to: "/transacciones", icon: Receipt,          label: "Finanzas" },
] as const;

export default function Layout() {
  const { logout } = useAuth();
  const [open, setOpen] = useState(false);

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {open && (
        <div
          className="fixed inset-0 bg-black/40 z-20 lg:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      <aside className={`
        fixed lg:static inset-y-0 left-0 z-30
        w-60 bg-[#111111] text-white flex flex-col
        transform transition-transform duration-200
        ${open ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
      `}>
        <div className="flex items-center justify-between px-5 py-4 border-t border-gray-700">
          <div>
            <p className="font-extrabold text-xl">
              <span className="text-[#C8C7C7]">M</span>
              <span className="text-[#E83C16]">D</span>
            </p>
            <p className="text-xs text-gray-400 tracking-wide">
              Marketing & Diseño
            </p>
          </div>
          <button className="lg:hidden" onClick={() => setOpen(false)}>
            <X size={18} className="text-gray-400" />
          </button>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setOpen(false)}
              className={({ isActive }: { isActive: boolean }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? "bg-[#be2e09] text-white"
                    : "text-gray-300 hover:bg-[#1A1A1A]"
                }`
              }
            >
              <Icon size={17} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="px-3 py-4 border-t border-gray-700">
          <button
            onClick={logout}
            className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg
                       text-sm text-gray-300 hover:bg-[#1A1A1A] transition-colors"
          >
            <LogOut size={17} />
            Cerrar sesión
          </button>
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header className="lg:hidden flex items-center px-4 py-3 bg-white border-b border-gray-200">
          <button onClick={() => setOpen(true)} className="mr-3">
            <Menu size={20} className="text-gray-600" />
          </button>
          <p className="font-semibold text-sm text-gray-800">MD Marketing & Diseño</p>
        </header>

        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}