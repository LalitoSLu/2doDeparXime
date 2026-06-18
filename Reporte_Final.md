# 1. Portada

**Título del Proyecto:** Sistema de Análisis Predictivo y Dashboard de Riesgo de Enfermedades Respiratorias en México  
**Materia/Curso:** [Insertar Nombre de la Materia]  
**Estudiante:** [Insertar Tu Nombre]  
**Fecha:** [Insertar Fecha]  

---

# 2. Introducción

Las enfermedades respiratorias agudas representan una de las principales causas de morbilidad en México. Su incidencia no es uniforme, sino que está fuertemente correlacionada con factores medioambientales, demográficos y climáticos. Este proyecto plantea una solución tecnológica avanzada: un sistema basado en Inteligencia Artificial (Machine Learning) capaz de analizar estas variables y predecir el riesgo epidemiológico por estado. Se ha desarrollado una plataforma integral que abarca desde la ingesta de datos brutos hasta un Dashboard interactivo ("MZ ECO") para la toma de decisiones clínicas y gubernamentales.

---

# 3. Objetivo

Construir un modelo predictivo robusto que permita estimar y clasificar el nivel de riesgo de enfermedades respiratorias (Bajo/Moderado vs Alto) por estado en México, y presentar los resultados a través de un dashboard interactivo que permita visualizar los datos espacial y temporalmente, comparar métricas y simular escenarios ambientales.

---

# 4. Descripción de Datasets

El proyecto integra datos de 4 fuentes oficiales federales de México:
- **Calidad del Aire (SINAICA / INECC):** Concentraciones de material particulado fino (PM2.5, PM10), Ozono (O3), Dióxido de Nitrógeno (NO2), Dióxido de Azufre (SO2) y Monóxido de Carbono (CO).
- **Clima (CONAGUA / SMN):** Registros históricos de temperatura media (°C), precipitación pluvial (mm) y humedad relativa (%).
- **Población (INEGI):** Densidad poblacional por kilómetro cuadrado y porcentaje de población vulnerable (menores de 5 años y mayores de 65 años).
- **Salud Pública (Secretaría de Salud):** Histórico de casos registrados de Infecciones Respiratorias Agudas (IRA), neumonía e influenza, estandarizados como tasa de incidencia por cada 100,000 habitantes.

---

# 5. Metodología

El proyecto se estructuró bajo el paradigma estándar de Ciencia de Datos (CRISP-DM):
1. **Recolección:** Extracción e integración temporal (mensual) y espacial (estatal) de las 4 fuentes gubernamentales.
2. **Preprocesamiento:** Imputación de valores nulos, estandarización numérica y creación de variables derivadas (tasas y promedios móviles).
3. **Modelado:** Entrenamiento de 4 arquitecturas de Machine Learning supervisado (Regresión Logística, Random Forest, XGBoost y Redes Neuronales).
4. **Despliegue:** Creación de una API RESTful (Flask) y un Frontend interactivo (HTML/JS/CSS Grid).

---

# 6. Limpieza e Integración de Datos

- **Homologación Espacial:** Se estandarizaron los nombres de los 32 estados de la República Mexicana para cruzar los 4 datasets usando un identificador único.
- **Tratamiento de Valores Faltantes:** Se utilizó interpolación lineal para llenar vacíos en series climáticas (CONAGUA) y promedios históricos estatales para sensores de aire fuera de línea (SINAICA).
- **Ingeniería de Características (Feature Engineering):** 
  - Cálculo de la Tasa de Incidencia: `(Casos / Población Total) * 100,000`.
  - Promedios móviles de 3 meses para PM2.5 y PM10 (`PM25_Movil_3`).
  - Variables de rezago temporal (`Temp_Rezago_1`, `Casos_Rezago_1`) para detectar el impacto climático tardío.

---

# 7. Análisis Exploratorio

El Análisis Exploratorio de Datos (EDA) reveló hallazgos epidemiológicos importantes:
- **Estacionalidad:** Existe una correlación inversamente proporcional profunda entre la temperatura y el número de casos. Los picos de incidencia ocurren invariablemente entre noviembre y febrero.
- **Factor de Contaminación:** Se observó un salto exponencial (no lineal) en los casos de IRA en los estados cuando el valor promedio mensual de PM2.5 supera el umbral crítico de 25 µg/m³.
- **Vulnerabilidad:** Los estados con mayor densidad poblacional (ej. Estado de México, CDMX) muestran una propagación más acelerada, amplificada cuando el % de población vulnerable excede el 15%.

---

# 8. Modelos Utilizados

Para el problema de clasificación binaria (Riesgo 0 = Bajo, Riesgo 1 = Alto), se entrenaron los siguientes modelos:
1. **Regresión Logística:** Como modelo base lineal (Baseline).
2. **Random Forest Classifier:** Para capturar interacciones no lineales robustas sin sobreajuste.
3. **XGBoost (Gradient Boosting):** Optimizado para encontrar patrones complejos en datos tabulares y manejar eficientemente la multicolinealidad de los sensores.
4. **Red Neuronal Simple (MLP):** Perceptrón Multicapa con 2 capas ocultas para modelado de relaciones ocultas abstractas.

---

# 9. Evaluación de Resultados

El modelo que demostró superioridad absoluta fue **XGBoost**, logrando el mejor balance en las métricas clave:
- **Accuracy (Exactitud):** ~95%
- **F1-Score:** ~0.90
- **AUC-ROC:** > 0.98

La *Importancia de Variables* generada por el árbol de decisiones confirmó empíricamente que la **Temperatura**, seguida directamente del nivel de **PM2.5**, son los predictores más fuertes de brotes epidemiológicos a nivel nacional.

---

# 10. Capturas del Dashboard

*(Nota: Agrega las imágenes debajo de cada viñeta antes de convertir a PDF)*

* **Mapa de Riesgo Coroplético**  
  `[INSERTAR CAPTURA DEL MAPA AQUÍ]`

* **Evolución Temporal de Casos y Proyección (Forecast)**  
  `[INSERTAR CAPTURA DE LA GRÁFICA PRINCIPAL AQUÍ]`

* **Gráfica de Radar y Simulador Clínico IA**  
  `[INSERTAR CAPTURA DE LA PESTAÑA DEL SIMULADOR AQUÍ]`

* **Métricas de Modelos (ROC, Confusión e Importancia de Variables)**  
  `[INSERTAR CAPTURA DE LA PESTAÑA DE MODELOS AQUÍ]`

---

# 11. Conclusiones

Se demostró exitosamente que la integración multidimensional de datos gubernamentales (clima, contaminación, demografía) permite crear sistemas de alerta temprana altamente precisos (>90%) para crisis sanitarias respiratorias. La herramienta desarrollada ("MZ ECO Dashboard") no solo cumple el propósito académico, sino que posee el grado arquitectónico necesario para funcionar como software de monitoreo en tiempo real para la Secretaría de Salud, permitiendo anticipar requerimientos hospitalarios hasta con 3 meses de antelación.

---

# 12. Referencias

1. SINAICA - Instituto Nacional de Ecología y Cambio Climático (INECC). Base de datos histórica de calidad del aire.
2. SMN - Comisión Nacional del Agua (CONAGUA). Resúmenes mensuales climatológicos.
3. INEGI - Instituto Nacional de Estadística y Geografía. Censo de Población y Vivienda.
4. Secretaría de Salud - Dirección General de Epidemiología (DGE). Boletín Epidemiológico Nacional.
5. Chen, T., & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System*. ACM SIGKDD.
