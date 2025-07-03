# 🧠 ORBIX FASTAPI MASTER
# Esta app sirve una página principal con estado del sistema (index.html)
# y puede lanzar microservicios como el sistema de validaciones automáticamente.
# Si el contenedor "orbix-validaciones" no está activo, clona el repo y lo despliega.
# También se puede integrar mediante iframe en el frontend o como redirección.

# Instrucciones para Copilot:
# - Crear función /validaciones en FastAPI
# - Clonar el repo si no existe: https://github.com/yovoyTecSRL/validacion-credito
# - Ejecutar docker-compose up -d
# - Redirigir a localhost:8090 o mostrar en iframe
# - Asegurar que esté en /opt/orbix_validaciones

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import requests
import asyncio
import random
from typing import List, Dict, Any
# Nuevas importaciones para el sistema de tarjeta de crédito
from pydantic import BaseModel, validator
import uuid
import re
import time

app = FastAPI(
    title="🧠 Orbix Systems", 
    version="2.0.0", 
    description="Inteligencia real para negocios reales - Sistema Integrado de Seguridad y Validaciones"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos del frontend
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Servir la página principal del panel Orbix"""
    try:
        with open("../frontend/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🧠 Orbix Systems</title>
            <style>
                body { font-family: Arial; padding: 20px; background: #0a0a0a; color: #00ff00; }
                .btn { padding: 10px 20px; margin: 10px; background: #1a1a1a; color: #00ff00; border: 1px solid #00ff00; border-radius: 5px; text-decoration: none; display: inline-block; }
                .btn:hover { background: #00ff00; color: #000; }
                .feature-card { background: #1a1a1a; border: 1px solid #00ff00; border-radius: 10px; padding: 20px; margin: 10px; }
            </style>
        </head>
        <body>
            <h1>🧠 Orbix Systems</h1>
            <p>Inteligencia real para negocios reales.</p>
            <div class="feature-card">
                <h2>💳 Solicitud de Tarjeta de Crédito</h2>
                <p>Sistema inteligente de evaluación crediticia con consultas automáticas a entidades oficiales.</p>
                <a href='tarjeta-credito.html' class='btn'>🚀 Solicitar Tarjeta</a>
            </div>
            <div>
                <a href='/validaciones' class='btn'>🧮 Lanzar Validaciones</a>
                <a href='/sentinel' class='btn'>🛡️ Sentinel</a>
                <a href='/calculadora' class='btn'>💰 Calculadora</a>
            </div>
        </body>
        </html>
        """)

@app.get("/tarjeta-credito", response_class=HTMLResponse)
async def tarjeta_credito_page():
    """Servir la página de solicitud de tarjeta de crédito"""
    try:
        with open("../frontend/tarjeta-credito.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Página de tarjeta de crédito no encontrada")

@app.get("/sentinel", response_class=HTMLResponse)
async def sentinel_page():
    """Servir la página de monitoreo Sentinel"""
    try:
        with open("../frontend/sentinel.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Página de Sentinel no encontrada")

@app.get("/calculadora", response_class=HTMLResponse)
async def calculadora_page():
    """Servir la página de calculadora"""
    try:
        with open("../public/calculadora.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Página de calculadora no encontrada")

@app.get("/validaciones")
async def lanzar_validaciones():
    """
    Verifica si el contenedor orbix-validaciones está corriendo.
    Si no, clona el repo desde GitHub y lo ejecuta con docker-compose,
    luego redirige al usuario al puerto 8090.
    """
    try:
        path = "/opt/orbix_validaciones"
        puerto = 8090
        contenedor = "orbix-validaciones"
        repo_url = "https://github.com/yovoyTecSRL/validacion-credito"

        print(f"🔍 Verificando contenedor {contenedor}...")
        
        # Verificar si Docker está disponible
        result = None
        try:
            result = subprocess.run(["docker", "ps"], capture_output=True, text=True, timeout=10)
            docker_disponible = True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            docker_disponible = False
            print("⚠️ Docker no disponible, intentando método alternativo...")

        if docker_disponible and result and contenedor in result.stdout:
            print(f"✅ Contenedor {contenedor} ya está corriendo")
            return RedirectResponse(url=f"http://localhost:{puerto}")

        # Si el contenedor no está corriendo, clonarlo y desplegarlo
        print(f"📥 Clonando repositorio desde {repo_url}...")
        
        if not os.path.exists(path):
            # Crear directorio si no existe
            os.makedirs(path, exist_ok=True)
            
            # Clonar repositorio
            clone_result = subprocess.run([
                "git", "clone", repo_url, path
            ], capture_output=True, text=True, timeout=30)
            
            if clone_result.returncode != 0:
                raise HTTPException(status_code=500, detail=f"Error clonando repositorio: {clone_result.stderr}")
            
            print(f"✅ Repositorio clonado en {path}")
        else:
            print(f"📁 Directorio {path} ya existe")

        # Intentar levantar con docker-compose si está disponible
        if docker_disponible:
            print("🚀 Levantando contenedor con docker-compose...")
            
            compose_file = os.path.join(path, "docker-compose.yml")
            if os.path.exists(compose_file):
                compose_result = subprocess.run([
                    "docker-compose", "-f", compose_file, "up", "-d"
                ], capture_output=True, text=True, timeout=60)
                
                if compose_result.returncode == 0:
                    print("✅ Contenedor levantado exitosamente")
                    await asyncio.sleep(5)
                    return RedirectResponse(url=f"http://localhost:{puerto}")
                else:
                    print(f"⚠️ Error con docker-compose: {compose_result.stderr}")

        # Si Docker no funciona, intentar levantar directamente con Python
        print("🐍 Intentando levantar con Python...")
        
        main_files = ["main.py", "app.py", "server.py"]
        main_file = None
        
        for file in main_files:
            full_path = os.path.join(path, file)
            if os.path.exists(full_path):
                main_file = full_path
                break
        
        if main_file:
            requirements_file = os.path.join(path, "requirements.txt")
            if os.path.exists(requirements_file):
                subprocess.run(["pip3", "install", "-r", requirements_file], 
                             capture_output=True, timeout=60)
            
            subprocess.Popen([
                "python3", "-m", "uvicorn", 
                f"{os.path.basename(main_file).replace('.py', '')}:app",
                "--host", "0.0.0.0", "--port", str(puerto)
            ], cwd=path)
            
            print(f"✅ Aplicación iniciada en puerto {puerto}")
            await asyncio.sleep(3)
            return RedirectResponse(url=f"http://localhost:{puerto}")
        
        return {
            "status": "cloned",
            "message": f"Repositorio clonado en {path}",
            "next_steps": [
                "Verificar docker-compose.yml",
                "Instalar dependencias manualmente",
                f"Navegar a http://localhost:{puerto} cuando esté listo"
            ],
            "path": path,
            "repo": repo_url
        }
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Timeout ejecutando comando")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deployando validaciones: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check del sistema principal"""
    return {
        "status": "healthy",
        "service": "🧠 Orbix Systems",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "validaciones": await check_service_status(8090),
            "sentinel": "integrated",
            "calculadora": "integrated"
        }
    }

async def check_service_status(port: int) -> str:
    """Verificar estado de un servicio por puerto"""
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=2)
        return "active" if response.status_code == 200 else "inactive"
    except:
        return "inactive"

@app.get("/api/status")
async def get_system_status():
    """Estado completo del sistema Orbix"""
    return {
        "system": "🧠 Orbix Systems",
        "status": "operational",
        "uptime": "99.9%",
        "services": {
            "main": "active",
            "validaciones": await check_service_status(8090),
            "sentinel": "integrated",
            "calculadora": "integrated"
        },
        "timestamp": datetime.now().isoformat()
    }

# === SENTINEL ENDPOINTS ===

@app.get("/api/sentinel/status")
async def sentinel_status():
    """Estado detallado del módulo Sentinel con datos dinámicos"""
    # Simular variaciones más realistas basadas en la hora del día
    hour = datetime.now().hour
    base_multiplier = 1.0
    
    # Mayor actividad durante horas laborales
    if 8 <= hour <= 18:
        base_multiplier = 1.5
    elif 19 <= hour <= 23:
        base_multiplier = 1.2
    
    return {
        "status": "operational",
        "threats_blocked": int(random.randint(100, 200) * base_multiplier),
        "events_today": int(random.randint(30, 80) * base_multiplier),
        "active_alerts": random.randint(0, 8),
        "active_connections": int(random.randint(50, 150) * base_multiplier),
        "uptime": "99.9%",
        "last_update": datetime.now().isoformat(),
        "security_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "system_health": {
            "cpu": round(random.uniform(15, 85), 1),
            "ram": round(random.uniform(25, 75), 1),
            "disk": round(random.uniform(40, 85), 1)
        },
        "network_status": {
            "ping": round(random.uniform(1, 15), 1),
            "packet_loss": round(random.uniform(0, 2), 2),
            "bandwidth_usage": round(random.uniform(10, 90), 1)
        }
    }

@app.get("/api/sentinel/events")
async def sentinel_events():
    """Eventos recientes de Sentinel con datos realistas"""
    event_types = ["security", "network", "system", "threat"]
    levels = ["critical", "warning", "info", "success"]
    
    messages = {
        "security": [
            "Intento de acceso no autorizado bloqueado",
            "Login fallido detectado",
            "Certificado SSL renovado automáticamente",
            "Política de firewall actualizada",
            "Autenticación de dos factores activada"
        ],
        "network": [
            "Nueva conexión desde IP externa",
            "Tráfico anómalo detectado",
            "Ancho de banda excedido",
            "Conexión VPN establecida",
            "Puerto escaneado desde IP sospechosa"
        ],
        "system": [
            "Backup automático completado",
            "Actualización de sistema aplicada",
            "Servicio reiniciado automáticamente",
            "Limpieza de logs ejecutada",
            "Monitoreo de recursos activado"
        ],
        "threat": [
            "Malware bloqueado en endpoint",
            "Virus detectado y eliminado",
            "Ataque DDoS mitigado",
            "Ransomware bloqueado",
            "Phishing detectado y bloqueado"
        ]
    }
    
    events = []
    for i in range(random.randint(5, 15)):
        event_type = random.choice(event_types)
        level = random.choice(levels)
        
        events.append({
            "id": i + 1,
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
            "type": event_type,
            "level": level,
            "message": random.choice(messages[event_type]),
            "source": f"192.168.1.{random.randint(1, 255)}" if event_type == "network" else f"WS-{random.randint(1, 100)}"
        })
    
    return {"events": events}

@app.get("/api/sentinel/metrics")
async def sentinel_metrics():
    """Métricas en tiempo real para los gráficos - Datos más realistas"""
    now = datetime.now()
    hour = now.hour
    
    # Simular patrones de tráfico más realistas
    if 8 <= hour <= 18:  # Horas laborales
        traffic_multiplier = 1.8
        threat_multiplier = 1.5
    elif 19 <= hour <= 23:  # Noche activa
        traffic_multiplier = 1.3
        threat_multiplier = 1.2
    else:  # Madrugada
        traffic_multiplier = 0.6
        threat_multiplier = 0.8
    
    # Datos de tráfico de red
    in_traffic = round(random.uniform(5, 40) * traffic_multiplier, 1)
    out_traffic = round(random.uniform(3, 25) * traffic_multiplier, 1)
    
    return {
        "network_traffic": {
            "timestamp": now.isoformat(),
            "in_mbps": in_traffic,
            "out_mbps": out_traffic,
            "total_gb_today": round((in_traffic + out_traffic) * 0.1, 2),
            "peak_mbps": round(max(in_traffic, out_traffic) * 1.5, 1),
            "avg_mbps": round((in_traffic + out_traffic) / 2, 1)
        },
        "security_events": {
            "critical": int(random.randint(0, 5) * threat_multiplier),
            "warning": int(random.randint(0, 10) * threat_multiplier),
            "info": int(random.randint(5, 25) * threat_multiplier)
        },
        "threat_detection": {
            "detected": int(random.randint(0, 8) * threat_multiplier),
            "blocked": int(random.randint(0, 6) * threat_multiplier),
            "resolved": int(random.randint(0, 5) * threat_multiplier),
            "investigating": random.randint(0, 3)
        },
        "system_performance": {
            "cpu_usage": round(random.uniform(15, 85), 1),
            "ram_usage": round(random.uniform(25, 75), 1),
            "disk_usage": round(random.uniform(40, 85), 1),
            "network_latency": round(random.uniform(1, 15), 1)
        },
        "bandwidth": {
            "current_usage": round(random.uniform(10, 90), 1),
            "peak_usage": round(random.uniform(70, 100), 1),
            "average_usage": round(random.uniform(30, 60), 1),
            "available_mbps": 100
        },
        "geographic": {
            "countries": {
                "Costa Rica": int(random.randint(100, 300) * traffic_multiplier),
                "Estados Unidos": int(random.randint(50, 200) * traffic_multiplier),
                "México": int(random.randint(30, 120) * traffic_multiplier),
                "Colombia": int(random.randint(20, 100) * traffic_multiplier),
                "España": int(random.randint(15, 80) * traffic_multiplier),
                "Brasil": int(random.randint(10, 60) * traffic_multiplier)
            },
            "suspicious_ips": random.randint(0, 15),
            "unique_countries": random.randint(8, 25)
        },
        "alerts": {
            "active": random.randint(0, 8),
            "resolved_today": int(random.randint(5, 20) * threat_multiplier),
            "pending": random.randint(0, 5)
        }
    }

# === VALIDACIONES ENDPOINTS ===

@app.get("/api/validaciones/tipos")
async def get_validation_types():
    """Tipos de validaciones disponibles"""
    return {
        "tipos": [
            {
                "id": "cedula",
                "nombre": "Validación de Cédula",
                "descripcion": "Verifica formato y validez de cédulas costarricenses",
                "activo": True
            },
            {
                "id": "telefono", 
                "nombre": "Validación de Teléfono",
                "descripcion": "Verifica formato de números telefónicos",
                "activo": True
            },
            {
                "id": "email",
                "nombre": "Validación de Email", 
                "descripcion": "Verifica formato y existencia de correos electrónicos",
                "activo": True
            },
            {
                "id": "cuenta_bancaria",
                "nombre": "Validación de Cuenta Bancaria",
                "descripcion": "Verifica formato de cuentas bancarias IBAN",
                "activo": True
            }
        ]
    }

@app.post("/api/validaciones/validar")
async def validate_data(data: dict):
    """Endpoint principal para validaciones"""
    tipo = data.get("tipo")
    valor = data.get("valor")
    
    if not tipo or not valor:
        raise HTTPException(status_code=400, detail="Tipo y valor son requeridos")
    
    # Simular validación según el tipo
    validaciones = {
        "cedula": validate_cedula,
        "telefono": validate_telefono,
        "email": validate_email,
        "cuenta_bancaria": validate_cuenta_bancaria
    }
    
    if tipo not in validaciones:
        raise HTTPException(status_code=400, detail="Tipo de validación no soportado")
    
    resultado = validaciones[tipo](valor)
    
    return {
        "tipo": tipo,
        "valor": valor,
        "valido": resultado["valido"],
        "mensaje": resultado["mensaje"],
        "detalles": resultado.get("detalles", {}),
        "timestamp": datetime.now().isoformat()
    }

def validate_cedula(cedula: str) -> dict:
    """Validar cédula costarricense"""
    # Limpiar la cédula
    cedula_limpia = ''.join(filter(str.isdigit, cedula))
    
    if len(cedula_limpia) != 9:
        return {"valido": False, "mensaje": "La cédula debe tener 9 dígitos"}
    
    # Algoritmo básico de validación
    multiplicadores = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    
    for i, digito in enumerate(cedula_limpia[:-1]):
        producto = int(digito) * multiplicadores[i]
        if producto > 9:
            producto = sum(int(d) for d in str(producto))
        suma += producto
    
    digito_verificador = (10 - (suma % 10)) % 10
    
    if digito_verificador == int(cedula_limpia[-1]):
        return {
            "valido": True,
            "mensaje": "Cédula válida",
            "detalles": {"formato": "123-456789-0"}
        }
    else:
        return {"valido": False, "mensaje": "Cédula inválida"}

def validate_telefono(telefono: str) -> dict:
    """Validar número telefónico"""
    telefono_limpio = ''.join(filter(str.isdigit, telefono))
    
    if len(telefono_limpio) == 8 and telefono_limpio.startswith(('2', '6', '7', '8')):
        return {
            "valido": True,
            "mensaje": "Número telefónico válido",
            "detalles": {"tipo": "nacional", "formato": "XXXX-XXXX"}
        }
    elif len(telefono_limpio) == 11 and telefono_limpio.startswith('506'):
        return {
            "valido": True,
            "mensaje": "Número telefónico válido con código de país",
            "detalles": {"tipo": "internacional", "formato": "+506 XXXX-XXXX"}
        }
    else:
        return {"valido": False, "mensaje": "Formato de teléfono inválido"}

def validate_email(email: str) -> dict:
    """Validar dirección de email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return {
            "valido": True,
            "mensaje": "Email válido",
            "detalles": {"dominio": email.split('@')[1]}
        }
    else:
        return {"valido": False, "mensaje": "Formato de email inválido"}

def validate_cuenta_bancaria(cuenta: str) -> dict:
    """Validar cuenta bancaria IBAN"""
    cuenta_limpia = ''.join(filter(str.isalnum, cuenta.upper()))
    
    if len(cuenta_limpia) >= 15 and len(cuenta_limpia) <= 34:
        return {
            "valido": True,
            "mensaje": "Formato de cuenta bancaria válido",
            "detalles": {"tipo": "IBAN", "longitud": len(cuenta_limpia)}
        }
    else:
        return {"valido": False, "mensaje": "Formato de cuenta bancaria inválido"}

# === CALCULADORA ENDPOINTS ===

@app.get("/api/calculadora/tipos")
async def get_calculation_types():
    """Tipos de cálculos disponibles en la calculadora"""
    return {
        "tipos": [
            {
                "id": "prestamo_personal",
                "nombre": "Préstamo Personal",
                "descripcion": "Cálculo de cuotas para préstamos personales",
                "tasa_min": 8.0,
                "tasa_max": 25.0
            },
            {
                "id": "prestamo_hipotecario",
                "nombre": "Préstamo Hipotecario", 
                "descripcion": "Cálculo de cuotas para préstamos hipotecarios",
                "tasa_min": 6.0,
                "tasa_max": 15.0
            },
            {
                "id": "prestamo_vehiculo",
                "nombre": "Préstamo Vehículo",
                "descripcion": "Cálculo de cuotas para préstamos de vehículos",
                "tasa_min": 7.0,
                "tasa_max": 18.0
            }
        ]
    }

@app.post("/api/calculadora/calcular")
async def calculate_loan(data: dict):
    """Calcular préstamo con datos reales"""
    try:
        monto = float(data.get("monto", 0))
        tasa_anual = float(data.get("tasa", 0))
        plazo_meses = int(data.get("plazo", 0))
        tipo = data.get("tipo", "prestamo_personal")
        
        if monto <= 0 or tasa_anual <= 0 or plazo_meses <= 0:
            raise ValueError("Valores deben ser positivos")
        
        # Calcular cuota mensual usando fórmula de amortización
        tasa_mensual = tasa_anual / 100 / 12
        
        if tasa_mensual == 0:
            cuota_mensual = monto / plazo_meses
        else:
            cuota_mensual = monto * (tasa_mensual * (1 + tasa_mensual)**plazo_meses) / ((1 + tasa_mensual)**plazo_meses - 1)
        
        total_pagar = cuota_mensual * plazo_meses
        total_intereses = total_pagar - monto
        
        # Generar tabla de amortización (primeros 12 meses)
        tabla_amortizacion = []
        saldo = monto
        
        for mes in range(1, min(13, plazo_meses + 1)):
            interes_mes = saldo * tasa_mensual
            capital_mes = cuota_mensual - interes_mes
            saldo -= capital_mes
            
            tabla_amortizacion.append({
                "mes": mes,
                "cuota": round(cuota_mensual, 2),
                "capital": round(capital_mes, 2),
                "interes": round(interes_mes, 2),
                "saldo": round(max(0, saldo), 2)
            })
        
        return {
            "monto": monto,
            "tasa_anual": tasa_anual,
            "plazo_meses": plazo_meses,
            "tipo": tipo,
            "cuota_mensual": round(cuota_mensual, 2),
            "total_pagar": round(total_pagar, 2),
            "total_intereses": round(total_intereses, 2),
            "tabla_amortizacion": tabla_amortizacion,
            "recomendaciones": generate_loan_recommendations(monto, tasa_anual, cuota_mensual),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en el cálculo: {str(e)}")

def generate_loan_recommendations(monto: float, tasa: float, cuota: float) -> List[str]:
    """Generar recomendaciones basadas en el cálculo"""
    recomendaciones = []
    
    if tasa > 20:
        recomendaciones.append("💡 La tasa de interés es alta. Considere buscar mejores opciones.")
    
    if cuota > monto * 0.3 / 12:  # Si la cuota es más del 30% del monto anual
        recomendaciones.append("⚠️ La cuota mensual parece elevada. Considere un plazo mayor.")
    
    if monto > 10000000:  # 10 millones de colones
        recomendaciones.append("🏦 Para montos altos, consulte opciones hipotecarias con mejores tasas.")
    
    recomendaciones.append("📊 Siempre compare ofertas de diferentes entidades financieras.")
    recomendaciones.append("💰 Considere realizar pagos adicionales para reducir el total de intereses.")
    
    return recomendaciones

# === MODELOS PYDANTIC PARA TARJETA DE CRÉDITO ===

class SolicitudTarjetaCredito(BaseModel):
    # Datos Personales
    nombre_completo: str
    cedula: str
    fecha_nacimiento: str
    telefono: str
    email: str
    estado_civil: str
    dependientes: int
    
    # Datos Laborales
    empresa: str
    puesto: str
    tipo_contrato: str
    salario_bruto: float
    tiempo_laborando: int  # meses
    telefono_empresa: str
    
    # Datos Financieros
    otros_ingresos: float
    gastos_mensuales: float
    deudas_actuales: float
    tarjetas_existentes: int
    
    # Datos de Referencia
    referencia_personal_nombre: str
    referencia_personal_telefono: str
    referencia_comercial_nombre: str
    referencia_comercial_telefono: str
    
    # Configuración de la tarjeta
    tipo_tarjeta: str  # clasica, oro, platinum
    limite_solicitado: float
    
    @validator('cedula')
    def validar_cedula(cls, v):
        if not v or len(v.replace('-', '')) != 9:
            raise ValueError('La cédula debe tener 9 dígitos')
        return v
    
    @validator('email')
    def validar_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Email inválido')
        return v
    
    @validator('salario_bruto')
    def validar_salario(cls, v):
        if v < 400000:  # Salario mínimo aproximado
            raise ValueError('El salario debe ser mayor a ¢400,000')
        return v

class ResultadoValidacion(BaseModel):
    entidad: str
    status: str
    mensaje: str
    score: int  # 0-100
    detalles: Dict[str, Any]
    tiempo_respuesta: float

class ResultadoSolicitud(BaseModel):
    solicitud_id: str
    aprobada: bool
    limite_aprobado: float
    tasa_interes: float
    score_final: int
    validaciones: List[ResultadoValidacion]
    recomendaciones: List[str]
    siguiente_paso: str
    timestamp: str

# === ENDPOINTS PARA TARJETA DE CRÉDITO ===

@app.get("/api/tarjeta/tipos")
async def get_card_types():
    """Tipos de tarjetas disponibles"""
    return {
        "tipos": [
            {
                "id": "clasica",
                "nombre": "Orbix Clásica",
                "limite_max": 500000,
                "tasa_interes": 24.5,
                "beneficios": ["Compras en línea", "Retiros cajero", "0% comisión primer año"],
                "requisitos": "Salario mínimo ¢400,000"
            },
            {
                "id": "oro",
                "nombre": "Orbix Oro",
                "limite_max": 1500000,
                "tasa_interes": 22.8,
                "beneficios": ["Seguros de viaje", "Compras internacionales", "Puntos Orbix", "Salas VIP"],
                "requisitos": "Salario mínimo ¢800,000"
            },
            {
                "id": "platinum",
                "nombre": "Orbix Platinum",
                "limite_max": 3000000,
                "tasa_interes": 19.9,
                "beneficios": ["Concierge 24/7", "Seguros premium", "Cashback 2%", "Acceso exclusivo"],
                "requisitos": "Salario mínimo ¢1,500,000"
            }
        ]
    }

@app.post("/api/tarjeta/solicitar")
async def procesar_solicitud_tarjeta(solicitud: SolicitudTarjetaCredito):
    """Procesar solicitud completa de tarjeta de crédito"""
    try:
        # Generar ID único para la solicitud
        solicitud_id = f"ORB-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        print(f"🏦 Procesando solicitud {solicitud_id} para {solicitud.nombre_completo}")
        
        # 1. Validaciones básicas de datos
        validaciones_basicas = await validar_datos_basicos(solicitud)
        
        # 2. Consultas a entidades externas
        validaciones_externas = await realizar_consultas_externas(solicitud, solicitud_id)
        
        # 3. Combinar todas las validaciones
        todas_validaciones = validaciones_basicas + validaciones_externas
        
        # 4. Calcular score final y decisión
        resultado = await evaluar_solicitud(solicitud, todas_validaciones, solicitud_id)
        
        # 5. Almacenar resultado (simulado)
        await guardar_solicitud(solicitud_id, solicitud, resultado)
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error procesando solicitud: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error procesando solicitud: {str(e)}")

async def validar_datos_basicos(solicitud: SolicitudTarjetaCredito) -> List[ResultadoValidacion]:
    """Validaciones básicas de formato y coherencia"""
    validaciones = []
    
    # Validación de cédula
    inicio = time.time()
    cedula_valida = validate_cedula(solicitud.cedula)
    validaciones.append(ResultadoValidacion(
        entidad="Orbix Validator",
        status="success" if cedula_valida["valido"] else "error",
        mensaje=cedula_valida["mensaje"],
        score=100 if cedula_valida["valido"] else 0,
        detalles={"tipo": "cedula", "formato": cedula_valida.get("detalles", {})},
        tiempo_respuesta=time.time() - inicio
    ))
    
    # Validación de email
    inicio = time.time()
    email_valido = validate_email(solicitud.email)
    validaciones.append(ResultadoValidacion(
        entidad="Orbix Validator",
        status="success" if email_valido["valido"] else "error",
        mensaje=email_valido["mensaje"],
        score=100 if email_valido["valido"] else 0,
        detalles={"tipo": "email", "dominio": email_valido.get("detalles", {})},
        tiempo_respuesta=time.time() - inicio
    ))
    
    # Validación de teléfono
    inicio = time.time()
    telefono_valido = validate_telefono(solicitud.telefono)
    validaciones.append(ResultadoValidacion(
        entidad="Orbix Validator",
        status="success" if telefono_valido["valido"] else "error",
        mensaje=telefono_valido["mensaje"],
        score=100 if telefono_valido["valido"] else 0,
        detalles={"tipo": "telefono", "formato": telefono_valido.get("detalles", {})},
        tiempo_respuesta=time.time() - inicio
    ))
    
    # Validación de capacidad de pago
    inicio = time.time()
    ingresos_netos = solicitud.salario_bruto + solicitud.otros_ingresos
    gastos_totales = solicitud.gastos_mensuales + solicitud.deudas_actuales
    capacidad_pago = (ingresos_netos - gastos_totales) / ingresos_netos if ingresos_netos > 0 else 0
    
    if capacidad_pago >= 0.3:  # Al menos 30% de capacidad libre
        score_capacidad = min(100, int(capacidad_pago * 200))
        status_capacidad = "success"
        mensaje_capacidad = f"Excelente capacidad de pago: {capacidad_pago:.1%}"
    elif capacidad_pago >= 0.15:
        score_capacidad = min(70, int(capacidad_pago * 300))
        status_capacidad = "warning"
        mensaje_capacidad = f"Capacidad de pago moderada: {capacidad_pago:.1%}"
    else:
        score_capacidad = 30
        status_capacidad = "error"
        mensaje_capacidad = f"Capacidad de pago insuficiente: {capacidad_pago:.1%}"
    
    validaciones.append(ResultadoValidacion(
        entidad="Orbix Financial",
        status=status_capacidad,
        mensaje=mensaje_capacidad,
        score=score_capacidad,
        detalles={
            "ingresos_netos": ingresos_netos,
            "gastos_totales": gastos_totales,
            "capacidad_libre": capacidad_pago,
            "recomendacion_limite": min(solicitud.limite_solicitado, ingresos_netos * 3)
        },
        tiempo_respuesta=time.time() - inicio
    ))
    
    return validaciones

async def realizar_consultas_externas(solicitud: SolicitudTarjetaCredito, solicitud_id: str) -> List[ResultadoValidacion]:
    """Simular consultas a entidades externas"""
    validaciones = []
    
    # Simular tiempo de consulta asíncrona
    await asyncio.sleep(2)
    
    # 1. Consulta CCSS (Caja Costarricense de Seguro Social)
    validaciones.append(await simular_consulta_ccss(solicitud))
    
    # 2. Consulta Protect Credit
    validaciones.append(await simular_consulta_protect_credit(solicitud))
    
    # 3. Consulta BCR (Banco Central)
    validaciones.append(await simular_consulta_bcr(solicitud))
    
    # 4. Consulta Ministerio de Hacienda
    validaciones.append(await simular_consulta_hacienda(solicitud))
    
    return validaciones

async def simular_consulta_ccss(solicitud: SolicitudTarjetaCredito) -> ResultadoValidacion:
    """Simular consulta a la CCSS"""
    inicio = time.time()
    await asyncio.sleep(random.uniform(1, 3))  # Simular tiempo de respuesta
    
    # Simular diferentes escenarios basados en datos
    escenarios = [
        (0.7, "success", "Al día con CCSS", 90, {"cotizaciones_dia": True, "patrono_activo": True}),
        (0.2, "warning", "Atraso menor en cotizaciones", 70, {"cotizaciones_dia": False, "meses_atraso": 2}),
        (0.1, "error", "Atrasos significativos en CCSS", 30, {"cotizaciones_dia": False, "meses_atraso": 6})
    ]
    
    peso_acumulado = 0
    valor_random = random.random()
    
    for probabilidad, status, mensaje, score, detalles in escenarios:
        peso_acumulado += probabilidad
        if valor_random <= peso_acumulado:
            return ResultadoValidacion(
                entidad="CCSS",
                status=status,
                mensaje=mensaje,
                score=score,
                detalles=detalles,
                tiempo_respuesta=time.time() - inicio
            )
    
    # Fallback
    return ResultadoValidacion(
        entidad="CCSS",
        status="success",
        mensaje="Al día con CCSS",
        score=90,
        detalles={"cotizaciones_dia": True},
        tiempo_respuesta=time.time() - inicio
    )

async def simular_consulta_protect_credit(solicitud: SolicitudTarjetaCredito) -> ResultadoValidacion:
    """Simular consulta a Protect Credit"""
    inicio = time.time()
    await asyncio.sleep(random.uniform(0.5, 2))
    
    # Score crediticio simulado basado en salario y deudas
    ratio_deuda = solicitud.deudas_actuales / solicitud.salario_bruto if solicitud.salario_bruto > 0 else 1
    
    if ratio_deuda < 0.3:
        score = random.randint(750, 850)
        status = "success"
        categoria = "Excelente"
    elif ratio_deuda < 0.5:
        score = random.randint(650, 749)
        status = "success"
        categoria = "Bueno"
    elif ratio_deuda < 0.7:
        score = random.randint(550, 649)
        status = "warning"
        categoria = "Regular"
    else:
        score = random.randint(300, 549)
        status = "error"
        categoria = "Deficiente"
    
    return ResultadoValidacion(
        entidad="Protect Credit",
        status=status,
        mensaje=f"Score crediticio: {score} ({categoria})",
        score=min(100, score // 8),  # Convertir a escala 0-100
        detalles={
            "score_crediticio": score,
            "categoria": categoria,
            "historial_pagos": random.choice(["Excelente", "Bueno", "Regular"]),
            "antiguedad_credito": f"{random.randint(1, 15)} años",
            "consultas_recientes": random.randint(0, 5)
        },
        tiempo_respuesta=time.time() - inicio
    )

async def simular_consulta_bcr(solicitud: SolicitudTarjetaCredito) -> ResultadoValidacion:
    """Simular consulta al Banco Central"""
    inicio = time.time()
    await asyncio.sleep(random.uniform(1, 2.5))
    
    # Simular verificación de antecedentes bancarios
    tiene_cuentas_bcr = random.choice([True, False])
    
    if tiene_cuentas_bcr:
        comportamiento = random.choice(["excelente", "bueno", "regular"])
        if comportamiento == "excelente":
            score = 95
            status = "success"
            mensaje = "Cliente de larga data con excelente comportamiento"
        elif comportamiento == "bueno":
            score = 80
            status = "success" 
            mensaje = "Buen cliente con historial positivo"
        else:
            score = 60
            status = "warning"
            mensaje = "Cliente con algunos eventos menores"
    else:
        score = 70
        status = "success"
        mensaje = "Sin historial en BCR - Cliente nuevo"
    
    return ResultadoValidacion(
        entidad="BCR",
        status=status,
        mensaje=mensaje,
        score=score,
        detalles={
            "cliente_bcr": tiene_cuentas_bcr,
            "cuentas_activas": random.randint(0, 3) if tiene_cuentas_bcr else 0,
            "sobregiros": random.randint(0, 2),
            "cheques_devueltos": random.randint(0, 1),
            "antiguedad_relacion": f"{random.randint(1, 10)} años" if tiene_cuentas_bcr else "0 años"
        },
        tiempo_respuesta=time.time() - inicio
    )

async def simular_consulta_hacienda(solicitud: SolicitudTarjetaCredito) -> ResultadoValidacion:
    """Simular consulta al Ministerio de Hacienda"""
    inicio = time.time()
    await asyncio.sleep(random.uniform(1.5, 3))
    
    # Simular estado tributario
    escenarios_tributarios = [
        (0.6, "success", "Al día con obligaciones tributarias", 90, {"declaraciones_dia": True, "deudas_tributarias": 0}),
        (0.25, "warning", "Atraso menor en declaraciones", 70, {"declaraciones_dia": False, "deudas_tributarias": random.randint(50000, 200000)}),
        (0.15, "error", "Deudas tributarias pendientes", 40, {"declaraciones_dia": False, "deudas_tributarias": random.randint(500000, 2000000)})
    ]
    
    peso_acumulado = 0
    valor_random = random.random()
    
    for probabilidad, status, mensaje, score, detalles in escenarios_tributarios:
        peso_acumulado += probabilidad
        if valor_random <= peso_acumulado:
            # Agregar detalles adicionales
            detalles.update({
                "regimen_tributario": random.choice(["Asalariado", "Trabajador Independiente", "Simplificado"]),
                "ultima_declaracion": random.choice(["2024", "2023", "2022"]),
                "multas_pendientes": random.randint(0, 3)
            })
            
            return ResultadoValidacion(
                entidad="Ministerio de Hacienda",
                status=status,
                mensaje=mensaje,
                score=score,
                detalles=detalles,
                tiempo_respuesta=time.time() - inicio
            )
    
    # Fallback en caso de que no se ejecute ningún escenario
    return ResultadoValidacion(
        entidad="Ministerio de Hacienda",
        status="success",
        mensaje="Al día con obligaciones tributarias",
        score=90,
        detalles={
            "declaraciones_dia": True,
            "deudas_tributarias": 0,
            "regimen_tributario": "Asalariado",
            "ultima_declaracion": "2024",
            "multas_pendientes": 0
        },
        tiempo_respuesta=time.time() - inicio
    )

async def evaluar_solicitud(solicitud: SolicitudTarjetaCredito, validaciones: List[ResultadoValidacion], solicitud_id: str) -> ResultadoSolicitud:
    """Evaluar solicitud y generar resultado final"""
    
    # Calcular score promedio ponderado
    peso_por_entidad = {
        "Orbix Validator": 0.15,
        "Orbix Financial": 0.25,
        "CCSS": 0.20,
        "Protect Credit": 0.25,
        "BCR": 0.10,
        "Ministerio de Hacienda": 0.05
    }
    
    score_total = 0
    validaciones_exitosas = 0
    
    for validacion in validaciones:
        peso = peso_por_entidad.get(validacion.entidad, 0.1)
        score_total += validacion.score * peso
        if validacion.status == "success":
            validaciones_exitosas += 1
    
    score_final = int(score_total)
    
    # Determinar aprobación y límite
    if score_final >= 75 and validaciones_exitosas >= 5:
        aprobada = True
        factor_limite = 1.0
        tasa_interes = 19.9 if solicitud.tipo_tarjeta == "platinum" else 22.8 if solicitud.tipo_tarjeta == "oro" else 24.5
    elif score_final >= 60 and validaciones_exitosas >= 4:
        aprobada = True
        factor_limite = 0.7  # 70% del límite solicitado
        tasa_interes = 26.5
    elif score_final >= 45:
        aprobada = True
        factor_limite = 0.5  # 50% del límite solicitado
        tasa_interes = 28.9
    else:
        aprobada = False
        factor_limite = 0
        tasa_interes = 0
    
    # Calcular límite aprobado
    limite_maximo_salario = solicitud.salario_bruto * 3  # Máximo 3x el salario
    limite_solicitado_ajustado = min(solicitud.limite_solicitado, limite_maximo_salario)
    limite_aprobado = limite_solicitado_ajustado * factor_limite if aprobada else 0
    
    # Generar recomendaciones
    recomendaciones = generar_recomendaciones(solicitud, validaciones, score_final, aprobada)
    
    # Determinar siguiente paso
    if aprobada:
        siguiente_paso = "Documentos requeridos enviados por correo. Visita sucursal para firma de contrato."
    else:
        siguiente_paso = "Solicitud no aprobada. Mejora tu perfil crediticio y vuelve a aplicar en 6 meses."
    
    return ResultadoSolicitud(
        solicitud_id=solicitud_id,
        aprobada=aprobada,
        limite_aprobado=limite_aprobado,
        tasa_interes=tasa_interes,
        score_final=score_final,
        validaciones=validaciones,
        recomendaciones=recomendaciones,
        siguiente_paso=siguiente_paso,
        timestamp=datetime.now().isoformat()
    )

def generar_recomendaciones(solicitud: SolicitudTarjetaCredito, validaciones: List[ResultadoValidacion], score: int, aprobada: bool) -> List[str]:
    """Generar recomendaciones personalizadas"""
    recomendaciones = []
    
    if aprobada:
        recomendaciones.append("🎉 ¡Felicitaciones! Tu solicitud ha sido aprobada.")
        recomendaciones.append("💳 Recibirás tu tarjeta en 5-7 días hábiles.")
        recomendaciones.append("📱 Descarga la app Orbix para gestionar tu cuenta.")
        
        if score < 80:
            recomendaciones.append("💡 Mantén un buen historial de pagos para aumentar tu límite.")
    else:
        recomendaciones.append("❌ Tu solicitud no fue aprobada en esta ocasión.")
        
        # Recomendaciones específicas basadas en validaciones
        for validacion in validaciones:
            if validacion.status == "error":
                if validacion.entidad == "CCSS":
                    recomendaciones.append("🏥 Regulariza tu situación con CCSS antes de aplicar nuevamente.")
                elif validacion.entidad == "Protect Credit":
                    recomendaciones.append("📊 Mejora tu score crediticio pagando deudas pendientes.")
                elif validacion.entidad == "Ministerio de Hacienda":
                    recomendaciones.append("🏛️ Ponte al día con tus obligaciones tributarias.")
                elif validacion.entidad == "Orbix Financial":
                    recomendaciones.append("💰 Reduce tus gastos o aumenta tus ingresos para mejorar tu capacidad de pago.")
        
        recomendaciones.append("⏰ Puedes volver a aplicar en 6 meses.")
        recomendaciones.append("🎯 Nuestro equipo te contactará con un plan de mejora personalizado.")
    
    return recomendaciones

async def guardar_solicitud(solicitud_id: str, solicitud: SolicitudTarjetaCredito, resultado: ResultadoSolicitud):
    """Simular guardado de solicitud en base de datos"""
    # En producción, aquí se guardaría en una base de datos real
    print(f"💾 Solicitud {solicitud_id} guardada exitosamente")
    print(f"📊 Score final: {resultado.score_final}")
    print(f"✅ Aprobada: {resultado.aprobada}")
    if resultado.aprobada:
        print(f"💳 Límite aprobado: ¢{resultado.limite_aprobado:,.0f}")

@app.get("/api/tarjeta/solicitud/{solicitud_id}")
async def consultar_solicitud(solicitud_id: str):
    """Consultar estado de una solicitud específica"""
    # En producción, consultar base de datos
    return {
        "solicitud_id": solicitud_id,
        "status": "En proceso",
        "mensaje": "Su solicitud está siendo evaluada por nuestro equipo especializado.",
        "tiempo_estimado": "24-48 horas",
        "documentos_pendientes": [],
        "contacto": "+506 2000-0000"
    }

@app.get("/api/tarjeta/calculadora")
async def calculadora_tarjeta():
    """Calculadora de pagos para tarjeta de crédito"""
    return {
        "tipos_calculo": [
            "Pago mínimo mensual",
            "Tiempo para pagar saldo",
            "Intereses por financiamiento",
            "Pago para liquidar en X meses"
        ],
        "tasas_referencia": {
            "clasica": 24.5,
            "oro": 22.8,
            "platinum": 19.9
        }
    }

@app.post("/api/tarjeta/calcular-pagos")
async def calcular_pagos_tarjeta(data: dict):
    """Calcular diferentes escenarios de pago para tarjeta"""
    try:
        saldo = float(data.get("saldo", 0))
        tasa_anual = float(data.get("tasa", 24.5))
        tipo_calculo = data.get("tipo", "pago_minimo")
        
        tasa_mensual = tasa_anual / 100 / 12
        
        if tipo_calculo == "pago_minimo":
            # Pago mínimo típicamente 2-3% del saldo
            pago_minimo = max(saldo * 0.025, 10000)  # Mínimo ¢10,000
            return {
                "pago_minimo": round(pago_minimo, 2),
                "interes_mensual": round(saldo * tasa_mensual, 2),
                "capital_pagado": round(pago_minimo - (saldo * tasa_mensual), 2),
                "tiempo_liquidacion": "Más de 30 años" if pago_minimo <= saldo * tasa_mensual else "Calculable"
            }
        
        elif tipo_calculo == "liquidar_meses":
            meses = int(data.get("meses", 12))
            if meses <= 0:
                raise ValueError("Meses debe ser mayor a 0")
            
            # Fórmula de anualidad
            pago_mensual = saldo * (tasa_mensual * (1 + tasa_mensual)**meses) / ((1 + tasa_mensual)**meses - 1)
            total_pagado = pago_mensual * meses
            total_intereses = total_pagado - saldo
            
            return {
                "pago_mensual": round(pago_mensual, 2),
                "total_pagado": round(total_pagado, 2),
                "total_intereses": round(total_intereses, 2),
                "ahorro_vs_minimo": "Cálculo disponible"
            }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en cálculo: {str(e)}")

# === ENDPOINTS ESPECÍFICOS PARA SENTINEL ===

@app.get("/api/sentinel/network-traffic")
async def get_network_traffic():
    """Datos específicos de tráfico de red en tiempo real"""
    hour = datetime.now().hour
    multiplier = 1.8 if 8 <= hour <= 18 else 1.3 if 19 <= hour <= 23 else 0.6
    
    entrada = round(random.uniform(0, 25) * multiplier, 1)
    salida = round(random.uniform(0, 20) * multiplier, 1)
    
    return {
        "entrada_mbps": entrada,
        "salida_mbps": salida,
        "total_gb_hoy": round((entrada + salida) * 0.12, 2),
        "pico_mbps": round(max(entrada, salida) * 1.3, 1),
        "disponible_mbps": 100,
        "ultimo_update": datetime.now().isoformat()
    }

@app.get("/api/sentinel/security-events")
async def get_security_events():
    """Eventos de seguridad actualizados"""
    hour = datetime.now().hour
    threat_level = 1.5 if 8 <= hour <= 18 else 1.2 if 19 <= hour <= 23 else 0.8
    
    criticos = random.randint(0, int(5 * threat_level))
    advertencias = random.randint(0, int(12 * threat_level))
    info = random.randint(3, int(25 * threat_level))
    
    return {
        "criticos": criticos,
        "advertencias": advertencias,
        "info": info,
        "total": criticos + advertencias + info,
        "nivel_riesgo": "ALTO" if criticos > 3 else "MEDIO" if advertencias > 8 else "BAJO",
        "ultimo_update": datetime.now().isoformat()
    }

@app.get("/api/sentinel/system-performance")
async def get_system_performance():
    """Rendimiento del sistema en tiempo real"""
    # Simular variaciones más naturales
    base_cpu = 20.9
    base_ram = 47.2
    base_disk = 73.5
    
    # Pequeñas variaciones aleatorias
    cpu_variation = random.uniform(-5, 15)
    ram_variation = random.uniform(-10, 20)
    disk_variation = random.uniform(-2, 8)
    
    cpu = max(5, min(95, base_cpu + cpu_variation))
    ram = max(10, min(90, base_ram + ram_variation))
    disk = max(30, min(95, base_disk + disk_variation))
    
    return {
        "cpu_porcentaje": round(cpu, 1),
        "ram_porcentaje": round(ram, 1),
        "disco_porcentaje": round(disk, 1),
        "estado": "NORMAL" if cpu < 80 and ram < 80 else "ALERTA" if cpu < 90 and ram < 90 else "CRÍTICO",
        "procesos_activos": random.randint(180, 250),
        "temperatura_cpu": round(random.uniform(35, 65), 1),
        "ultimo_update": datetime.now().isoformat()
    }

@app.get("/api/sentinel/threat-detection")
async def get_threat_detection():
    """Detección de amenazas actualizada"""
    hour = datetime.now().hour
    activity_level = 1.5 if 8 <= hour <= 18 else 1.2 if 19 <= hour <= 23 else 0.7
    
    detectadas = random.randint(0, int(8 * activity_level))
    bloqueadas = random.randint(0, int(6 * activity_level))
    resueltas = random.randint(0, int(5 * activity_level))
    
    nivel_amenaza = "ALTO" if detectadas > 5 else "MEDIO" if detectadas > 2 else "BAJO"
    
    return {
        "detectadas": detectadas,
        "bloqueadas": bloqueadas,
        "resueltas": resueltas,
        "investigando": random.randint(0, 3),
        "nivel_amenaza": nivel_amenaza,
        "tipos_amenaza": {
            "malware": random.randint(0, 3),
            "phishing": random.randint(0, 2),
            "ddos": random.randint(0, 1),
            "intrusion": random.randint(0, 2),
            "exploit": random.randint(0, 1)
        },
        "ultimo_update": datetime.now().isoformat()
    }

@app.get("/api/sentinel/bandwidth")
async def get_bandwidth():
    """Uso de ancho de banda en tiempo real"""
    hour = datetime.now().hour
    usage_base = 30 if 2 <= hour <= 6 else 60 if 8 <= hour <= 18 else 45
    
    current = round(random.uniform(usage_base - 15, usage_base + 25), 1)
    peak = round(random.uniform(max(current, 70), 100), 1)
    average = round(random.uniform(30, 65), 1)
    
    return {
        "uso_actual_mbps": current,
        "pico_mbps": peak,
        "promedio_mbps": average,
        "disponible_mbps": 100,
        "porcentaje_uso": round(current, 1),
        "calidad_conexion": "EXCELENTE" if current < 50 else "BUENA" if current < 75 else "SATURADA",
        "ultimo_update": datetime.now().isoformat()
    }

@app.get("/api/sentinel/geographic")
async def get_geographic():
    """Actividad geográfica en tiempo real"""
    hour = datetime.now().hour
    traffic_mult = 1.5 if 8 <= hour <= 18 else 1.2 if 19 <= hour <= 23 else 0.8
    
    paises_data = {
        "Costa Rica": int(random.randint(150, 350) * traffic_mult),
        "Estados Unidos": int(random.randint(80, 220) * traffic_mult),
        "México": int(random.randint(40, 130) * traffic_mult),
        "Colombia": int(random.randint(25, 110) * traffic_mult),
        "España": int(random.randint(20, 90) * traffic_mult),
        "Brasil": int(random.randint(15, 70) * traffic_mult),
        "Argentina": int(random.randint(10, 60) * traffic_mult),
        "Chile": int(random.randint(8, 45) * traffic_mult)
    }
    
    ips_sospechosas = random.randint(0, 12)
    paises_unicos = len(paises_data) + random.randint(2, 8)
    
    return {
        "paises": paises_data,
        "ips_unicas": sum(paises_data.values()),
        "ips_sospechosas": ips_sospechosas,
        "paises_unicos": paises_unicos,
        "conexiones_activas": sum(paises_data.values()),
        "top_pais": max(paises_data, key=lambda k: paises_data[k]),
        "riesgo_geografico": "ALTO" if ips_sospechosas > 8 else "MEDIO" if ips_sospechosas > 4 else "BAJO",
        "ultimo_update": datetime.now().isoformat()
    }

@app.get("/api/sentinel/dashboard-complete")
async def get_complete_dashboard():
    """Dashboard completo con todos los datos agregados"""
    try:
        # Obtener datos de todos los endpoints
        network = await get_network_traffic()
        security = await get_security_events()
        performance = await get_system_performance()
        threats = await get_threat_detection()
        bandwidth = await get_bandwidth()
        geographic = await get_geographic()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "status": "operational",
            "network_traffic": network,
            "security_events": security,
            "system_performance": performance,
            "threat_detection": threats,
            "bandwidth": bandwidth,
            "geographic": geographic,
            "general_health": {
                "overall_status": "NORMAL",
                "uptime": "99.97%",
                "services_online": random.randint(45, 52),
                "services_total": 52
            }
        }
    except Exception as e:
        return {
            "error": f"Error obteniendo datos del dashboard: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
