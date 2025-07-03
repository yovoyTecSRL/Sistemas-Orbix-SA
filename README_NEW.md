# 🧠 Orbix Systems — Panel Inteligente + Validaciones + Sentinel

## 🚀 Descripción

**Orbix Systems** es una plataforma integrada de inteligencia empresarial que combina:

- **Panel Principal**: Dashboard interactivo con estado del sistema
- **Sistema de Validaciones**: IA para validación automática de datos (cédulas, teléfonos, emails, cuentas bancarias)
- **Orbix Sentinel**: Centro de comando de seguridad y monitoreo 24/7
- **Calculadora Financiera**: Herramientas avanzadas para cálculos de préstamos e inversiones
- **Integración ERP**: Conexión directa con Odoo para gestión empresarial

## 📁 Estructura del Proyecto

```
orbix_project/
├── backend/
│   ├── main.py               # FastAPI con todos los endpoints
│   └── orbix_config.json     # Configuración del sistema
├── frontend/
│   └── index.html            # Panel principal Orbix
├── public/
│   ├── sentinel_new.html     # Dashboard de seguridad
│   ├── calculadora.html      # Calculadora financiera
│   └── validaciones.html     # Interfaz de validaciones
├── deploy/
│   ├── start_orbix.sh        # Script de arranque completo
│   └── docker-compose.yml    # Despliegue con contenedores
├── validaciones/             # Será clonado automáticamente
│   └── (repo validacion-credito)
├── logs/                     # Logs del sistema
└── README.md
```

## 🏃‍♂️ Inicio Rápido

### Opción 1: Script Automático (Recomendado)

```bash
# Clonar el repositorio
git clone [tu-repo]
cd Sistemas-Orbix-SA

# Ejecutar el script de deploy
./deploy/start_orbix.sh
```

### Opción 2: Manual

```bash
# Instalar dependencias Python
pip3 install -r requirements.txt

# Levantar FastAPI
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Levantar Express (si tienes server.js)
cd ..
node server.js &
```

### Opción 3: Docker (Producción)

```bash
# Levantar toda la infraestructura
cd deploy
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🌐 URLs de Acceso

Una vez iniciado, accede a:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| 🧠 **Panel Principal** | http://localhost:8000 | Dashboard principal |
| 📊 **API Docs** | http://localhost:8000/docs | Documentación interactiva |
| 🧮 **Validaciones** | http://localhost:8000/validaciones | Sistema de validaciones |
| 🛡️ **Sentinel** | http://localhost:3000/sentinel | Centro de seguridad |
| 💰 **Calculadora** | http://localhost:3000/calculadora | Herramientas financieras |
| 🚀 **ERP Odoo** | https://erp.sistemasorbix.com | Sistema empresarial |

## 🛡️ API Endpoints Principales

### 🔍 Sistema
- `GET /health` - Health check del sistema
- `GET /api/status` - Estado completo del sistema

### 🧮 Validaciones
- `GET /api/validaciones/tipos` - Tipos de validación disponibles
- `POST /api/validaciones/validar` - Validar datos (cédula, teléfono, email, cuenta bancaria)

### 🛡️ Sentinel (Seguridad)
- `GET /api/sentinel/status` - Estado del sistema de seguridad
- `GET /api/sentinel/events` - Eventos de seguridad recientes
- `GET /api/sentinel/metrics` - Métricas en tiempo real

### 💰 Calculadora
- `GET /api/calculadora/tipos` - Tipos de cálculo disponibles
- `POST /api/calculadora/calcular` - Calcular préstamos y amortizaciones

## 🎯 Comandos Rápidos

```bash
# Iniciar todo el sistema
./deploy/start_orbix.sh

# Solo mostrar logs
./deploy/start_orbix.sh --show-logs

# Probar APIs
curl http://localhost:8000/health
curl http://localhost:8000/api/sentinel/status

# Validar una cédula
curl -X POST "http://localhost:8000/api/validaciones/validar" \
     -H "Content-Type: application/json" \
     -d '{"tipo": "cedula", "valor": "123456789"}'

# Calcular préstamo
curl -X POST "http://localhost:8000/api/calculadora/calcular" \
     -H "Content-Type: application/json" \
     -d '{"monto": 1000000, "tasa": 12, "plazo": 24, "tipo": "prestamo_personal"}'
```

## 📞 Contacto

- **Email**: info@sistemasorbix.com
- **Teléfono**: +506 2200-0000
- **Website**: https://sistemasorbix.com
- **ERP**: https://erp.sistemasorbix.com

---

> **🧠 Orbix Systems** - *Inteligencia real para negocios reales*
