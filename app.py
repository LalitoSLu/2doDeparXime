from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import joblib
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# 1. Cargar datos en memoria al iniciar el servidor
try:
    df = pd.read_csv("datos_enfermedades_respiratorias.csv")
    
    # Mapeo de estados para el GeoJSON (para asegurar que coincidan en el frontend)
    geojson_mapping = {
        "CDMX": "Ciudad de México",
        "Edomex": "México",
        "Michoacán": "Michoacán",
        "Nuevo León": "Nuevo León",
        "Querétaro": "Querétaro",
        "San Luis Potosí": "San Luis Potosí",
        "Yucatán": "Yucatán"
    }
    df['Estado_Map'] = df['Estado'].map(lambda x: geojson_mapping.get(x, x))
    
    # Cargar métricas
    with open("model_evaluation_metrics.json", "r", encoding="utf-8") as f:
        metrics = json.load(f)
        
    print("Datos y métricas cargados exitosamente.")
except Exception as e:
    print(f"Error al cargar datos iniciales: {e}")
    df = pd.DataFrame()
    metrics = {}

# Cargar modelos y scaler en memoria
try:
    models = {
        "regresion_logistica": joblib.load("modelo_regresion_logistica.joblib"),
        "random_forest": joblib.load("modelo_random_forest.joblib"),
        "xgboost": joblib.load("modelo_xgboost.joblib"),
        "red_neuronal_simple": joblib.load("modelo_red_neuronal_simple.joblib")
    }
    scaler = joblib.load("scaler.joblib")
    print("Modelos y scaler cargados exitosamente en memoria.")
except Exception as e:
    print(f"Error al cargar modelos: {e}")
    models = {}
    scaler = None


# 2. Funciones auxiliares
def get_filtered_df(estado, anio):
    df_filtered = df.copy()
    if estado and estado != "Nacional":
        df_filtered = df_filtered[df_filtered["Estado"] == estado]
    if anio and anio != "Todos":
        df_filtered = df_filtered[df_filtered["Año"] == int(anio)]
    return df_filtered

# 3. Rutas de la API

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """Devuelve las listas de estados y años disponibles para los filtros del frontend."""
    estados = sorted(df["Estado"].unique().tolist()) if not df.empty else []
    anios = sorted(df["Año"].unique().tolist()) if not df.empty else []
    return jsonify({
        "estados": estados,
        "anios": [str(a) for a in anios]
    })

@app.route('/api/kpis', methods=['GET'])
def get_kpis():
    estado = request.args.get('estado', 'Nacional')
    anio = request.args.get('anio', 'Todos')
    
    df_filtered = get_filtered_df(estado, anio)
    if df_filtered.empty:
        return jsonify({"error": "No data"}), 404
        
    total_casos = int(df_filtered["Casos_Respiratorios"].sum())
    
    # Tasa acumulada
    if estado == "Nacional":
        total_poblacion_promedio = df_filtered.groupby("Estado")["Poblacion"].mean().sum()
    else:
        total_poblacion_promedio = df_filtered["Poblacion"].mean()
        
    tasa_100k = (total_casos / total_poblacion_promedio) * 100000.0 if total_poblacion_promedio > 0 else 0
    
    estado_max_tasa = df_filtered.groupby("Estado")["Casos_Por_100k"].mean().idxmax()
    max_tasa_val = float(df_filtered.groupby("Estado")["Casos_Por_100k"].mean().max())
    prom_pm25 = float(df_filtered["PM25"].mean())
    
    return jsonify({
        "total_casos": total_casos,
        "tasa_100k": round(tasa_100k, 2),
        "estado_max_tasa": estado_max_tasa,
        "max_tasa_val": round(max_tasa_val, 1),
        "prom_pm25": round(prom_pm25, 2)
    })

@app.route('/api/time-series', methods=['GET'])
def get_time_series():
    estado = request.args.get('estado', 'Nacional')
    anio = request.args.get('anio', 'Todos')
    df_filtered = get_filtered_df(estado, anio)
    
    df_time = df_filtered.groupby("Fecha")[["Casos_Por_100k", "PM25"]].mean().reset_index()
    df_time = df_time.sort_values("Fecha")
    
    return jsonify({
        "fechas": df_time["Fecha"].tolist(),
        "casos_100k": df_time["Casos_Por_100k"].round(2).tolist(),
        "pm25": df_time["PM25"].round(2).tolist()
    })

@app.route('/api/pollutants', methods=['GET'])
def get_pollutants():
    estado = request.args.get('estado', 'Nacional')
    anio = request.args.get('anio', 'Todos')
    df_filtered = get_filtered_df(estado, anio)
    
    df_poll = df_filtered.groupby("Estado")[["PM25", "PM10"]].mean().reset_index()
    df_poll = df_poll.sort_values("PM25", ascending=False).head(8)
    
    return jsonify({
        "estados": df_poll["Estado"].tolist(),
        "pm25": df_poll["PM25"].round(2).tolist(),
        "pm10": df_poll["PM10"].round(2).tolist()
    })

@app.route('/api/map-data', methods=['GET'])
def get_map_data():
    anio = request.args.get('anio', 'Todos')
    df_filtered = get_filtered_df("Nacional", anio)
    
    df_map = df_filtered.groupby("Estado_Map")[["Casos_Por_100k", "PM25", "Temperatura", "Riesgo_Alto"]].mean().reset_index()
    
    return jsonify({
        "estados": df_map["Estado_Map"].tolist(),
        "casos_100k": df_map["Casos_Por_100k"].round(2).tolist(),
        "riesgo_alto": df_map["Riesgo_Alto"].round(2).tolist()
    })

@app.route('/api/scatter-data', methods=['GET'])
def get_scatter_data():
    estado = request.args.get('estado', 'Nacional')
    anio = request.args.get('anio', 'Todos')
    df_filtered = get_filtered_df(estado, anio)
    
    # Tomar una muestra si hay muchos datos para no sobrecargar el navegador
    if len(df_filtered) > 1000:
        df_filtered = df_filtered.sample(1000, random_state=42)
        
    return jsonify({
        "temperatura": df_filtered["Temperatura"].tolist(),
        "casos_100k": df_filtered["Casos_Por_100k"].tolist(),
        "riesgo": df_filtered["Riesgo_Alto"].tolist()
    })

@app.route('/api/state-averages', methods=['GET'])
def get_state_averages():
    estado = request.args.get('estado', 'CDMX')
    df_filtered = df[df["Estado"] == estado]
    if df_filtered.empty:
        return jsonify({"error": "State not found"}), 404
        
    avg = df_filtered.mean(numeric_only=True)
    return jsonify({
        "Temperatura": float(avg["Temperatura"]),
        "Precipitacion": float(avg["Precipitacion"]),
        "Humedad": float(avg["Humedad"]),
        "PM25": float(avg["PM25"]),
        "PM10": float(avg["PM10"]),
        "O3": float(avg["O3"]),
        "NO2": float(avg["NO2"]),
        "SO2": float(avg["SO2"]),
        "CO": float(avg["CO"]),
        "Densidad_Poblacional": float(avg["Densidad_Poblacional"]),
        "Poblacion_Vulnerable_Pct": float(avg["Poblacion_Vulnerable_Pct"]),
        "Casos_Respiratorios": float(avg["Casos_Respiratorios"])
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    modelo_key = data.get("modelo", "Regresion_Logistica").lower()
    features = data.get("features", {})
    
    try:
        clf = models.get(modelo_key)
        if clf is None:
            return jsonify({"error": f"Modelo {modelo_key} no encontrado en memoria."}), 400
        if scaler is None:
            return jsonify({"error": "Scaler no cargado en memoria."}), 500
        

        # Orden exacto de características esperado por el modelo:
        feature_order = [
            "Temperatura", "Precipitacion", "Humedad", "PM25", "PM10", "O3", "NO2", "SO2", "CO",
            "Densidad_Poblacional", "Poblacion_Vulnerable_Pct", "PM25_Movil_3", "PM10_Movil_3",
            "Temp_Rezago_1", "Precip_Rezago_1", "Casos_Rezago_1"
        ]
        
        input_list = []
        for col in feature_order:
            input_list.append(float(features.get(col, 0.0)))
            
        input_data = pd.DataFrame([input_list], columns=feature_order)
        input_scaled = scaler.transform(input_data)
        input_scaled_df = pd.DataFrame(input_scaled, columns=feature_order)
        
        pred = int(clf.predict(input_scaled_df)[0])
        prob = float(clf.predict_proba(input_scaled_df)[0][1])
        
        return jsonify({
            "prediccion": pred,
            "probabilidad": prob
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/correlation', methods=['GET'])
def get_correlation():
    estado = request.args.get('estado', 'Nacional')
    anio = request.args.get('anio', 'Todos')
    df_filtered = get_filtered_df(estado, anio)
    
    corr_cols = ["Casos_Por_100k", "Temperatura", "Precipitacion", "Humedad", "PM25", "PM10", "O3", "CO", "Densidad_Poblacional"]
    corr_matrix = df_filtered[corr_cols].corr().fillna(0).round(2)
    
    return jsonify({
        "columns": corr_cols,
        "values": corr_matrix.values.tolist()
    })

@app.route('/api/model-metrics', methods=['GET'])
def get_model_metrics():
    return jsonify(metrics)

@app.route('/api/download-dataset', methods=['GET'])
def download_dataset():
    # Return the CSV file as an attachment
    return send_from_directory(os.getcwd(), 'datos_enfermedades_respiratorias.csv', as_attachment=True)

@app.route('/api/raw-data', methods=['GET'])
def get_raw_data():
    try:
        df = pd.read_csv('datos_enfermedades_respiratorias.csv')
        # Limitar a las primeras 500 filas por eficiencia en el frontend
        sample_df = df[['Fecha', 'Estado', 'Temperatura', 'PM25', 'Poblacion', 'Casos_Respiratorios', 'Riesgo_Epidemiologico']].head(500)
        
        # Formatear números para display
        sample_df['Temperatura'] = sample_df['Temperatura'].round(1).astype(str) + ' °C'
        sample_df['PM25'] = sample_df['PM25'].round(2).astype(str) + ' µg/m³'
        sample_df['Poblacion'] = sample_df['Poblacion'].apply(lambda x: f"{int(x):,}")
        sample_df['Casos_Respiratorios'] = sample_df['Casos_Respiratorios'].apply(lambda x: f"{int(x):,}")
        
        # Mapear riesgo a texto
        sample_df['Riesgo_Epidemiologico'] = sample_df['Riesgo_Epidemiologico'].map({0: 'Bajo', 1: 'Alto'})
        
        return jsonify(sample_df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Asegurarnos de que el puerto sea el 5000 (Flask standard)
    app.run(host='0.0.0.0', port=5000, debug=True)