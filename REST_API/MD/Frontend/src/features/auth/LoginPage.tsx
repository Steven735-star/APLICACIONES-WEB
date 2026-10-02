// ==============================================================================
// MD Marketing & Diseño — src/features/auth/LoginPage.tsx
// ==============================================================================

import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";

export default function LoginPage() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error,    setError]    = useState("");
  const [loading,  setLoading]  = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login({ username, password });
    } catch {
      setError("Usuario o contraseña incorrectos.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">

        {/* Logo / Título */}
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-white">Marketing & Diseño</h1>
          <p className="text-gray-400 text-sm mt-1">Sistema ERP/CRM</p>
        </div>

        {/* Card */}
        <form
          onSubmit={handleSubmit}
          className="bg-gray-800 rounded-2xl p-6 space-y-4 shadow-xl"
        >
          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Usuario
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoFocus
              className="w-full bg-gray-700 text-white rounded-lg px-3 py-2.5
                         text-sm border border-gray-600 focus:outline-none
                         focus:border-indigo-500 transition-colors"
              placeholder="Tu usuario"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Contraseña
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full bg-gray-700 text-white rounded-lg px-3 py-2.5
                         text-sm border border-gray-600 focus:outline-none
                         focus:border-indigo-500 transition-colors"
              placeholder="••••••••"
            />
          </div>

          {error && (
            <p className="text-red-400 text-xs bg-red-900/30 rounded-lg px-3 py-2">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50
                       text-white font-medium rounded-lg py-2.5 text-sm
                       transition-colors mt-2"
          >
            {loading ? "Ingresando..." : "Iniciar sesión"}
          </button>
        </form>
      </div>
    </div>
  );
}