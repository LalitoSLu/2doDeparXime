const API_URL = 'http://localhost:5000/api';

// --- TOAST NOTIFICATION SYSTEM ---
function showToast(message, type = 'normal') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type === 'purple' ? 'toast-purple' : ''}`;
    
    let icon = 'fa-info-circle';
    if(type === 'purple') icon = 'fa-brain';
    else if(type === 'success') icon = 'fa-check-circle';
    
    toast.innerHTML = `<i class="fa-solid ${icon} toast-icon"></i> ${message}`;
    container.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

document.addEventListener('DOMContentLoaded', async () => {
    setupNavigation();
    setupThemeToggle();
    await initFilters();
    loadDashboardData();
    loadMetricsData();
});

function setupNavigation() {
    // Left Sidebar Tabs
    const sideBtns = document.querySelectorAll('.sidebar-btn');
    const tabPanes = document.querySelectorAll('.tab-content');
    
    sideBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if(!btn.dataset.tab) return;
            
            sideBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            tabPanes.forEach(p => p.classList.remove('active'));
            document.getElementById(btn.dataset.tab).classList.add('active');
            
            window.dispatchEvent(new Event('resize'));
            
            if (btn.dataset.tab === 'tab-map' && !document.getElementById('mexico-map').hasChildNodes()) {
                loadMapData('Todos');
            }
        });
    });

    // Map Play Button
    const btnMapPlay = document.getElementById('btn-map-play');
    if(btnMapPlay) {
        btnMapPlay.addEventListener('click', async () => {
            const anios = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026'];
            btnMapPlay.disabled = true;
            for(let i=0; i<anios.length; i++) {
                document.querySelector('.breadcrumb').innerHTML = `Evolución Espacial > <strong>Año ${anios[i]}</strong>`;
                await loadMapData(anios[i]);
                await new Promise(r => setTimeout(r, 1500)); // 1.5 second delay per frame
            }
            document.querySelector('.breadcrumb').innerHTML = `Análisis Predictivo > <strong>Riesgo Respiratorio MX</strong>`;
            btnMapPlay.disabled = false;
        });
    }

    // Filters & Actions
    document.getElementById('state-filter').addEventListener('change', (e) => {
        showToast(`Cargando datos históricos de ${e.target.value}...`, 'normal');
        loadDashboardData();
    });
    document.getElementById('year-filter').addEventListener('change', loadDashboardData);
    
    document.getElementById('model-filter').addEventListener('change', (e) => {
        const modelName = e.target.options[e.target.selectedIndex].text;
        showToast(`Motor de predicción cambiado a: ${modelName}. Reevaluando...`, 'purple');
        loadMetricsData();
    });
    
    const btnExport = document.getElementById('btn-export');
    if(btnExport) {
        btnExport.addEventListener('click', () => {
            window.open(`${API_URL}/download-dataset`, '_blank');
        });
    }

    // Simulator Logic
    const btnPredict = document.getElementById('btn-predict');
    if(btnPredict) btnPredict.addEventListener('click', runPrediction);
    
    const btnPdf = document.getElementById('btn-pdf');
    if(btnPdf) {
        btnPdf.addEventListener('click', () => {
            const element = document.getElementById('pdf-content-area');
            const opt = {
                margin:       0.5,
                filename:     'Reporte_Clinico_Riesgo.pdf',
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, backgroundColor: '#2c3e50' },
                jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
            };
            showToast('Generando PDF oficial...', 'success');
            html2pdf().set(opt).from(element).save();
        });
    }
    
    // Sliders dynamic value update
    const sliders = ['temp', 'prec', 'hum', 'pm25', 'pm10', 'o3', 'vuln'];
    sliders.forEach(s => {
        const input = document.getElementById(`sim-${s}`);
        const display = document.getElementById(`val-${s}`);
        if(input && display) {
            input.addEventListener('input', e => display.innerText = e.target.value);
        }
    });

    // Simulador: Preset de Estado
    const simPreset = document.getElementById('sim-state-preset');
    simPreset.addEventListener('change', async (e) => {
        const estado = e.target.value;
        const res = await fetch(`${API_URL}/state-averages?estado=${estado}`);
        if(res.ok) {
            const data = await res.json();
            document.getElementById('sim-temp').value = data.Temperatura;
            document.getElementById('val-temp').innerText = data.Temperatura.toFixed(1);
            
            document.getElementById('sim-prec').value = data.Precipitacion;
            document.getElementById('val-prec').innerText = data.Precipitacion.toFixed(1);
            
            document.getElementById('sim-hum').value = data.Humedad;
            document.getElementById('val-hum').innerText = data.Humedad.toFixed(1);
            
            document.getElementById('sim-pm25').value = data.PM25;
            document.getElementById('val-pm25').innerText = data.PM25.toFixed(1);
            
            document.getElementById('sim-pm10').value = data.PM10;
            document.getElementById('val-pm10').innerText = data.PM10.toFixed(1);
            
            document.getElementById('sim-o3').value = data.O3;
            document.getElementById('val-o3').innerText = data.O3.toFixed(3);
            
            document.getElementById('sim-vuln').value = data.Poblacion_Vulnerable_Pct;
            document.getElementById('val-vuln').innerText = data.Poblacion_Vulnerable_Pct.toFixed(1);
            
            document.getElementById('sim-dens').value = Math.round(data.Densidad_Poblacional);
            
            // Guardar rezagos ocultos
            window.simContext = {
                Casos_Rezago_1: data.Casos_Respiratorios,
                NO2: data.NO2,
                SO2: data.SO2,
                CO: data.CO
            };
        }
    });
}

// --- THEME TOGGLE LOGIC ---
function setupThemeToggle() {
    const btn = document.getElementById('btn-theme-toggle');
    if(!btn) return;
    btn.addEventListener('click', () => {
        const body = document.documentElement;
        if(body.getAttribute('data-theme') === 'clinical') {
            body.removeAttribute('data-theme');
            showToast('Tema cambiado a Ambiental (Terracota)', 'normal');
        } else {
            body.setAttribute('data-theme', 'clinical');
            showToast('Tema cambiado a Clínico (Azul Neón)', 'normal');
        }
    });
}

async function initFilters() {
    try {
        const res = await fetch(`${API_URL}/metadata`);
        const data = await res.json();
        
        const stateSelect = document.getElementById('state-filter');
        const simPreset = document.getElementById('sim-state-preset');
        
        data.estados.forEach(est => {
            const opt = document.createElement('option');
            opt.value = est;
            opt.innerText = est;
            stateSelect.appendChild(opt);
            
            const optSim = document.createElement('option');
            optSim.value = est;
            optSim.innerText = est;
            simPreset.appendChild(optSim);
        });
        
        // Seleccionar CDMX por defecto en simulador
        simPreset.value = "CDMX";
        simPreset.dispatchEvent(new Event('change'));
        
        const yearSelect = document.getElementById('year-filter');
        data.anios.forEach(anio => {
            const opt = document.createElement('option');
            opt.value = anio;
            opt.innerText = `Años: ${anio}`;
            yearSelect.appendChild(opt);
        });
    } catch(e) { console.error(e); }
}

const layoutConfig = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#fff' },
    margin: { t: 10, r: 10, l: 30, b: 20 },
    xaxis: { showgrid: false, zeroline: false, color: '#e0e0e0' },
    yaxis: { showgrid: true, gridcolor: 'rgba(255,255,255,0.1)', zeroline: false, color: '#e0e0e0' }
};

async function loadDashboardData() {
    const estado = document.getElementById('state-filter').value;
    const anio = document.getElementById('year-filter').value;
    const query = `?estado=${estado}&anio=${anio}`;
    
    try {
        // 1. KPIs
        const kpiRes = await fetch(`${API_URL}/kpis${query}`);
        if(kpiRes.ok) {
            const kpi = await kpiRes.json();
            document.getElementById('kpi-rate').innerHTML = `${kpi.tasa_100k} <span class="kpi-unit">casos/100k</span>`;
            document.getElementById('kpi-pm25').innerHTML = `${kpi.prom_pm25} <span class="kpi-unit">µg/m³</span>`;
            document.getElementById('kpi-cases').innerHTML = `${kpi.total_casos.toLocaleString()} <span class="kpi-unit">casos</span>`;
            document.getElementById('kpi-max-state').innerText = kpi.estado_max_tasa;
        }

        // 2. Evolución (Center Area Chart) + FORECAST
        const timeRes = await fetch(`${API_URL}/time-series${query}`);
        if(timeRes.ok) {
            const tData = await timeRes.json();
            
            // Generate a simple forecast for the next 3 months based on the last 6 months trend
            const last6 = tData.casos_100k.slice(-6);
            const trend = (last6[last6.length-1] - last6[0]) / 6;
            const lastDate = new Date(tData.fechas[tData.fechas.length-1]);
            const forecastDates = [];
            const forecastVals = [];
            
            for(let i=1; i<=3; i++) {
                const nd = new Date(lastDate);
                nd.setMonth(nd.getMonth() + i);
                forecastDates.push(nd.toISOString().split('T')[0]);
                forecastVals.push(Math.max(0, last6[last6.length-1] + (trend * i)));
            }

            const traceHist = {
                x: tData.fechas,
                y: tData.casos_100k,
                name: 'Histórico',
                type: 'scatter',
                fill: 'tozeroy',
                mode: 'lines+markers',
                line: { color: '#f39c12', width: 2 },
                marker: { size: 4, color: '#fff' },
                fillcolor: 'rgba(243, 156, 18, 0.2)'
            };
            
            const traceForecast = {
                x: [tData.fechas[tData.fechas.length-1], ...forecastDates],
                y: [tData.casos_100k[tData.casos_100k.length-1], ...forecastVals],
                name: 'Proyección IA (3 meses)',
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#e74c3c', width: 2, dash: 'dot' },
                marker: { size: 6, color: '#e74c3c' }
            };

            Plotly.newPlot('chart-evolution', [traceHist, traceForecast], { ...layoutConfig, showlegend: true, legend: {x:0, y:1} }, {responsive:true, displayModeBar: false});
        }

        // 3. Distribución (Right Horizontal Bar Chart)
        const pollRes = await fetch(`${API_URL}/pollutants${query}`);
        if(pollRes.ok) {
            const pData = await pollRes.json();
            const colors = ['#1abc9c', '#f39c12', '#e74c3c', '#9b59b6', '#2ecc71', '#34495e', '#f1c40f', '#e67e22'];
            const trace = {
                y: pData.estados,
                x: pData.pm25,
                type: 'bar',
                orientation: 'h',
                marker: { color: colors.slice(0, pData.estados.length) }
            };
            const layoutRight = { ...layoutConfig, yaxis: { ...layoutConfig.yaxis, autorange: 'reversed', showgrid: false }, margin: { t: 0, r: 0, l: 80, b: 20 } };
            Plotly.newPlot('chart-distribution', [trace], layoutRight, {responsive:true, displayModeBar: false});
        }

        // 4. Correlación 
        const corrRes = await fetch(`${API_URL}/correlation${query}`);
        if(corrRes.ok) {
            const cData = await corrRes.json();
            const traceCorr = {
                z: cData.values,
                x: cData.columns.map(c => c.substring(0,6)),
                y: cData.columns.map(c => c.substring(0,6)),
                type: 'heatmap',
                colorscale: 'RdBu',
                zmin: -1, zmax: 1,
                showscale: false
            };
            Plotly.newPlot('correlation-chart', [traceCorr], { ...layoutConfig, margin:{t:10,b:30,l:40,r:10} }, {responsive:true, displayModeBar: false});
        }

        // 5. Static Gauge (Bottom Middle)
        const gaugeTrace = {
            type: "indicator",
            mode: "gauge+number",
            value: document.getElementById('kpi-rate').innerText.split(' ')[0], // Dynamic based on current rate
            title: { text: "Tasa 100k", font: { color: "#fff", size: 12 } },
            number: { font: { color: "#fff", size: 24 } },
            gauge: {
                axis: { range: [null, 600], tickwidth: 1, tickcolor: "#fff" },
                bar: { color: "#2ecc71" },
                bgcolor: "rgba(0,0,0,0.5)",
                borderwidth: 0,
                steps: [
                    { range: [0, 200], color: "rgba(46, 204, 113, 0.3)" },
                    { range: [200, 400], color: "rgba(243, 156, 18, 0.3)" },
                    { range: [400, 600], color: "rgba(231, 76, 60, 0.3)" }
                ]
            }
        };
        Plotly.newPlot('chart-gauge-static', [gaugeTrace], { paper_bgcolor: 'rgba(0,0,0,0)', margin: { t: 25, r: 15, l: 15, b: 15 } }, {responsive:true, displayModeBar: false});

    } catch(e) { console.error(e); }
}

async function loadMapData(forceYear = null) {
    const anio = forceYear || document.getElementById('year-filter').value;
    const res = await fetch(`${API_URL}/map-data?anio=${anio}`);
    const data = await res.json();
    const geoRes = await fetch('https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json');
    const geojson = await geoRes.json();
    
    const trace = {
        type: "choroplethmapbox",
        geojson: geojson,
        locations: data.estados,
        z: data.riesgo_alto,
        featureidkey: "properties.name",
        colorscale: "YlOrRd",
        zmin: 0,
        zmax: 1,
        colorbar: { title: 'Nivel Riesgo', tickfont: {color: 'white'} },
        hovertemplate: '<b>%{location}</b><br>Riesgo Promedio: %{z:.2f}<br><extra></extra>'
    };
    
    const layout = {
        mapbox: { style: "carto-darkmatter", center: { lon: -102.5528, lat: 23.6345 }, zoom: 4.5 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: { t: 0, r: 0, l: 0, b: 0 }
    };
    Plotly.newPlot('mexico-map', [trace], layout, {responsive:true});
}

async function runPrediction() {
    const modelKey = document.getElementById('model-filter').value;
    const temp = parseFloat(document.getElementById('sim-temp').value);
    const prec = parseFloat(document.getElementById('sim-prec').value);
    const hum = parseFloat(document.getElementById('sim-hum').value);
    const pm25 = parseFloat(document.getElementById('sim-pm25').value);
    const pm10 = parseFloat(document.getElementById('sim-pm10').value);
    const o3 = parseFloat(document.getElementById('sim-o3').value);
    const vuln = parseFloat(document.getElementById('sim-vuln').value);
    const dens = parseFloat(document.getElementById('sim-dens').value);
    
    const ctx = window.simContext || {};
    
    const payload = {
        modelo: modelKey,
        features: {
            Temperatura: temp,
            Precipitacion: prec,
            Humedad: hum,
            PM25: pm25,
            PM10: pm10,
            O3: o3,
            NO2: ctx.NO2 || 0.02,
            SO2: ctx.SO2 || 0.01,
            CO: ctx.CO || 1.0,
            Densidad_Poblacional: dens,
            Poblacion_Vulnerable_Pct: vuln,
            PM25_Movil_3: pm25,
            PM10_Movil_3: pm10,
            Temp_Rezago_1: temp,
            Precip_Rezago_1: prec,
            Casos_Rezago_1: ctx.Casos_Rezago_1 || 100
        }
    };
    
    const res = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    
    if(res.ok) {
        const data = await res.json();
        
        // Insights dinámicos
        let insightTemp = temp < 10 ? "Bajas temperaturas elevando vulnerabilidad." : "Clima no crítico.";
        let insightPM = pm25 > 25 ? `PM2.5 Crítico (${pm25} µg/m³).` : "Calidad aire segura.";
        let insightVuln = vuln > 15 ? `Demografía vulnerable alta (${vuln}%).` : "Demografía estable.";

        // Mostrar botón de PDF
        document.getElementById('btn-pdf').style.display = 'block';

        const box = document.getElementById('prediction-box');
        box.innerHTML = `
            <div style="border-left: 5px solid ${data.prediccion === 1 ? '#e74c3c' : '#2ecc71'}; padding-left: 15px;">
                <h3 style="color: ${data.prediccion === 1 ? '#e74c3c' : '#2ecc71'}; font-size: 20px; margin-bottom: 10px;">
                    ${data.prediccion === 1 ? '🔴 RIESGO ALTO DE EPIDEMIA' : '🟢 RIESGO BAJO / MODERADO'}
                </h3>
                <p style="margin-bottom: 15px;"><strong>Análisis de IA:</strong> ${data.prediccion === 1 ? 'Condiciones críticas detectadas. Se estima un incremento severo en atenciones.' : 'Factores estables. No se prevén brotes significativos.'}</p>
                <ul style="color: #ccc; margin-left: 20px;">
                    <li>${insightTemp}</li>
                    <li>${insightPM}</li>
                    <li>${insightVuln}</li>
                </ul>
            </div>
        `;
        
        // Gauge Dinámico
        const traceGauge = {
            type: "indicator",
            mode: "gauge+number",
            value: data.probabilidad * 100,
            title: { text: "Probabilidad (%)", font: { color: "white" } },
            number: { font: { color: "white" } },
            gauge: {
                axis: { range: [null, 100], tickcolor: "white" },
                bar: { color: data.prediccion === 1 ? '#e74c3c' : '#2ecc71' },
                bgcolor: "rgba(0,0,0,0.5)",
                borderwidth: 0,
                steps: [
                    { range: [0, 50], color: "rgba(46, 204, 113, 0.2)" },
                    { range: [50, 80], color: "rgba(243, 156, 18, 0.2)" },
                    { range: [80, 100], color: "rgba(231, 76, 60, 0.3)" }
                ]
            }
        };
        Plotly.newPlot('gauge-chart', [traceGauge], { paper_bgcolor: 'rgba(0,0,0,0)', font: {color: 'white'}, margin: { t: 25, r: 25, l: 25, b: 25 } }, {responsive: true});

        // Gráfico de Radar (Telaraña)
        // Comparación de inputs vs "Promedio Nacional Normalizado"
        const traceRadar = {
            type: 'scatterpolar',
            r: [pm25, pm10, o3*1000, vuln, temp], // Scaling O3 to be visible on radar
            theta: ['PM2.5', 'PM10', 'O3 (x1000)', 'Vulnerabilidad %', 'Temperatura °C'],
            fill: 'toself',
            name: 'Región Actual',
            marker: { color: '#9b59b6' }
        };
        
        const traceRadarRef = {
            type: 'scatterpolar',
            r: [15, 30, 30, 12, 22], // Safe national baseline
            theta: ['PM2.5', 'PM10', 'O3 (x1000)', 'Vulnerabilidad %', 'Temperatura °C'],
            fill: 'toself',
            name: 'Umbral Seguro',
            marker: { color: 'rgba(46, 204, 113, 0.5)' }
        };

        const layoutRadar = {
            polar: {
                radialaxis: { visible: true, range: [0, 100], color: 'rgba(255,255,255,0.5)' },
                angularaxis: { color: '#fff' },
                bgcolor: 'rgba(0,0,0,0)'
            },
            showlegend: true,
            legend: { x: 0, y: -0.2, orientation: 'h' },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: '#fff' },
            margin: { t: 20, r: 20, l: 20, b: 20 }
        };
        Plotly.newPlot('radar-chart', [traceRadar, traceRadarRef], layoutRadar, {responsive: true});
        
        showToast('Predicción completada con éxito. Listo para exportar.', 'purple');
    }
}

async function loadMetricsData() {
    try {
        const res = await fetch(`${API_URL}/model-metrics`);
        if(!res.ok) return;
        const metrics = await res.json();
        
        // 1. Comparison Bar Chart
        const models = Object.keys(metrics);
        const f1Scores = models.map(m => metrics[m].f1_score);
        const aucScores = models.map(m => metrics[m].auc_roc);
        const accScores = models.map(m => metrics[m].accuracy);
        
        const labels = models.map(m => m.replace(/_/g, ' '));
        
        const traceF1 = { x: labels, y: f1Scores, name: 'Puntuación F1', type: 'bar', marker: {color: '#f39c12'} };
        const traceAUC = { x: labels, y: aucScores, name: 'AUC-ROC', type: 'bar', marker: {color: '#9b59b6'} };
        const traceAcc = { x: labels, y: accScores, name: 'Exactitud', type: 'bar', marker: {color: '#2ecc71'} };
        
        Plotly.newPlot('metrics-bar-chart', [traceAcc, traceF1, traceAUC], { ...layoutConfig, title: 'Comparación Global de Métricas', barmode: 'group', yaxis: { range: [0.8, 1.0], gridcolor: 'rgba(255,255,255,0.1)' } }, {responsive: true});
        
        // Render selected model specifics
        const selectedModel = document.getElementById('model-filter').value || 'Regresion_Logistica';
        const selData = metrics[selectedModel];
        
        if(!selData) return;

        // 2. Confusion Matrix Heatmap
        const cm = selData.confusion_matrix;
        const traceCM = {
            z: cm.reverse(), 
            x: ['Riesgo Bajo', 'Riesgo Alto'],
            y: ['Riesgo Alto', 'Riesgo Bajo'],
            type: 'heatmap',
            colorscale: 'YlOrRd',
            showscale: false
        };
        Plotly.newPlot('confusion-matrix-chart', [traceCM], { ...layoutConfig, margin:{t:20,l:80,r:20,b:40} }, {responsive: true});
        
        // 3. ROC Curve
        const roc = selData.roc_curve;
        const traceROC = {
            x: roc.fpr, y: roc.tpr,
            name: 'Curva ROC',
            type: 'scatter',
            mode: 'lines',
            line: {color: '#f39c12', width: 3}
        };
        const traceDiag = {
            x: [0, 1], y: [0, 1],
            type: 'scatter',
            mode: 'lines',
            line: {color: '#fff', dash: 'dash'}
        };
        Plotly.newPlot('roc-chart', [traceROC, traceDiag], { ...layoutConfig, showlegend:false, margin:{t:20,l:40,r:20,b:40} }, {responsive: true});
        
        // 4. Feature Importance (Only for RF/XGBoost)
        if (selData.feature_importances && Object.keys(selData.feature_importances).length > 0) {
            const fi = selData.feature_importances;
            // Get top 10 features, sort ascending for horizontal bar chart
            const entries = Object.entries(fi).slice(0, 10).reverse();
            const fNames = entries.map(e => e[0].replace(/_/g, ' '));
            const fVals = entries.map(e => e[1]);
            
            const traceFI = {
                y: fNames,
                x: fVals,
                type: 'bar',
                orientation: 'h',
                marker: { color: '#e74c3c' }
            };
            Plotly.newPlot('feature-importance-chart', [traceFI], { ...layoutConfig, margin:{t:20,l:180,r:20,b:40} }, {responsive: true});
        } else {
            document.getElementById('feature-importance-chart').innerHTML = '<div style="padding: 20px; color: #aaa; text-align: center; margin-top: 50px;">El modelo seleccionado no provee<br>pesos de variables directos<br>(ej. Red Neuronal).</div>';
        }
        
    } catch(e) {
        console.error("Error loading metrics", e);
    }
}
