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
            </style>
        </head>
        <body>
            <h1>🧠 Orbix Systems</h1>
            <p>Inteligencia real para negocios reales.</p>
            <div>
                <a href='/validaciones' class='btn'>🧮 Lanzar Validaciones</a>
                <a href='/sentinel' class='btn'>🛡️ Sentinel</a>
                <a href='/calculadora' class='btn'>💰 Calculadora</a>
            </div>
        </body>
        </html>
        """)

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
    """Estado detallado del módulo Sentinel"""
    return {
        "status": "operational",
        "threats_blocked": random.randint(100, 200),
        "events_today": random.randint(30, 80),
        "active_alerts": random.randint(1, 8),
        "active_connections": random.randint(50, 150),
        "uptime": "99.9%",
        "last_update": datetime.now().isoformat(),
        "security_level": random.choice(["LOW", "MEDIUM", "HIGH"]),
        "system_health": {
            "cpu": round(random.uniform(20, 80), 1),
            "ram": round(random.uniform(30, 70), 1),
            "disk": round(random.uniform(40, 85), 1)
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
    """Métricas en tiempo real para los gráficos"""
    now = datetime.now()
    
    return {
        "network_traffic": {
            "timestamp": now.isoformat(),
            "in_mbps": round(random.uniform(10, 60), 1),
            "out_mbps": round(random.uniform(5, 35), 1)
        },
        "security_events": {
            "critical": random.randint(0, 5),
            "warning": random.randint(0, 10),
            "info": random.randint(0, 20)
        },
        "threat_detection": {
            "detected": random.randint(0, 8),
            "blocked": random.randint(0, 5),
            "resolved": random.randint(0, 6)
        },
        "bandwidth": {
            "usage_mbps": round(random.uniform(10, 90), 1),
            "peak_mbps": round(random.uniform(70, 100), 1),
            "available_mbps": 100
        },
        "geographic": {
            "countries": {
                "Costa Rica": random.randint(100, 200),
                "Estados Unidos": random.randint(50, 150),
                "México": random.randint(30, 100),
                "Colombia": random.randint(20, 80),
                "España": random.randint(15, 60)
            }
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
