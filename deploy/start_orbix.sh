#!/bin/bash

# 🧠 Orbix Systems - Script de arranque completo
# Instala dependencias, configura el entorno y levanta todos los servicios

echo "🚀 Iniciando Orbix Sentinel + Validaciones + Calculadora"
echo "========================================================="

# Colores para el output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para mostrar mensajes con colores
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/main.py" ]; then
    log_error "No se encuentra backend/main.py. Ejecute desde la raíz del proyecto."
    exit 1
fi

# Paso 1: Verificar dependencias del sistema
log_step "Verificando dependencias del sistema..."

if ! command -v python3 &> /dev/null; then
    log_error "Python3 no está instalado"
    exit 1
fi
log_success "Python3 encontrado: $(python3 --version)"

if ! command -v pip3 &> /dev/null; then
    log_error "pip3 no está instalado"
    exit 1
fi
log_success "pip3 encontrado"

if ! command -v node &> /dev/null; then
    log_error "Node.js no está instalado"
    exit 1
fi
log_success "Node.js encontrado: $(node --version)"

if ! command -v npm &> /dev/null; then
    log_error "npm no está instalado"
    exit 1
fi
log_success "npm encontrado: $(npm --version)"

# Paso 2: Instalar dependencias Python
log_step "Instalando dependencias Python..."
cd backend

if [ ! -f "../requirements.txt" ]; then
    log_warning "requirements.txt no encontrado, creando uno básico..."
    cat > ../requirements.txt << EOF
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
requests==2.31.0
jinja2==3.1.2
aiofiles==23.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
EOF
fi

pip3 install -r ../requirements.txt

if [ $? -eq 0 ]; then
    log_success "Dependencias Python instaladas correctamente"
else
    log_error "Error instalando dependencias Python"
    exit 1
fi

cd ..

# Paso 3: Instalar dependencias Node.js si es necesario
if [ ! -d "node_modules" ]; then
    log_step "Instalando dependencias Node.js..."
    npm install
    if [ $? -eq 0 ]; then
        log_success "Dependencias Node.js instaladas"
    else
        log_warning "Algunas dependencias de Node.js fallaron, continuando..."
    fi
fi

# Paso 4: Verificar puertos disponibles
log_step "Verificando puertos disponibles..."

check_port() {
    local port=$1
    local service=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warning "Puerto $port ($service) ya está en uso"
        return 1
    else
        log_success "Puerto $port ($service) disponible"
        return 0
    fi
}

check_port 8000 "FastAPI"
FASTAPI_PORT_OK=$?

check_port 3000 "Express"
EXPRESS_PORT_OK=$?

# Paso 5: Crear directorio de logs si no existe
mkdir -p logs
log_info "Directorio de logs creado/verificado"

# Paso 6: Función para limpiar procesos al salir
cleanup() {
    echo
    log_step "Deteniendo servidores..."
    
    if [ ! -z "$FASTAPI_PID" ]; then
        kill $FASTAPI_PID 2>/dev/null
        log_info "FastAPI detenido (PID: $FASTAPI_PID)"
    fi
    
    if [ ! -z "$EXPRESS_PID" ]; then
        kill $EXPRESS_PID 2>/dev/null
        log_info "Express detenido (PID: $EXPRESS_PID)"
    fi
    
    # Matar cualquier proceso que esté usando los puertos
    lsof -ti:8000 | xargs -r kill -9 2>/dev/null
    lsof -ti:3000 | xargs -r kill -9 2>/dev/null
    
    log_success "Limpieza completada"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Paso 7: Levantar FastAPI
log_step "Iniciando FastAPI en puerto 8000..."
cd backend

# Verificar que el archivo main.py existe
if [ ! -f "main.py" ]; then
    log_error "No se encuentra backend/main.py"
    exit 1
fi

# Levantar FastAPI en background con logs
uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ../logs/fastapi.log 2>&1 &
FASTAPI_PID=$!

log_info "FastAPI iniciado con PID: $FASTAPI_PID"

# Esperar a que FastAPI esté listo
log_info "Esperando a que FastAPI esté listo..."
for i in {1..15}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        log_success "FastAPI está respondiendo"
        break
    fi
    
    if [ $i -eq 15 ]; then
        log_error "FastAPI no responde después de 15 segundos"
        cleanup
        exit 1
    fi
    
    sleep 1
    echo -n "."
done

cd ..

# Paso 8: Levantar Express si existe server.js
if [ -f "server.js" ]; then
    log_step "Iniciando Express en puerto 3000..."
    
    node server.js > logs/express.log 2>&1 &
    EXPRESS_PID=$!
    
    log_info "Express iniciado con PID: $EXPRESS_PID"
    
    # Esperar a que Express esté listo
    log_info "Esperando a que Express esté listo..."
    for i in {1..10}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            log_success "Express está respondiendo"
            break
        fi
        
        if [ $i -eq 10 ]; then
            log_warning "Express no responde, pero continuamos..."
            break
        fi
        
        sleep 1
        echo -n "."
    done
else
    log_warning "server.js no encontrado, saltando Express"
fi

# Paso 9: Mostrar información del deployment
echo
echo "🎉 ¡Orbix Systems desplegado exitosamente!"
echo "=========================================="
echo

log_success "🧠 FastAPI Backend:"
echo -e "   ${CYAN}• URL:${NC} http://localhost:8000"
echo -e "   ${CYAN}• Documentación:${NC} http://localhost:8000/docs"
echo -e "   ${CYAN}• Health Check:${NC} http://localhost:8000/health"
echo -e "   ${CYAN}• Logs:${NC} tail -f logs/fastapi.log"

if [ ! -z "$EXPRESS_PID" ]; then
    echo
    log_success "🌐 Express Frontend:"
    echo -e "   ${CYAN}• URL:${NC} http://localhost:3000"
    echo -e "   ${CYAN}• Logs:${NC} tail -f logs/express.log"
fi

echo
log_success "🧮 Módulos Disponibles:"
echo -e "   ${CYAN}• Validaciones:${NC} http://localhost:8000/validaciones"
echo -e "   ${CYAN}• Sentinel:${NC} http://localhost:3000/sentinel"
echo -e "   ${CYAN}• Calculadora:${NC} http://localhost:3000/calculadora"
echo -e "   ${CYAN}• Panel Principal:${NC} http://localhost:8000/"

echo
log_success "📊 API Endpoints:"
echo -e "   ${CYAN}• Estado del Sistema:${NC} http://localhost:8000/api/status"
echo -e "   ${CYAN}• Métricas Sentinel:${NC} http://localhost:8000/api/sentinel/metrics"
echo -e "   ${CYAN}• Eventos Sentinel:${NC} http://localhost:8000/api/sentinel/events"
echo -e "   ${CYAN}• Validaciones API:${NC} http://localhost:8000/api/validaciones/tipos"

echo
echo -e "${YELLOW}📝 Comandos útiles:${NC}"
echo "   • Ver logs FastAPI: tail -f logs/fastapi.log"
echo "   • Ver logs Express: tail -f logs/express.log"
echo "   • Probar API: curl http://localhost:8000/health"
echo "   • Detener todo: Ctrl+C"

echo
log_info "⏹️  Presiona Ctrl+C para detener todos los servidores"
echo

# Paso 10: Mostrar logs en tiempo real (opcional)
if [ "$1" = "--show-logs" ]; then
    log_info "Mostrando logs en tiempo real..."
    tail -f logs/fastapi.log logs/express.log
else
    # Mantener el script corriendo
    wait
fi
