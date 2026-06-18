# Proyecto Final: Análisis Predictivo de Riesgo de Enfermedades Respiratorias en México 🫁

Este proyecto implementa un sistema completo de ciencia de datos, combinando un **generador de datos históricos**, el entrenamiento de **múltiples modelos de aprendizaje automático** (Machine Learning) y la creación de un **Dashboard Interactivo** (Backend Flask + Frontend SPA) para predecir el impacto climático y ambiental en las tasas de incidencia respiratoria en México.

## Características Exclusivas (Funciones WOW) 🌟

Además de cumplir estrictamente con los requerimientos académicos, el proyecto cuenta con características avanzadas de nivel profesional:
* **Generación de Reportes PDF:** El Simulador IA cuenta con un botón para exportar instantáneamente el diagnóstico clínico a un PDF profesional.
* **Proyección Futura (Forecast):** La gráfica temporal inyecta automáticamente una proyección predictiva de 3 meses basada en la tendencia histórica.
* **Animación de Mapa (Time-Lapse):** Un motor de reproducción cronológica que muestra la evolución espacial del riesgo respiratorio año con año (2018-2026).
* **Interruptor de Tema (UI/UX):** Permite cambiar toda la paleta de colores del dashboard de un estilo "Ambiental" (Terracota) a un estilo "Clínico" (Azul Marino/Neón).

---

## Estructura del Repositorio 📂

* `app.py`: Servidor backend (API REST) construido en Flask.
* `data_generator.py`: Script para generar datos sintéticos históricos de las 4 fuentes oficiales (SINAICA, CONAGUA, INEGI, SSa), aplicando limpieza e ingeniería de características.
* `model_trainer.py`: Script de entrenamiento que evalúa y exporta métricas de Regresión Logística, Random Forest, XGBoost y Redes Neuronales (MLP).
* `datos_enfermedades_respiratorias.csv`: Dataset procesado final (10,000+ registros).
* `model_evaluation_metrics.json`: Métricas de evaluación pre-calculadas y pesos de **Importancia de Variables**.
* `*.joblib`: Modelos entrenados y el escalador de variables numéricas.
* `frontend/`: Carpeta de la Interfaz Interactiva Web ("MZ ECO").
  * `index.html`: La Single Page Application (UI Grid).
  * `css/styles.css`: Hojas de estilo dinámicas.
  * `js/app.js`: Lógica de conexión y renderizado de gráficos (Plotly.js y html2pdf).
* `Reporte_Final.md`: Documento de investigación estructurado bajo las 12 secciones exactas de la rúbrica (listo para PDF).

---

## Instalación y Uso 🚀

### Requisitos Previos
* Python 3.10 o superior.

### Instalación de dependencias
Abre una terminal y ejecuta:
```bash
pip install flask flask-cors pandas numpy scikit-learn xgboost joblib
```

### Ejecución del Servidor Dashboard
Para iniciar la plataforma web:
```bash
python app.py
```
A continuación, abre tu navegador web favorito y accede a:
👉 **http://localhost:5000**

---

## Funcionalidades del Dashboard 🛠️

* **Tablero Epidemiológico**: Visualiza los indicadores principales (Casos Totales, Tasas), las gráficas temporales con proyección IA, una comparativa de material particulado y la Matriz de Correlación cruzada.
* **Mapa de Riesgo Nacional**: Mapa interactivo Coroplético de México con función Time-Lapse integrada.
* **Simulador Clínico IA**: Permite modificar clima, densidad y contaminantes mediante sliders, ejecutando la inferencia de la IA en tiempo real para generar diagnósticos visuales y Gráficos de Radar (Telaraña).
* **Evaluación de Modelos**: Presenta la Matriz de Confusión, la gráfica de Importancia de Variables (Feature Importance), la gráfica comparativa de modelos (Accuracy, F1, AUC) y la Curva ROC.
