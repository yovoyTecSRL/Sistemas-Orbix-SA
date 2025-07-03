# 🧠 Orbix Systems

**Inteligencia real para negocios reales.**

Orbix Systems es una plataforma integral que combina inteligencia artificial, automatización y seguridad para empresas modernas.

## 🚀 Servicios Principales

### ✅ Sistema de Validaciones
- **CCSS**: Validación de estado laboral y cuotas obrero-patronales
- **SUGEF**: Consultas de centrales de riesgo y reportes crediticios
- **Registro Nacional**: Validación de documentos y registros oficiales
- **IA Integration**: Análisis automático con Odoo ERP

### 🧮 Calculadora Financiera Inteligente
- Calculadora de préstamos con amortización
- Análisis de capacidad de pago
- Simulador de inversiones
- Scoring crediticio automático

### 🛡️ Sentinel - Monitoreo y Seguridad
- Monitoreo de red en tiempo real
- Detección de amenazas con IA
- Análisis de logs centralizados
- Dashboard de seguridad

### 🚀 ERP Integration
- Conexión con Odoo ERP
- Sincronización de datos
- Workflows automatizados

## 🔌 Puertos y Servicios

| Servicio | Puerto | Estado | URL |
|----------|--------|--------|-----|
| **Web Principal** | 3000 | ✅ Activo | http://localhost:3000 |
| **Sentinel Main** | 3001 | 🔄 Dev | http://localhost:3001 |
| **Sentinel Dashboard** | 3002 | 🔄 Dev | http://localhost:3002 |
| **Sentinel API** | 3003 | 🔄 Dev | http://localhost:3003 |
| **Validaciones** | 3005 | 🔄 Planned | http://localhost:3005 |
| **Calculadora** | 3009 | 🔄 Planned | http://localhost:3009 |

Ver [PUERTOS.md](./PUERTOS.md) para documentación completa de puertos.

---

## 🗂 Estructura del Proyecto

/public
├── index.html # Página principal con menú Orbix
├── styles.css # Estilos visuales oscuros
└── orbixlogo.png # Logo oficial
index.js # Servidor Express (modo Node)
app.py # Servidor Flask (modo Python)
levantarserver.sh # Script de ejecución Flask
Dockerfile # Contenedor universal
.github/workflows/
└── deploy.yml # CI/CD automático vía GitHub Actions

yaml
Copiar
Editar

---

## 🌐 Enlaces rápidos (desde la página)

- 🧠 Inicio → https://sistemasorbix.com
- ✅ Validaciones → `/validaciones`
- 🧮 Calculadora → `/calculadora`
- 🛡️ Sentinel → `/sentinel`
- 🚀 ERP → [https://erp.sistemasorbix.com](https://erp.sistemasorbix.com)

---

## ▶️ Usar en modo Express

```bash
npm install
npm start
Abre: http://localhost:3000

🧠 Usar en modo Flask
bash
Copiar
Editar
chmod +x levantarserver.sh
./levantarserver.sh
Abre: http://127.0.0.1:5000

🐳 Desplegar con Docker
bash
Copiar
Editar
docker build -t orbix-web .
docker run -p 80:80 orbix-web
☁️ Deploy automático (Copilot + GitHub Actions)
Usa .github/workflows/deploy.yml para despliegue automático cada vez que pushes a main.

✉️ Contacto
Orbix Systems S.A.
Web: https://sistemasorbix.com
Correo: info@sistemasorbix.com

php-template
Copiar
Editar

---

## ✅ `index.html` con menú completo y enlaces clave

```html
<header>
  <h1>🧠 Orbix Systems</h1>
  <p>Inteligencia real para negocios reales.</p>
  <nav>
    <a href="/">Inicio</a>
    <a href="#validaciones">✅ Validaciones</a>
    <a href="#calculadora">🧮 Calculadora</a>
    <a href="#sentinel">🛡️ Sentinel</a>
    <a href="https://erp.sistemasorbix.com" target="_blank">🚀 ERP</a>
  </nav>
</header>
(Ya está incluido en tu versión actual con estilos adaptados)

✅ Dockerfile
Dockerfile
Copiar
Editar
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install flask gunicorn

RUN apt-get update && apt-get install -y curl gnupg \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && npm install

EXPOSE 80

CMD ["bash", "levantarserver.sh"]
✅ .github/workflows/deploy.yml
yaml
Copiar
Editar
name: 🚀 Deploy Orbix Landing

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout
        uses: actions/checkout@v3

      - name: 🐍 Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: 🧠 Install Flask
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install flask gunicorn

      - name: 🧰 Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: 📦 Install Node Dependencies
        run: npm install

      - name: 🐳 Build Docker Image
        run: docker build -t orbix-web .

      - name: 🚀 Run Docker
        run: docker run -d -p 80:80 orbix-web

# 🛡️ Sistemas Orbix S.A. - Plataforma Web Integrada

## 📋 Descripción

Plataforma web completa de Orbix Systems que integra múltiples servicios y herramientas empresariales incluyendo validaciones, calculadoras avanzadas y un centro de monitoreo de seguridad (Sentinel) con dashboards en tiempo real.

## 🏗️ Arquitectura del Sistema

### Frontend Web (Puerto 3000)
- **Servidor**: Node.js + Express
- **Páginas**: 
  - Inicio (`/`)
  - Validaciones (`/validaciones`) - Con integración a FastAPI
  - Calculadora (`/calculadora`)
  - **Sentinel (`/sentinel`) - Dashboard de Monitoreo en Tiempo Real**
- **Proxy**: `/api/orbix/*` → FastAPI (puerto 8000)

### Sentinel - Centro de Monitoreo Avanzado
La página de Sentinel ahora incluye un dashboard completo de monitoreo en tiempo real con:

#### 📊 Gráficos en Tiempo Real (Chart.js)
- **Tráfico de Red**: Monitoreo de entrada y salida de datos
- **Eventos de Seguridad**: Críticos, advertencias e información
- **Rendimiento del Sistema**: CPU, RAM, Disco (gráfico de dona)
- **Detección de Amenazas**: Amenazas detectadas vs bloqueadas
- **Uso de Ancho de Banda**: Monitoreo continuo
- **Actividad Geográfica**: Conexiones por país

#### 🚨 Características Avanzadas
- **Feed de Actividad en Tiempo Real**: Eventos de seguridad actualizados cada 2 segundos
- **Controles Interactivos**: Pausar/reanudar, filtros, limpieza de datos
- **Métricas Dinámicas**: Estadísticas que se actualizan automáticamente
- **Indicadores de Amenaza**: Niveles bajo, medio, alto con animaciones
- **Verificación de APIs**: Estado en tiempo real de servicios conectados
- **Design Responsivo**: Optimizado para dispositivos móviles

#### 🎨 Diseño Profesional
- **Tema Moderno**: Gradientes azules con efectos de glassmorphism
- **Cards Interactivas**: Contenedores con sombras y efectos de profundidad
- **Animaciones**: Transiciones suaves y efectos visuales
- **Dashboard Tipo Grafana**: Layout profesional estilo centro de operaciones

## 🔌 Puertos Documentados

| Puerto | Servicio | Estado | Descripción |
|--------|----------|---------|-------------|
| 3000 | Node.js/Express | ✅ Activo | Servidor web principal |
| 8000 | FastAPI | ⏳ Pendiente | API backend de validaciones |
| 8070 | Odoo ERP | ⏳ Pendiente | Sistema ERP empresarial |
| 5432 | PostgreSQL | ⏳ Pendiente | Base de datos principal |
