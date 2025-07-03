"""
🧠 Orbix Systems - FastAPI Backend
Servidor API principal para validaciones, calculadora y monitoreo
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
from datetime import datetime
import json
import random

# Configuración de la aplicación
app = FastAPI(
    title="🧠 Orbix Systems API",
    description="API principal para validaciones crediticias, calculadora financiera y monitoreo de seguridad",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# MODELOS PYDANTIC
# ===============================

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]

class ValidationRequest(BaseModel):
    cedula: str
    tipo_validacion: str  # "ccss", "sugef", "hacienda", "tss"
    datos_adicionales: Optional[Dict[str, Any]] = None

class ValidationResponse(BaseModel):
    success: bool
    cedula: str
    tipo_validacion: str
    resultado: Dict[str, Any]
    timestamp: str
    codigo_respuesta: str

class CalculatorRequest(BaseModel):
    monto_prestamo: float
    plazo_meses: int
    tasa_interes: float
    tipo_calculo: str  # "frances", "aleman", "americano"
    ingresos_mensuales: Optional[float] = None
    gastos_mensuales: Optional[float] = None

class CalculatorResponse(BaseModel):
    success: bool
    cuota_mensual: float
    total_pagar: float
    total_intereses: float
    capacidad_pago: Optional[float] = None
    recomendacion: str
    cronograma: List[Dict[str, Any]]

class SentinelMetrics(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_in: float
    network_out: float
    active_connections: int
    threats_detected: int
    threats_blocked: int
    timestamp: str

# ===============================
# ENDPOINTS PRINCIPALES
# ===============================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raíz con información básica"""
    return {
        "message": "🧠 Orbix Systems API",
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de verificación de salud del sistema"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        services={
            "fastapi": "running",
            "database": "checking",
            "redis": "checking",
            "odoo": "disconnected"
        }
    )

# ===============================
# MÓDULO VALIDACIONES
# ===============================

@app.post("/api/validaciones/validate", response_model=ValidationResponse)
async def validate_cedula(request: ValidationRequest):
    """
    Endpoint principal para validaciones de cédula
    Integra con CCSS, SUGEF, Hacienda y TSS
    """
    try:
        # Simulación de validación (integrar con APIs reales)
        resultado = await _procesar_validacion(request.cedula, request.tipo_validacion)
        
        return ValidationResponse(
            success=True,
            cedula=request.cedula,
            tipo_validacion=request.tipo_validacion,
            resultado=resultado,
            timestamp=datetime.now().isoformat(),
            codigo_respuesta="VAL_200"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en validación: {str(e)}")

@app.get("/api/validaciones/tipos")
async def get_validation_types():
    """Obtiene los tipos de validación disponibles"""
    return {
        "tipos_validacion": [
            {
                "codigo": "ccss",
                "nombre": "Caja Costarricense de Seguro Social",
                "descripcion": "Validación de estado en CCSS",
                "activo": True
            },
            {
                "codigo": "sugef",
                "nombre": "Superintendencia General de Entidades Financieras",
                "descripcion": "Consulta en centrales de riesgo",
                "activo": True
            },
            {
                "codigo": "hacienda",
                "nombre": "Ministerio de Hacienda",
                "descripcion": "Validación tributaria",
                "activo": True
            },
            {
                "codigo": "tss",
                "nombre": "Tribunal Supremo de Elecciones",
                "descripcion": "Validación de identidad",
                "activo": True
            }
        ]
    }

async def _procesar_validacion(cedula: str, tipo: str) -> Dict[str, Any]:
    """Procesa la validación según el tipo especificado"""
    # Simulación de respuestas (integrar con APIs reales)
    base_response = {
        "cedula_valida": len(cedula) >= 9,
        "fecha_consulta": datetime.now().isoformat(),
        "proveedor": tipo.upper()
    }
    
    if tipo == "ccss":
        return {
            **base_response,
            "estado_ccss": "ACTIVO" if random.choice([True, False]) else "INACTIVO",
            "ultima_cotizacion": "2024-12-01",
            "meses_cotizados": random.randint(12, 240)
        }
    elif tipo == "sugef":
        return {
            **base_response,
            "score_crediticio": random.randint(300, 850),
            "estado_morosidad": "SIN_MOROSIDAD" if random.choice([True, False]) else "MOROSO",
            "deudas_activas": random.randint(0, 5)
        }
    elif tipo == "hacienda":
        return {
            **base_response,
            "estado_tributario": "AL_DIA" if random.choice([True, False]) else "ATRASADO",
            "deudas_pendientes": random.uniform(0, 50000)
        }
    elif tipo == "tss":
        return {
            **base_response,
            "cedula_vigente": True,
            "nombre_completo": "NOMBRE SIMULADO",
            "fecha_nacimiento": "1990-01-01"
        }
    
    return base_response

# ===============================
# MÓDULO CALCULADORA
# ===============================

@app.post("/api/calculadora/calculate", response_model=CalculatorResponse)
async def calculate_loan(request: CalculatorRequest):
    """
    Calculadora de préstamos con diferentes tipos de amortización
    """
    try:
        cronograma = []
        
        if request.tipo_calculo == "frances":
            # Sistema Francés (cuota fija)
            tasa_mensual = request.tasa_interes / 100 / 12
            num_pagos = request.plazo_meses
            
            cuota_mensual = (request.monto_prestamo * tasa_mensual * 
                           (1 + tasa_mensual) ** num_pagos) / \
                          ((1 + tasa_mensual) ** num_pagos - 1)
            
            saldo = request.monto_prestamo
            
            for mes in range(1, num_pagos + 1):
                interes = saldo * tasa_mensual
                capital = cuota_mensual - interes
                saldo = saldo - capital
                
                cronograma.append({
                    "mes": mes,
                    "cuota": round(cuota_mensual, 2),
                    "capital": round(capital, 2),
                    "interes": round(interes, 2),
                    "saldo": round(max(0, saldo), 2)
                })
        
        total_pagar = sum(item["cuota"] for item in cronograma)
        total_intereses = total_pagar - request.monto_prestamo
        
        # Análisis de capacidad de pago
        capacidad_pago = None
        recomendacion = "Préstamo calculado correctamente"
        
        if request.ingresos_mensuales and request.gastos_mensuales:
            ingresos_netos = request.ingresos_mensuales - request.gastos_mensuales
            capacidad_pago = (cuota_mensual / ingresos_netos) * 100
            
            if capacidad_pago > 40:
                recomendacion = "⚠️ Cuota muy alta. Se recomienda reducir monto o aumentar plazo."
            elif capacidad_pago > 30:
                recomendacion = "⚡ Cuota moderada. Revisar otros gastos."
            else:
                recomendacion = "✅ Cuota adecuada para su capacidad de pago."
        
        return CalculatorResponse(
            success=True,
            cuota_mensual=round(cuota_mensual, 2),
            total_pagar=round(total_pagar, 2),
            total_intereses=round(total_intereses, 2),
            capacidad_pago=round(capacidad_pago, 2) if capacidad_pago else None,
            recomendacion=recomendacion,
            cronograma=cronograma[:12]  # Solo primeros 12 meses para la respuesta
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en cálculo: {str(e)}")

@app.get("/api/calculadora/tipos")
async def get_calculation_types():
    """Obtiene los tipos de cálculo disponibles"""
    return {
        "tipos_calculo": [
            {
                "codigo": "frances",
                "nombre": "Sistema Francés",
                "descripcion": "Cuotas fijas, amortización creciente"
            },
            {
                "codigo": "aleman",
                "nombre": "Sistema Alemán",
                "descripcion": "Capital fijo, cuotas decrecientes"
            },
            {
                "codigo": "americano",
                "nombre": "Sistema Americano",
                "descripcion": "Solo intereses, capital al final"
            }
        ]
    }

# ===============================
# MÓDULO SENTINEL
# ===============================

@app.get("/api/sentinel/metrics", response_model=SentinelMetrics)
async def get_sentinel_metrics():
    """Obtiene métricas en tiempo real del sistema"""
    return SentinelMetrics(
        cpu_usage=random.uniform(10, 80),
        memory_usage=random.uniform(20, 90),
        disk_usage=random.uniform(30, 70),
        network_in=random.uniform(5, 50),
        network_out=random.uniform(3, 30),
        active_connections=random.randint(50, 200),
        threats_detected=random.randint(0, 10),
        threats_blocked=random.randint(0, 5),
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/sentinel/events")
async def get_security_events():
    """Obtiene eventos de seguridad recientes"""
    events = []
    event_types = [
        {"type": "network", "message": "Nueva conexión detectada", "level": "info"},
        {"type": "security", "message": "Intento de login fallido", "level": "warning"},
        {"type": "threat", "message": "Malware bloqueado", "level": "critical"},
        {"type": "system", "message": "Backup completado", "level": "success"}
    ]
    
    for i in range(10):
        event = random.choice(event_types)
        events.append({
            "id": f"evt_{i+1}",
            "timestamp": datetime.now().isoformat(),
            "type": event["type"],
            "level": event["level"],
            "message": event["message"],
            "source": f"server-{random.randint(1, 5)}"
        })
    
    return {"events": events}

@app.get("/api/sentinel/status")
async def get_system_status():
    """Estado general del sistema"""
    return {
        "system_status": "operational",
        "uptime": "99.9%",
        "services": {
            "web_server": {"status": "running", "port": 3000},
            "api_server": {"status": "running", "port": 8000},
            "database": {"status": "checking", "port": 5432},
            "redis": {"status": "checking", "port": 6379}
        },
        "last_update": datetime.now().isoformat()
    }

# ===============================
# ENDPOINTS DE UTILIDAD
# ===============================

@app.get("/api/info")
async def get_api_info():
    """Información general de la API"""
    return {
        "name": "Orbix Systems API",
        "version": "1.0.0",
        "description": "API para validaciones, calculadora y monitoreo",
        "endpoints": {
            "validaciones": "/api/validaciones/*",
            "calculadora": "/api/calculadora/*",
            "sentinel": "/api/sentinel/*"
        },
        "docs": "/docs",
        "health": "/health"
    }

# ===============================
# CONFIGURACIÓN DEL SERVIDOR
# ===============================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("🧠 Iniciando Orbix Systems API...")
    print(f"📡 Servidor: http://{host}:{port}")
    print(f"📚 Documentación: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
