# 🔌 Puertos y Servicios - Orbix Systems

## 📋 Puertos Principales

### 🌐 Servidor Web Principal
- **Puerto**: `3000`
- **Servicio**: Servidor web principal de Orbix Systems
- **URL**: http://localhost:3000
- **Estado**: ✅ Activo
- **Descripción**: Aplicación web principal con todas las funcionalidades

### 🛡️ Sentinel - Sistema de Monitoreo
- **Puerto Principal**: `3001`
- **Puerto Dashboard**: `3002` 
- **Puerto API**: `3003`
- **Puerto WebSocket**: `3004`
- **Estado**: 🔄 Planificado
- **Descripción**: Sistema de monitoreo y seguridad en tiempo real

### ✅ Servicio de Validaciones
- **Puerto**: `3005`
- **API CCSS**: `3006`
- **API SUGEF**: `3007`
- **API Registro Nacional**: `3008`
- **Estado**: 🔄 Planificado
- **Descripción**: APIs para validaciones gubernamentales y crediticias

### 🧮 Calculadora Financiera
- **Puerto**: `3009`
- **API Cálculos**: `3010`
- **Estado**: 🔄 Planificado
- **Descripción**: Servicios de cálculos financieros avanzados

### 🗄️ Base de Datos
- **PostgreSQL**: `5432`
- **Redis Cache**: `6379`
- **MongoDB**: `27017`
- **Estado**: 🔄 Planificado

### 🔗 Servicios Externos
- **ERP Odoo**: `8069` (https://erp.sistemasorbix.com)
- **Estado**: ✅ Externo

## 🚀 Comandos de Inicio

```bash
# Servidor principal
npm start                    # Puerto 3000

# Servicios individuales (cuando estén implementados)
npm run start:sentinel       # Puerto 3001
npm run start:validaciones   # Puerto 3005
npm run start:calculadora    # Puerto 3009
```

## 🔧 Configuración de Puertos

Los puertos pueden configurarse mediante variables de entorno:

```bash
# Servidor principal
PORT=3000

# Sentinel
SENTINEL_PORT=3001
SENTINEL_DASHBOARD_PORT=3002
SENTINEL_API_PORT=3003
SENTINEL_WS_PORT=3004

# Validaciones
VALIDACIONES_PORT=3005
CCSS_API_PORT=3006
SUGEF_API_PORT=3007
REGISTRO_API_PORT=3008

# Calculadora
CALCULADORA_PORT=3009
CALC_API_PORT=3010
```

## 🛡️ Seguridad de Puertos

- Todos los puertos están configurados para bind en `0.0.0.0`
- CORS habilitado para desarrollo
- Logs de acceso activados
- Rate limiting planificado para producción

## 📊 Monitoreo de Puertos

El sistema Sentinel monitoreará automáticamente:
- Estado de puertos (activo/inactivo)
- Latencia de respuesta
- Número de conexiones
- Alertas por caídas de servicio

## 🔄 Estado Actual

| Servicio | Puerto | Estado | Notas |
|----------|--------|--------|-------|
| Web Principal | 3000 | ✅ Activo | Funcionando |
| Sentinel | 3001-3004 | 🔄 Desarrollo | En desarrollo |
| Validaciones | 3005-3008 | 🔄 Planificado | Próximamente |
| Calculadora | 3009-3010 | 🔄 Planificado | Próximamente |

---
*Última actualización: 3 de julio, 2025*
