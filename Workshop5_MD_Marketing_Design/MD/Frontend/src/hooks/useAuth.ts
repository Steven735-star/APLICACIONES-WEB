// ==============================================================================
// MD Marketing & Diseño — src/hooks/useAuth.ts
// ==============================================================================

import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import api from "@/api/axios";
import { ENDPOINTS } from "@/api/endpoints";
import type { LoginForm, TokenPair } from "@/types/api.types";

export function useAuth() {
  const navigate  = useNavigate();
  const { setTokens, logout: storeLogout, isAuthenticated, user } = useAuthStore();

  const login = async (credentials: LoginForm): Promise<void> => {
    const { data } = await api.post<TokenPair>(
      ENDPOINTS.AUTH.TOKEN,
      credentials
    );
    setTokens(data.access, data.refresh);
    navigate("/dashboard");
  };

  const logout = async (): Promise<void> => {
    try {
      const refresh = useAuthStore.getState().refreshToken;
      if (refresh) {
        await api.post(ENDPOINTS.AUTH.BLACKLIST, { refresh });
      }
    } catch {
      // Si falla el blacklist, igual hacemos logout local
    } finally {
      storeLogout();
      navigate("/login");
    }
  };

  return { login, logout, isAuthenticated, user };
}
