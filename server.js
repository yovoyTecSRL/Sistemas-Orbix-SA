const express = require('express');
const path = require('path');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 3000;
const FASTAPI_URL = process.env.FASTAPI_URL || 'http://localhost:3001';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Proxy para FastAPI de validaciones
app.use('/api/orbix', createProxyMiddleware({
  target: FASTAPI_URL,
  changeOrigin: true,
  pathRewrite: {
    '^/api/orbix': ''
  },
  onError: (err, req, res) => {
    console.log('Error conectando con FastAPI:', err.message);
    res.status(503).json({
      error: 'Servicio de validaciones no disponible',
      message: 'Por favor, inicie el servidor FastAPI en puerto 8000'
    });
  }
}));

// Ruta para validaciones que redirige a FastAPI
app.get('/validaciones', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'validaciones.html'));
});

// Ruta para Sentinel
app.get('/sentinel', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'sentinel.html'));
});

// Ruta para calculadora
app.get('/calculadora', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'calculadora.html'));
});

// Servir archivos estáticos
app.use(express.static(path.join(__dirname)));
app.use('/public', express.static(path.join(__dirname, 'public')));

// Ruta principal
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Rutas para las páginas de servicios
app.get('/validaciones', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'validaciones.html'));
});

app.get('/calculadora', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'calculadora.html'));
});

app.get('/sentinel', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'sentinel.html'));
});

// Ruta de salud del servidor
app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: '🧠 Orbix Systems está funcionando correctamente',
    timestamp: new Date().toISOString()
  });
});

// Ruta para API (futuras extensiones)
app.get('/api/status', (req, res) => {
  res.json({
    service: 'Orbix Systems',
    version: '1.0.0',
    status: 'active',
    features: [
      '✅ Validaciones',
      '🧮 Calculadora',
      '🛡️ Sentinel',
      '🚀 ERP Integration'
    ]
  });
});

// Manejo de errores 404
app.use((req, res) => {
  res.status(404).sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Iniciar servidor
app.listen(PORT, '0.0.0.0', () => {
  console.log('🚀 ===============================================');
  console.log('🧠 Orbix Systems Server Iniciado');
  console.log('🌐 URL: http://localhost:' + PORT);
  console.log('🔧 Puerto: ' + PORT);
  console.log('✅ Estado: Activo y listo para recibir conexiones');
  console.log('===============================================');
});

module.exports = app;
