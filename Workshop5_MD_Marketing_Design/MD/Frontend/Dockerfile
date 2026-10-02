# ==============================================================================
# MD Marketing & Diseño — Frontend/Dockerfile
# Imagen de desarrollo para React + Vite con hot-reload
# ==============================================================================

FROM node:20-alpine

WORKDIR /app

# Instalar dependencias del sistema para Vite y algunos loaders nativos
RUN apk add --no-cache libc6-compat

# Copiar manifests primero (caché de Docker: solo reinstala si cambian)
COPY package.json package-lock.json* ./

# Instalar dependencias
RUN npm ci --prefer-offline

# Copiar resto del código
COPY . .

EXPOSE 5173

# Vite con host 0.0.0.0 para ser accesible desde fuera del contenedor
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
