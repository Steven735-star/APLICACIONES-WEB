// ==============================================================================
// MD Marketing & Diseño — src/store/authStore.ts
// Estado global de autenticación con Zustand
// ==============================================================================

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  id:       number;
  username: string;
  email:    string;
}

interface AuthState {
  accessToken:  string | null;
  refreshToken: string | null;
  user:         User | null;
  isAuthenticated: boolean;

  // Acciones
  setTokens:  (access: string, refresh: string) => void;
  setUser:    (user: User) => void;
  logout:     () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken:     null,
      refreshToken:    null,
      user:            null,
      isAuthenticated: false,

      setTokens: (access, refresh) =>
        set({ accessToken: access, refreshToken: refresh, isAuthenticated: true }),

      setUser: (user) => set({ user }),

      logout: () =>
        set({ accessToken: null, refreshToken: null, user: null, isAuthenticated: false }),
    }),
    {
      name: "md-auth",   // Clave en localStorage
      // Solo persistir tokens, no el objeto user completo
      partialize: (state) => ({
        accessToken:  state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);