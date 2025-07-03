// Orbix Cyber Effects - JavaScript para efectos futuristas
class OrbixCyberEffects {
  constructor() {
    this.particles = [];
    this.codeLines = [];
    this.init();
  }

  init() {
    this.createParticleSystem();
    this.createCodeRain();
    this.createDataMatrix();
    this.initHoverEffects();
    this.startAnimationLoop();
  }

  createParticleSystem() {
    const container = document.createElement('div');
    container.className = 'floating-particles';
    document.body.appendChild(container);

    // Crear 50 partículas
    for (let i = 0; i < 50; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      
      // Posición aleatoria
      particle.style.left = Math.random() * 100 + '%';
      particle.style.animationDelay = Math.random() * 20 + 's';
      particle.style.animationDuration = (Math.random() * 10 + 15) + 's';
      
      container.appendChild(particle);
      this.particles.push(particle);
    }
  }

  createCodeRain() {
    const container = document.createElement('div');
    container.className = 'code-rain';
    document.body.appendChild(container);

    const codeSnippets = [
      'function validate(data) {',
      'if (user.authenticated) {',
      'return apiResponse.json();',
      'const token = jwt.sign(...);',
      'db.collection.find({...});',
      'export default class API {',
      'async processPayment() {',
      'const hash = crypto.hash(...);',
      'if (security.check()) {',
      'logger.info("Request processed");'
    ];

    // Crear 20 líneas de código
    for (let i = 0; i < 20; i++) {
      const codeLine = document.createElement('div');
      codeLine.className = 'code-line';
      codeLine.textContent = codeSnippets[Math.floor(Math.random() * codeSnippets.length)];
      
      codeLine.style.left = Math.random() * 100 + '%';
      codeLine.style.animationDelay = Math.random() * 15 + 's';
      codeLine.style.animationDuration = (Math.random() * 5 + 10) + 's';
      
      container.appendChild(codeLine);
      this.codeLines.push(codeLine);
    }
  }

  createDataMatrix() {
    const container = document.createElement('div');
    container.className = 'data-matrix';
    document.body.appendChild(container);

    const matrixChars = '0123456789ABCDEFABCDEF';
    const columns = Math.floor(window.innerWidth / 20);

    for (let i = 0; i < columns; i++) {
      const column = document.createElement('div');
      column.className = 'matrix-column';
      column.style.left = (i * 20) + 'px';
      column.style.animationDelay = Math.random() * 10 + 's';
      column.style.animationDuration = (Math.random() * 5 + 8) + 's';

      // Generar cadena de caracteres
      let text = '';
      for (let j = 0; j < 20; j++) {
        text += matrixChars[Math.floor(Math.random() * matrixChars.length)] + '<br>';
      }
      column.innerHTML = text;

      container.appendChild(column);
    }
  }

  initHoverEffects() {
    // Añadir efectos hover a botones y cards
    const elements = document.querySelectorAll('.btn-primary, .calc-card, .tool-card, .stat-box, .chart-container');
    
    elements.forEach(element => {
      element.classList.add('cyber-hover-effect');
      
      element.addEventListener('mouseenter', () => {
        this.createHoverParticles(element);
      });
    });
  }

  createHoverParticles(element) {
    const rect = element.getBoundingClientRect();
    
    for (let i = 0; i < 5; i++) {
      const particle = document.createElement('div');
      particle.style.position = 'absolute';
      particle.style.width = '2px';
      particle.style.height = '2px';
      particle.style.background = 'var(--primary-color)';
      particle.style.borderRadius = '50%';
      particle.style.pointerEvents = 'none';
      particle.style.zIndex = '1000';
      particle.style.left = (rect.left + Math.random() * rect.width) + 'px';
      particle.style.top = (rect.top + Math.random() * rect.height) + 'px';
      
      document.body.appendChild(particle);
      
      // Animar partícula
      const animation = particle.animate([
        { 
          opacity: 1, 
          transform: 'translateY(0px) scale(1)' 
        },
        { 
          opacity: 0, 
          transform: 'translateY(-50px) scale(0)' 
        }
      ], {
        duration: 1000,
        easing: 'ease-out'
      });
      
      animation.onfinish = () => {
        document.body.removeChild(particle);
      };
    }
  }

  createTypingEffect(element, text, speed = 50) {
    element.innerHTML = '';
    let i = 0;
    
    const typeInterval = setInterval(() => {
      if (i < text.length) {
        element.innerHTML += text.charAt(i);
        i++;
      } else {
        clearInterval(typeInterval);
        
        // Añadir cursor parpadeante
        const cursor = document.createElement('span');
        cursor.className = 'terminal-cursor';
        cursor.textContent = '█';
        element.appendChild(cursor);
      }
    }, speed);
  }

  createGlitchEffect(element, duration = 2000) {
    const originalText = element.textContent;
    element.setAttribute('data-text', originalText);
    element.classList.add('glitch-text');
    
    setTimeout(() => {
      element.classList.remove('glitch-text');
      element.removeAttribute('data-text');
    }, duration);
  }

  createHologramScan(element) {
    element.classList.add('hologram-scan');
    
    setTimeout(() => {
      element.classList.remove('hologram-scan');
    }, 3000);
  }

  startAnimationLoop() {
    const animate = () => {
      // Actualizar partículas si es necesario
      this.updateParticles();
      requestAnimationFrame(animate);
    };
    animate();
  }

  updateParticles() {
    // Lógica de actualización de partículas si es necesario
    // Por ahora, las animaciones CSS manejan todo
  }

  // Método para inicializar efectos en elementos específicos
  applyToElement(selector, effect) {
    const elements = document.querySelectorAll(selector);
    
    elements.forEach(element => {
      switch(effect) {
        case 'typing':
          const text = element.textContent;
          this.createTypingEffect(element, text);
          break;
        case 'glitch':
          this.createGlitchEffect(element);
          break;
        case 'scan':
          this.createHologramScan(element);
          break;
        case 'pulse':
          element.classList.add('pulse-btn');
          break;
      }
    });
  }

  // Crear efecto de terminal
  createTerminal(container, commands) {
    const terminal = document.createElement('div');
    terminal.className = 'cyber-terminal';
    
    commands.forEach((command, index) => {
      setTimeout(() => {
        const line = document.createElement('div');
        line.className = 'terminal-line';
        this.createTypingEffect(line, command, 30);
        terminal.appendChild(line);
      }, index * 1500);
    });
    
    container.appendChild(terminal);
  }

  // Crear conexiones de red neuronal
  createNeuralNetwork(container) {
    const network = document.createElement('div');
    network.className = 'neural-network';
    
    // Crear neuronas
    for (let i = 0; i < 20; i++) {
      const neuron = document.createElement('div');
      neuron.className = 'neuron';
      neuron.style.left = Math.random() * 100 + '%';
      neuron.style.top = Math.random() * 100 + '%';
      neuron.style.animationDelay = Math.random() * 3 + 's';
      network.appendChild(neuron);
    }
    
    // Crear conexiones
    for (let i = 0; i < 15; i++) {
      const connection = document.createElement('div');
      connection.className = 'connection';
      connection.style.left = Math.random() * 100 + '%';
      connection.style.top = Math.random() * 100 + '%';
      connection.style.width = Math.random() * 200 + 50 + 'px';
      connection.style.transform = 'rotate(' + Math.random() * 360 + 'deg)';
      connection.style.animationDelay = Math.random() * 2 + 's';
      network.appendChild(connection);
    }
    
    container.appendChild(network);
  }

  // Limpiar efectos
  destroy() {
    // Limpiar partículas
    const particles = document.querySelector('.floating-particles');
    const codeRain = document.querySelector('.code-rain');
    const dataMatrix = document.querySelector('.data-matrix');
    
    if (particles) particles.remove();
    if (codeRain) codeRain.remove();
    if (dataMatrix) dataMatrix.remove();
  }
}

// Auto-inicializar cuando se carga el DOM
document.addEventListener('DOMContentLoaded', () => {
  // Solo inicializar si no es un dispositivo móvil para mejor performance
  if (window.innerWidth > 768 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    window.orbixEffects = new OrbixCyberEffects();
    
    // Aplicar efectos específicos
    setTimeout(() => {
      // Efecto glitch en títulos principales
      window.orbixEffects.applyToElement('h1', 'glitch');
      
      // Efecto de escaneo en cards importantes
      window.orbixEffects.applyToElement('.hero-content', 'scan');
    }, 2000);
  }
});

// Limpiar al salir de la página
window.addEventListener('beforeunload', () => {
  if (window.orbixEffects) {
    window.orbixEffects.destroy();
  }
});

// Exportar para uso manual
if (typeof module !== 'undefined' && module.exports) {
  module.exports = OrbixCyberEffects;
}
