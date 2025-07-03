✅ 1. README.md — profesional y claro para GitHub
markdown
Copiar
Editar
# 🧠 Orbix Systems - Landing Oficial

Bienvenido al repositorio principal de **Orbix Systems S.A.**, donde se despliega la página de inicio del ecosistema Orbix con soporte para Express (Node.js) y Flask (Python).

---

## 🚀 Funcionalidades

- Interfaz profesional con diseño oscuro y futurista
- Modo dual: `Node.js + Express` y `Python + Flask`
- Responsive, rápido y fácil de desplegar en cualquier VPS o Codespace
- Integración opcional con Odoo, OpenAI y Sentinel

---

## 📁 Estructura del Proyecto

/public/
├── index.html
├── styles.css
└── orbixlogo.png
index.js # Express server
package.json
app.py # Flask server
levantarserver.sh # Script para levantar con Flask
Dockerfile # Contenedor multiuso
.github/workflows/deploy.yml

yaml
Copiar
Editar

---

## 🧪 Modo Express (Node.js)

```bash
npm install
npm start
Accede en: http://localhost:3000

🧠 Modo Flask (Python)
bash
Copiar
Editar
chmod +x levantarserver.sh
./levantarserver.sh
Accede en: http://127.0.0.1:5000

🐳 Deploy con Docker
bash
Copiar
Editar
docker build -t orbix-web .
docker run -p 80:80 orbix-web
☁️ Deploy automático con GitHub Actions (Copilot Ready)
Revisa .github/workflows/deploy.yml para deploy automático.

Ideal para Codespaces, VPS o integraciones continuas.

📫 Contacto
Orbix Systems S.A.
Email: info@sistemasorbix.com
Web: https://sistemasorbix.com

yaml
Copiar
Editar

---

## ✅ 2. `Dockerfile` — soporta tanto Node como Flask (multi-modo)

```Dockerfile
# Dockerfile para Orbix Systems

FROM python:3.10-slim

WORKDIR /app

COPY . .

# Instalar dependencias de Python (para Flask)
RUN pip install flask gunicorn

# Instalar Node.js + npm para modo Express
RUN apt-get update && apt-get install -y curl gnupg \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && npm install

EXPOSE 80

CMD ["bash", "levantarserver.sh"]
✅ 3. .github/workflows/deploy.yml — para GitHub Copilot + Actions
yaml
Copiar
Editar
name: 🚀 Deploy Orbix Landing

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Clonar repositorio
        uses: actions/checkout@v3

      - name: 🐍 Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: 🧪 Instalar dependencias Flask
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install flask gunicorn

      - name: 🧰 Instalar Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: 📦 Instalar dependencias Node.js
        run: npm install

      - name: 🐳 Construir imagen Docker
        run: docker build -t orbix-web .

      - name: 🚀 Ejecutar contenedor
        run: docker run -d -p 80:80 orbix-web
