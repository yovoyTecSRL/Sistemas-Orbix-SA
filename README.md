✅ README.md COMPLETO
markdown
Copiar
Editar
# 🧠 Orbix Systems - Startpage Oficial

Landing profesional y dinámica para **Sistemas Orbix S.A.**, con enlaces clave hacia servicios Orbix como validaciones, Sentinel, calculadora y el ERP empresarial.

---

## 🚀 Funcionalidades

- Interfaz responsive con diseño futurista estilo dark
- Enlaces rápidos a módulos críticos de Orbix
- Soporte dual para despliegue con Node.js o Flask
- Compatible con Docker y GitHub Actions (Copilot Ready)

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
