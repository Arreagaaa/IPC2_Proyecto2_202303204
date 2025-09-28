// Funciones globales para la aplicacion GuateRiegos 2.0

// Utilities
const Utils = {
  // Mostrar notificaciones toast
  showToast: function (message, type = "info") {
    const toastContainer = document.getElementById("toastContainer");
    if (!toastContainer) {
      // Crear contenedor si no existe
      const container = document.createElement("div");
      container.id = "toastContainer";
      container.className = "position-fixed top-0 end-0 p-3";
      container.style.zIndex = "1055";
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-bg-${type} border-0`;
    toast.setAttribute("role", "alert");
    toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

    document.getElementById("toastContainer").appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    // Remover toast despues de 5 segundos
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 5000);
  },

  // Formatear tiempo en formato HH:MM:SS
  formatTime: function (seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, "0")}:${secs
        .toString()
        .padStart(2, "0")}`;
    } else {
      return `${minutes}:${secs.toString().padStart(2, "0")}`;
    }
  },

  // Validar archivo XML
  validateXmlFile: function (file) {
    if (!file) {
      return { valid: false, message: "No se selecciono ningun archivo" };
    }

    if (!file.name.toLowerCase().endsWith(".xml")) {
      return { valid: false, message: "El archivo debe tener extension .xml" };
    }

    if (file.size > 10 * 1024 * 1024) {
      // 10MB
      return {
        valid: false,
        message: "El archivo es demasiado grande (maximo 10MB)",
      };
    }

    return { valid: true, message: "Archivo valido" };
  },

  // Mostrar/ocultar loading spinner
  toggleLoading: function (show, message = "Cargando...") {
    let overlay = document.getElementById("loadingOverlay");

    if (!overlay) {
      overlay = document.createElement("div");
      overlay.id = "loadingOverlay";
      overlay.className = "loading-overlay";
      overlay.innerHTML = `
                <div class="text-center">
                    <div class="spinner-border" role="status" style="width: 3rem; height: 3rem;">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                    <div class="mt-3">
                        <h5 id="loadingMessage">${message}</h5>
                        <p class="text-muted">Por favor espere...</p>
                    </div>
                </div>
            `;
      document.body.appendChild(overlay);
    }

    document.getElementById("loadingMessage").textContent = message;
    overlay.style.display = show ? "flex" : "none";
  },
};

// Manejador de API calls
const API = {
  // Configuracion base
  baseUrl: "",

  // Metodo generico para hacer peticiones
  request: async function (url, options = {}) {
    const defaultOptions = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    const finalOptions = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, finalOptions);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Error en la peticion");
      }

      return data;
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  },

  // Subir archivo
  uploadFile: async function (file, onProgress = null) {
    const formData = new FormData();
    formData.append("file", file);

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();

      if (onProgress) {
        xhr.upload.addEventListener("progress", (e) => {
          if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            onProgress(percentComplete);
          }
        });
      }

      xhr.addEventListener("load", () => {
        if (xhr.status === 200) {
          resolve(JSON.parse(xhr.responseText));
        } else {
          reject(new Error("Error en la subida del archivo"));
        }
      });

      xhr.addEventListener("error", () => {
        reject(new Error("Error de red"));
      });

      xhr.open("POST", "/upload");
      xhr.send(formData);
    });
  },

  // Ejecutar simulacion
  runSimulation: async function (invernadero) {
    return this.request("/run_simulation", {
      method: "POST",
      body: JSON.stringify({ invernadero }),
    });
  },

  // Generar reporte HTML
  generateHtmlReport: async function () {
    return this.request("/generate_html_report", {
      method: "POST",
    });
  },

  // Generar graficos TDA
  generateTdaGraph: async function (tiempo) {
    return this.request("/generate_tda_graph", {
      method: "POST",
      body: JSON.stringify({ tiempo }),
    });
  },
};

// Sistema de estado global
const AppState = {
  invernaderos: [],
  currentSimulation: null,

  setInvernaderos: function (invernaderos) {
    this.invernaderos = invernaderos;
    this.notifyStateChange("invernaderos", invernaderos);
  },

  setCurrentSimulation: function (simulation) {
    this.currentSimulation = simulation;
    this.notifyStateChange("simulation", simulation);
  },

  observers: [],

  subscribe: function (callback) {
    this.observers.push(callback);
  },

  notifyStateChange: function (type, data) {
    this.observers.forEach((callback) => {
      callback(type, data);
    });
  },
};

// Componentes reutilizables
const Components = {
  // Crear card de estadisticas
  createStatsCard: function (title, value, icon, color = "primary") {
    return `
            <div class="stats-card">
                <div class="stats-icon text-${color}">
                    <i class="${icon}"></i>
                </div>
                <div class="stats-number">${value}</div>
                <div class="stats-label">${title}</div>
            </div>
        `;
  },

  // Crear fila de tabla
  createTableRow: function (data) {
    return `
            <tr>
                ${data.map((cell) => `<td>${cell}</td>`).join("")}
            </tr>
        `;
  },

  // Crear alerta
  createAlert: function (message, type = "info") {
    return `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
  },
};

// Inicializacion global
document.addEventListener("DOMContentLoaded", function () {
  // Inicializar tooltips
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Inicializar popovers
  const popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Agregar animaciones a las cards
  const cards = document.querySelectorAll(".card");
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
    card.classList.add("fade-in");
  });

  // Agregar efecto hover a los botones
  const buttons = document.querySelectorAll(".btn:not(.btn-outline-*)");
  buttons.forEach((btn) => {
    btn.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-2px)";
    });

    btn.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });

  console.log("GuateRiegos 2.0 - Sistema inicializado correctamente");
});
