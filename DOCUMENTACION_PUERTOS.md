# 🌐 Documentación de Puertos - Orbix Systems

## 📋 Arquitectura de Servicios

### 🖥️ Servidor Principal (Node.js + Express)
- **Puerto**: `3000`
- **Función**: Frontend web y proxy para APIs
- **URL**: http://localhost:3000
- **Estado**: ✅ Activo
- **Archivos servidos**: 
  - `/` → `public/index.html`
  - `/validaciones` → `public/validaciones.html`
  - `/calculadora` → `public/calculadora.html`
  - `/sentinel` → `public/sentinel.html`

### 🐍 FastAPI Server (Python)
- **Puerto**: `8000`
- **Función**: API de validaciones, cotizaciones y backend
- **URL**: http://localhost:8000
- **Estado**: ⏳ Pendiente (requiere clone del repo)
- **Repositorio**: https://github.com/yovoyTecSRL/orbix.git
- **Endpoints principales**:
  - `/health` - Estado del servicio
  - `/cotizar` - Cotizaciones inteligentes
  - `/api/payment-stats` - Estadísticas de pagos
  - `/api/metrics` - Métricas del sistema
  - `/docs` - Documentación Swagger

### 🏢 Odoo ERP
- **Puerto**: `8070`
- **Función**: Sistema empresarial completo
- **URL**: http://localhost:8070
- **Estado**: ⏳ Pendiente (requiere instalación)
- **Master Password**: `orbix_master_2025`
- **Base de datos**: PostgreSQL

### 🗃️ PostgreSQL Database
- **Puerto**: `5432`
- **Función**: Base de datos principal
- **Host**: localhost
- **Estado**: ⏳ Pendiente (requiere instalación)
- **Usuario**: postgres
- **Database**: orbix_db

## 🔗 Integración entre Servicios

### Proxy Middleware (Node.js → FastAPI)
```javascript
// Rutas proxy configuradas:
app.use('/api/orbix', proxy({
  target: 'http://localhost:8000',
  changeOrigin: true,
  pathRewrite: { '^/api/orbix': '' }
}));
```

### 📡 Endpoints de Comunicación
- **Node.js** (3000) ↔ **FastAPI** (8000): `/api/orbix/*`
- **FastAPI** (8000) ↔ **PostgreSQL** (5432): Conexión directa
- **Odoo** (8070) ↔ **PostgreSQL** (5432): Conexión directa

## 🚀 Comandos para Levantar Servicios

### 1. Servidor Node.js (Ya corriendo)
```bash
cd /workspaces/Sistemas-Orbix-SA
npm start
# o
node server.js
```

### 2. FastAPI Server (Pendiente)
```bash
# Primero clonar el repositorio:
git clone https://github.com/yovoyTecSRL/orbix.git
cd orbix
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Odoo ERP (Pendiente)
```bash
# Instalación de Odoo
docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:15
docker run -p 8070:8069 --name odoo --link db:db -t odoo
```

### 4. PostgreSQL (Pendiente)
```bash
# Con Docker
docker run --name postgres-orbix -e POSTGRES_PASSWORD=orbix123 -p 5432:5432 -d postgres:15
```

## 🔧 Variables de Entorno

```bash
# Node.js Server
PORT=3000
FASTAPI_URL=http://localhost:8000

# FastAPI
ENVIRONMENT=development
DATABASE_URL=postgresql://postgres:orbix123@localhost:5432/orbix_db

# Odoo
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=orbix_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=orbix123
```

## 🛡️ Seguridad y Acceso

### CORS Configuration
- **Node.js**: Habilitado para todos los orígenes
- **FastAPI**: Configurado para permitir conexiones locales
- **Odoo**: Configuración por defecto

### Autenticación
- **Node.js**: Sin autenticación (desarrollo)
- **FastAPI**: Tokens JWT (si está configurado)
- **Odoo**: Usuario/contraseña + Master Password

## 📊 Monitoreo

### Health Checks
- **Node.js**: `GET http://localhost:3000/health`
- **FastAPI**: `GET http://localhost:8000/health`
- **PostgreSQL**: Conexión directa en puerto 5432

### Logs
- **Node.js**: Console output
- **FastAPI**: uvicorn logs
- **Odoo**: Docker logs
- **PostgreSQL**: Docker logs

## 🔄 Estado Actual

### ✅ Servicios Activos
- [x] Node.js Server (Puerto 3000)
- [x] Proxy Middleware configurado
- [x] Frontend web funcionando

### ⏳ Servicios Pendientes
- [ ] FastAPI Server (Puerto 8000)
- [ ] Odoo ERP (Puerto 8070)
- [ ] PostgreSQL (Puerto 5432)

## 🎯 Próximos Pasos

1. **Clonar repositorio FastAPI**: `git clone https://github.com/yovoyTecSRL/orbix.git`
2. **Instalar y configurar PostgreSQL**
3. **Levantar FastAPI server**
4. **Instalar y configurar Odoo**
5. **Probar integración completa**

---
*Actualizado: 3 de julio, 2025*
*Orbix Systems S.A.*
