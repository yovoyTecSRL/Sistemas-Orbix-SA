#!/bin/bash

# 🧠 Orbix Systems - Script de instalación y despliegue
# Instala dependencias Python y levanta FastAPI + Node.js

echo "🧠 Orbix Systems - Instalación y Despliegue"
echo "============================================"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    exit 1
fi

# Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencias Python instaladas correctamente"
else
    echo "❌ Error instalando dependencias Python"
    exit 1
fi

# Verificar instalación de Node.js
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias Node.js..."
    npm install
fi

echo ""
echo "🚀 Levantando servidores..."
echo ""

# Crear ventanas de terminal para cada servidor
echo "📡 Iniciando FastAPI en puerto 8000..."
echo "🌐 Iniciando Express en puerto 3000..."

# Función para manejar señales de interrupción
cleanup() {
    echo ""
    echo "🛑 Deteniendo servidores..."
    kill $FASTAPI_PID $EXPRESS_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Levantar FastAPI en background
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
FASTAPI_PID=$!

# Esperar un poco para que FastAPI se inicie
sleep 3

# Levantar Express en background
node server.js &
EXPRESS_PID=$!

echo ""
echo "🎉 Servidores iniciados exitosamente!"
echo ""
echo "📡 FastAPI: http://localhost:8000"
echo "   - Documentación: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/health"
echo ""
echo "🌐 Express: http://localhost:3000"
echo "   - Dashboard: http://localhost:3000/sentinel"
echo "   - Validaciones: http://localhost:3000/validaciones"
echo "   - Calculadora: http://localhost:3000/calculadora"
echo ""
echo "⏹️  Presiona Ctrl+C para detener los servidores"
echo ""

# Mantener el script corriendo
wait
