// cyber-dashboard.js
// Dashboard de métricas en tiempo real para Orbix Systems
// Requiere Chart.js

let charts = {};

function crearGraficosDashboard() {
  // CPU Usage
  const cpuCtx = document.getElementById('chart-cpu').getContext('2d');
  charts.cpu = new Chart(cpuCtx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'CPU (%)',
        data: [],
        borderColor: '#00ff88',
        backgroundColor: 'rgba(0,255,136,0.1)',
        tension: 0.3,
        fill: true,
        pointRadius: 0
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { min: 0, max: 100, ticks: { color: '#00ff88' } },
        x: { ticks: { color: '#a0b3cc' } }
      }
    }
  });

  // Memoria
  const memCtx = document.getElementById('chart-mem').getContext('2d');
  charts.mem = new Chart(memCtx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Memoria (%)',
        data: [],
        borderColor: '#00d4ff',
        backgroundColor: 'rgba(0,212,255,0.1)',
        tension: 0.3,
        fill: true,
        pointRadius: 0
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { min: 0, max: 100, ticks: { color: '#00d4ff' } },
        x: { ticks: { color: '#a0b3cc' } }
      }
    }
  });

  // Red
  const netCtx = document.getElementById('chart-net').getContext('2d');
  charts.net = new Chart(netCtx, {
    type: 'bar',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Enviados (KB/s)',
          data: [],
          backgroundColor: 'rgba(0,255,136,0.5)',
          borderColor: '#00ff88',
          borderWidth: 1
        },
        {
          label: 'Recibidos (KB/s)',
          data: [],
          backgroundColor: 'rgba(0,212,255,0.5)',
          borderColor: '#00d4ff',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: '#a0b3cc' } } },
      scales: {
        y: { beginAtZero: true, ticks: { color: '#00ff88' } },
        x: { ticks: { color: '#a0b3cc' } }
      }
    }
  });
}

function actualizarGraficosDashboard(metrics) {
  const now = new Date();
  const timeLabel = now.toLocaleTimeString('es-CR', { hour12: false });

  // CPU
  if (charts.cpu) {
    if (charts.cpu.data.labels.length > 20) {
      charts.cpu.data.labels.shift();
      charts.cpu.data.datasets[0].data.shift();
    }
    charts.cpu.data.labels.push(timeLabel);
    charts.cpu.data.datasets[0].data.push(metrics.cpu || 0);
    charts.cpu.update();
  }
  // Memoria
  if (charts.mem) {
    if (charts.mem.data.labels.length > 20) {
      charts.mem.data.labels.shift();
      charts.mem.data.datasets[0].data.shift();
    }
    charts.mem.data.labels.push(timeLabel);
    charts.mem.data.datasets[0].data.push(metrics.memory || 0);
    charts.mem.update();
  }
  // Red
  if (charts.net) {
    if (charts.net.data.labels.length > 20) {
      charts.net.data.labels.shift();
      charts.net.data.datasets[0].data.shift();
      charts.net.data.datasets[1].data.shift();
    }
    charts.net.data.labels.push(timeLabel);
    charts.net.data.datasets[0].data.push(metrics.net_sent || 0);
    charts.net.data.datasets[1].data.push(metrics.net_recv || 0);
    charts.net.update();
  }
}

function obtenerYActualizarDashboard() {
  fetch('/api/sentinel/metrics')
    .then(r => r.json())
    .then(metrics => {
      actualizarGraficosDashboard(metrics);
    })
    .catch(() => {});
}

document.addEventListener('DOMContentLoaded', function() {
  if (window.Chart && document.getElementById('chart-cpu')) {
    crearGraficosDashboard();
    obtenerYActualizarDashboard();
    setInterval(obtenerYActualizarDashboard, 3000);
  }
});
