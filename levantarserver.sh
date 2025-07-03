#!/bin/bash

# Script para levantar el servidor de Orbix Systems
echo "🚀 Iniciando Orbix Systems Server..."

# Crear un servidor HTTP simple con Python
echo "📁 Sirviendo archivos desde el directorio actual..."
echo "🌐 Servidor disponible en puerto 80"
echo "✅ Orbix Systems está listo!"

# Usar Python para servir archivos estáticos
cd /app
python3 -m http.server 80 --bind 0.0.0.0
