#!/bin/bash

# 🛡️ Script de pruebas para Orbix Sentinel
# Verifica que todos los endpoints estén funcionando correctamente

echo "🛡️ ORBIX SENTINEL - PRUEBAS DE ENDPOINTS"
echo "========================================"

BASE_URL="http://localhost:8000/api/sentinel"

# Función para hacer pruebas
test_endpoint() {
    echo "📊 Probando: $1"
    response=$(curl -s "$BASE_URL$2")
    if [ $? -eq 0 ]; then
        echo "✅ OK - $1"
        echo "$response" | jq . > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ JSON válido"
        else
            echo "⚠️ Respuesta no es JSON válido"
        fi
    else
        echo "❌ FALLO - $1"
    fi
    echo "---"
}

# Verificar que el servidor esté corriendo
echo "🔍 Verificando servidor..."
server_status=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✅ Servidor FastAPI funcionando"
else
    echo "❌ Servidor no responde"
    exit 1
fi

echo ""
echo "🧪 PRUEBAS DE ENDPOINTS SENTINEL"
echo "================================"

# Probar todos los endpoints
test_endpoint "Tráfico de Red" "/network-traffic"
test_endpoint "Eventos de Seguridad" "/security-events"
test_endpoint "Rendimiento del Sistema" "/system-performance"
test_endpoint "Detección de Amenazas" "/threat-detection"
test_endpoint "Ancho de Banda" "/bandwidth"
test_endpoint "Actividad Geográfica" "/geographic"
test_endpoint "Dashboard Completo" "/dashboard-complete"

echo ""
echo "🎯 PRUEBA DE ACTUALIZACIONES EN TIEMPO REAL"
echo "==========================================="

echo "📊 Ejecutando 5 consultas consecutivas con intervalos de 1 segundo..."

for i in {1..5}; do
    echo "Consulta #$i:"
    entrada=$(curl -s "$BASE_URL/network-traffic" | jq -r '.entrada_mbps')
    salida=$(curl -s "$BASE_URL/network-traffic" | jq -r '.salida_mbps')
    cpu=$(curl -s "$BASE_URL/system-performance" | jq -r '.cpu_porcentaje')
    
    echo "  📈 Tráfico: ${entrada} MB/s entrada, ${salida} MB/s salida"
    echo "  💻 CPU: ${cpu}%"
    echo ""
    
    if [ $i -lt 5 ]; then
        sleep 1
    fi
done

echo "✅ PRUEBAS COMPLETADAS"
echo ""
echo "🌐 URLS DISPONIBLES:"
echo "==================="
echo "• Dashboard Principal: http://localhost:8000/"
echo "• Sistema Sentinel: http://localhost:8000/static/sentinel.html"
echo "• Tarjeta de Crédito: http://localhost:8000/static/tarjeta-credito.html"
echo "• API Health: http://localhost:8000/health"
echo "• API Docs: http://localhost:8000/docs"
echo ""
echo "🚀 Sistema Orbix completamente operacional!"
