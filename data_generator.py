import pandas as pd
import numpy as np
import datetime

# Configuración de reproducibilidad
np.random.seed(42)

# 1. Definición de Estados de México y sus características base (demografía e índices base)
estados_info = {
    "Aguascalientes": {"pop": 1425607, "area": 5618, "vuln_pct": 11.5, "base_temp": 18.5, "base_pm25": 14.2},
    "Baja California": {"pop": 3769020, "area": 71446, "vuln_pct": 10.2, "base_temp": 20.2, "base_pm25": 16.5},
    "Baja California Sur": {"pop": 798447, "area": 73922, "vuln_pct": 9.8, "base_temp": 22.5, "base_pm25": 9.5},
    "Campeche": {"pop": 928363, "area": 57924, "vuln_pct": 12.0, "base_temp": 26.5, "base_pm25": 10.2},
    "Chiapas": {"pop": 5543828, "area": 73289, "vuln_pct": 14.5, "base_temp": 24.5, "base_pm25": 12.1},
    "Chihuahua": {"pop": 3741869, "area": 247455, "vuln_pct": 11.8, "base_temp": 17.0, "base_pm25": 11.0},
    "Coahuila": {"pop": 3146771, "area": 151563, "vuln_pct": 11.0, "base_temp": 21.5, "base_pm25": 13.8},
    "Colima": {"pop": 731391, "area": 5625, "vuln_pct": 12.5, "base_temp": 25.5, "base_pm25": 10.8},
    "CDMX": {"pop": 9209944, "area": 1495, "vuln_pct": 14.2, "base_temp": 16.2, "base_pm25": 24.5},
    "Durango": {"pop": 1832650, "area": 123317, "vuln_pct": 12.0, "base_temp": 17.5, "base_pm25": 11.5},
    "Guanajuato": {"pop": 6166934, "area": 30607, "vuln_pct": 12.2, "base_temp": 19.5, "base_pm25": 18.2},
    "Guerrero": {"pop": 3540685, "area": 63596, "vuln_pct": 13.8, "base_temp": 26.8, "base_pm25": 11.2},
    "Hidalgo": {"pop": 3082841, "area": 20813, "vuln_pct": 13.0, "base_temp": 16.8, "base_pm25": 15.0},
    "Jalisco": {"pop": 8348151, "area": 78588, "vuln_pct": 12.4, "base_temp": 20.8, "base_pm25": 19.0},
    "Edomex": {"pop": 16992418, "area": 22357, "vuln_pct": 11.9, "base_temp": 15.0, "base_pm25": 22.8},
    "Michoacán": {"pop": 4748846, "area": 58599, "vuln_pct": 13.2, "base_temp": 21.0, "base_pm25": 14.5},
    "Morelos": {"pop": 1971520, "area": 4879, "vuln_pct": 13.5, "base_temp": 21.5, "base_pm25": 15.5},
    "Nayarit": {"pop": 1235456, "area": 27815, "vuln_pct": 12.8, "base_temp": 24.8, "base_pm25": 11.0},
    "Nuevo León": {"pop": 5784442, "area": 64156, "vuln_pct": 10.8, "base_temp": 22.0, "base_pm25": 21.5},
    "Oaxaca": {"pop": 4132148, "area": 93757, "vuln_pct": 14.8, "base_temp": 22.0, "base_pm25": 11.8},
    "Puebla": {"pop": 6583278, "area": 34306, "vuln_pct": 12.6, "base_temp": 17.5, "base_pm25": 17.5},
    "Querétaro": {"pop": 2368467, "area": 11684, "vuln_pct": 11.2, "base_temp": 19.0, "base_pm25": 15.8},
    "Quintana Roo": {"pop": 1857985, "area": 44705, "vuln_pct": 9.5, "base_temp": 26.8, "base_pm25": 9.0},
    "San Luis Potosí": {"pop": 2822255, "area": 61137, "vuln_pct": 12.5, "base_temp": 21.0, "base_pm25": 14.8},
    "Sinaloa": {"pop": 3026943, "area": 57365, "vuln_pct": 12.0, "base_temp": 24.5, "base_pm25": 12.5},
    "Sonora": {"pop": 2944840, "area": 179355, "vuln_pct": 11.2, "base_temp": 22.5, "base_pm25": 12.0},
    "Tabasco": {"pop": 2402598, "area": 24731, "vuln_pct": 12.5, "base_temp": 27.0, "base_pm25": 9.8},
    "Tamaulipas": {"pop": 3527735, "area": 80175, "vuln_pct": 11.5, "base_temp": 23.5, "base_pm25": 13.5},
    "Tlaxcala": {"pop": 1342977, "area": 3991, "vuln_pct": 12.2, "base_temp": 15.5, "base_pm25": 16.5},
    "Veracruz": {"pop": 8062579, "area": 71820, "vuln_pct": 13.5, "base_temp": 23.0, "base_pm25": 12.8},
    "Yucatán": {"pop": 2320898, "area": 39524, "vuln_pct": 12.5, "base_temp": 26.2, "base_pm25": 9.2},
    "Zacatecas": {"pop": 1622138, "area": 75284, "vuln_pct": 12.8, "base_temp": 16.0, "base_pm25": 11.2}
}

# 2. Rango Temporal (Mensual, de Enero 2018 a Mayo 2026)
start_date = datetime.date(2018, 1, 1)
end_date = datetime.date(2026, 5, 1)

current = start_date
dates = []
while current <= end_date:
    dates.append(current)
    # Siguiente mes
    if current.month == 12:
        current = datetime.date(current.year + 1, 1, 1)
    else:
        current = datetime.date(current.year, current.month + 1, 1)

print(f"Generando series mensuales para {len(estados_info)} estados a lo largo de {len(dates)} meses...")

# 3. Creación del Dataset
data_rows = []

for date in dates:
    year = date.year
    month = date.month
    
    # Efecto estacional general para clima y enfermedades (1 = Ene, 12 = Dic)
    # Invierno: Diciembre (12), Enero (1), Febrero (2) -> más frío y seco en el centro/norte
    # Lluvias: Junio (6) a Septiembre (9) -> reduce contaminación, aumenta humedad
    cos_season = np.cos(2 * np.pi * (month - 1) / 12)  # max en Ene, min en Jul
    sin_season = np.sin(2 * np.pi * (month - 1) / 12)
    
    for estado, info in estados_info.items():
        pop = info["pop"]
        density = pop / info["area"]
        vuln_pct = info["vuln_pct"]
        
        # --- CLIMA ---
        # Temperatura: fluctuación estacional (colder in winter, hotter in summer)
        # Amplitud térmica mayor en el norte (Chihuahua, Sonora) que en el sur (Campeche)
        temp_amplitude = 12.0 if info["base_temp"] < 20 else 6.0
        if estado in ["Chihuahua", "Sonora", "Coahuila", "Zacatecas"]:
            temp_amplitude = 14.0 # Norte continental
        
        temp = info["base_temp"] - temp_amplitude * cos_season + np.random.normal(0, 1.2)
        
        # Precipitación: Concentrada en verano (Junio-Septiembre)
        rain_base = 80.0 if estado in ["Tabasco", "Veracruz", "Chiapas", "Campeche"] else 30.0
        # Multiplicador estacional invertido de cos_season (más lluvia en verano)
        rain_season_mult = max(0.1, -cos_season * 1.5 + 1.0)
        rain = rain_base * rain_season_mult + np.random.uniform(0, 40)
        if estado in ["Baja California Sur", "Sonora", "Chihuahua"]:
            rain *= 0.25 # Estados muy áridos
            
        # Humedad relativa: Mayor en verano y en zonas costeras
        humidity = 55.0 + 20.0 * (-cos_season) + np.random.normal(0, 5.0)
        if estado in ["Tabasco", "Veracruz", "Quintana Roo", "Yucatán"]:
            humidity = min(100.0, humidity + 15.0)
        elif estado in ["Chihuahua", "Sonora", "Coahuila"]:
            humidity = max(15.0, humidity - 20.0)
        humidity = min(100.0, max(0.0, humidity))

        # --- CALIDAD DEL AIRE ---
        # Contaminantes se elevan en invierno seco (estabilidad atmosférica)
        # y se reducen en la temporada de lluvias (lavado por lluvia)
        pollution_season_mult = 1.0 + 0.4 * cos_season  # mayor en invierno, menor en verano
        
        pm25 = info["base_pm25"] * pollution_season_mult + np.random.normal(0, 2.5)
        pm25 = max(2.0, pm25)
        
        pm10 = pm25 * 1.8 + np.random.normal(0, 5.0)
        pm10 = max(5.0, pm10)
        
        # Ozono: mayor en primavera/verano con calor y radiación solar alta (abril, mayo, junio)
        # Abril es mes 4. cos_season de abril es alrededor de cos(2*pi*3/12) = 0.
        # Creemos un pico de ozono en primavera
        o3_season = np.sin(2 * np.pi * (month - 3) / 12) # pico en Junio, minimo en Diciembre
        o3 = 0.03 + 0.015 * o3_season + np.random.uniform(0, 0.01)
        o3 = max(0.005, o3)
        
        no2 = (pm25 * 0.0015) * (1.0 + 0.2 * cos_season) + np.random.normal(0, 0.002)
        no2 = max(0.001, no2)
        
        so2 = (pm25 * 0.0008) * (1.0 + 0.1 * cos_season) + np.random.normal(0, 0.001)
        so2 = max(0.0005, so2)
        
        co = (pm25 * 0.04) * (1.0 + 0.3 * cos_season) + np.random.normal(0, 0.1)
        co = max(0.1, co)

        # --- CASOS DE ENFERMEDADES RESPIRATORIAS (IRA, Influenza, Neumonía) ---
        # Los casos suben cuando:
        # 1. Hace frío (temp < 18°C)
        # 2. Hay alta contaminación (PM2.5 elevado)
        # 3. Alta densidad poblacional (mayor contagio)
        # 4. Alta proporción de población vulnerable
        
        cold_effect = max(0, (26.0 - temp) * 8.0)
        pollution_effect = (pm25 * 2.5) + (pm10 * 0.8) + (o3 * 150.0)
        density_effect = np.log10(density) * 12.0
        vulnerability_effect = vuln_pct * 4.0
        
        # Tasa base por 100,000 habitantes
        tasa_base = 50.0 + cold_effect + pollution_effect + density_effect + vulnerability_effect
        # Variación anual (tendencia de ligero aumento a lo largo de los años)
        year_trend = (year - 2018) * 4.0
        tasa_total = tasa_base + year_trend + np.random.normal(0, 10.0)
        tasa_total = max(10.0, tasa_total)
        
        casos = int((pop / 100000.0) * tasa_total)

        data_rows.append({
            "Estado": estado,
            "Fecha": f"{year}-{month:02d}-01",
            "Año": year,
            "Mes": month,
            "Temperatura": round(temp, 2),
            "Precipitacion": round(rain, 2),
            "Humedad": round(humidity, 2),
            "PM25": round(pm25, 2),
            "PM10": round(pm10, 2),
            "O3": round(o3, 5),
            "NO2": round(no2, 5),
            "SO2": round(so2, 5),
            "CO": round(co, 3),
            "Poblacion": pop,
            "Densidad_Poblacional": round(density, 2),
            "Poblacion_Vulnerable_Pct": vuln_pct,
            "Casos_Respiratorios": casos
        })

df = pd.DataFrame(data_rows)

# 4. INTRODUCCIÓN DE DATOS FALTANTES INTENCIONALES (Para demostrar limpieza de datos)
# Introduciremos 2% de datos nulos en Temperatura, Precipitación, PM2.5 y PM10
nan_cols = ["Temperatura", "Precipitacion", "PM25", "PM10"]
for col in nan_cols:
    nan_indices = df.sample(frac=0.02, random_state=42).index
    df.loc[nan_indices, col] = np.nan

# Guardar Dataset Crudo
raw_file = "datos_enfermedades_respiratorias_raw.csv"
df.to_csv(raw_file, index=False, encoding="utf-8")
print(f"Archivo de datos crudos guardado en: {raw_file}")

# 5. PREPROCESAMIENTO Y LIMPIEZA DE DATOS (Homologar, Imputar Faltantes y crear variables rezagadas)
print("Ejecutando pipeline de preprocesamiento...")

# A. Tratar datos faltantes (Imputación por el promedio histórico mensual del mismo estado)
# Esto es más preciso que usar la media global.
for col in nan_cols:
    df[col] = df.groupby(["Estado", "Mes"])[col].transform(lambda x: x.fillna(x.mean()))
    # En caso de que queden nulos residuales
    df[col] = df[col].fillna(df[col].mean())

# B. Ingeniería de Características (Feature Engineering)
# - Casos respiratorios por cada 100,000 habitantes
df["Casos_Por_100k"] = (df["Casos_Respiratorios"] / df["Poblacion"]) * 100000.0

# - Promedios móviles de 3 meses para PM2.5 y PM10 (por estado)
df = df.sort_values(by=["Estado", "Fecha"]).reset_index(drop=True)
df["PM25_Movil_3"] = df.groupby("Estado")["PM25"].transform(lambda x: x.rolling(3, min_periods=1).mean())
df["PM10_Movil_3"] = df.groupby("Estado")["PM10"].transform(lambda x: x.rolling(3, min_periods=1).mean())

# - Variables rezagadas (Lagged Variables) de 1 mes (temperatura, precipitación y casos)
df["Temp_Rezago_1"] = df.groupby("Estado")["Temperatura"].shift(1)
df["Precip_Rezago_1"] = df.groupby("Estado")["Precipitacion"].shift(1)
df["Casos_Rezago_1"] = df.groupby("Estado")["Casos_Respiratorios"].shift(1)

# Imputar primeros registros del rezago con el valor del mes actual para no tener NAs
df["Temp_Rezago_1"] = df["Temp_Rezago_1"].fillna(df["Temperatura"])
df["Precip_Rezago_1"] = df["Precip_Rezago_1"].fillna(df["Precipitacion"])
df["Casos_Rezago_1"] = df["Casos_Rezago_1"].fillna(df["Casos_Respiratorios"])

# C. Definición de la Variable Objetivo: riesgo_alto
# Definiremos riesgo alto como 1 si la tasa de casos por 100k está por encima del percentil 75 a nivel nacional
threshold = df["Casos_Por_100k"].quantile(0.75)
df["Riesgo_Alto"] = (df["Casos_Por_100k"] > threshold).astype(int)

# Guardar Dataset Limpio y Preprocesado
clean_file = "datos_enfermedades_respiratorias.csv"
df.to_csv(clean_file, index=False, encoding="utf-8")
print(f"Archivo de datos limpios guardado en: {clean_file}")
print(f"Umbral de Riesgo Alto (percentil 75): {threshold:.2f} casos por 100k hab.")
print(f"Distribución de clases del target: {df['Riesgo_Alto'].value_counts(normalize=True).to_dict()}")
