import pandas as pd
import numpy as np
import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
from xgboost import XGBClassifier

print("Iniciando pipeline de entrenamiento de modelos predictivos...")

# 1. Cargar datos
df = pd.read_csv("datos_enfermedades_respiratorias.csv")

# 2. Definir características (X) y variable objetivo (y)
features = [
    "Temperatura", "Precipitacion", "Humedad",
    "PM25", "PM10", "O3", "NO2", "SO2", "CO",
    "Densidad_Poblacional", "Poblacion_Vulnerable_Pct",
    "PM25_Movil_3", "PM10_Movil_3",
    "Temp_Rezago_1", "Precip_Rezago_1", "Casos_Rezago_1"
]
target = "Riesgo_Alto"

X = df[features]
y = df[target]

print(f"Características utilizadas para el modelado: {features}")
print(f"Tamaño total del dataset: X={X.shape}, y={y.shape}")

# 3. Separar en conjuntos de entrenamiento y prueba (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Tamaño del set de entrenamiento: X_train={X_train.shape}, y_train={y_train.shape}")
print(f"Tamaño del set de prueba: X_test={X_test.shape}, y_test={y_test.shape}")

# 4. Escalar características (StandardScaler)
# Es vital para Regresión Logística y MLP, y no afecta negativamente a los modelos basados en árboles.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Guardar el escalador
joblib.dump(scaler, "scaler.joblib")
print("Escalador guardado en 'scaler.joblib'")

# Convertir a pandas DataFrame de nuevo para mantener consistencia de nombres de columnas en XGBoost
X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=features)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=features)

# 5. Definir modelos
modelos = {
    "Regresion_Logistica": LogisticRegression(max_iter=1000, random_state=42),
    "Random_Forest": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1),
    "XGBoost": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1, eval_metric="logloss"),
    "Red_Neuronal_Simple": MLPClassifier(hidden_layer_sizes=(32, 16), max_iter=500, alpha=0.01, random_state=42)
}

# 6. Estructura para almacenar métricas y datos de evaluación
evaluation_metrics = {}

for nombre_modelo, modelo in modelos.items():
    print(f"Entrenando modelo: {nombre_modelo}...")
    
    # Entrenar
    modelo.fit(X_train_scaled_df, y_train)
    
    # Predecir
    y_pred = modelo.predict(X_test_scaled_df)
    y_prob = modelo.predict_proba(X_test_scaled_df)[:, 1]
    
    # Calcular métricas básicas
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Matriz de Confusión
    cm = confusion_matrix(y_test, y_pred)
    # Convertir a lista nativa de Python para serialización JSON
    cm_list = cm.tolist() 
    
    # Curva ROC y AUC
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    
    # Limitar el número de puntos de la curva ROC para ahorrar espacio en JSON
    # Seleccionamos hasta 50 puntos distribuidos uniformemente
    indices = np.linspace(0, len(fpr) - 1, min(50, len(fpr)), dtype=int)
    fpr_selected = fpr[indices].tolist()
    tpr_selected = tpr[indices].tolist()
    
    print(f"[{nombre_modelo}] Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {roc_auc:.4f}")
    
    # Guardar modelo entrenado
    modelo_filename = f"modelo_{nombre_modelo.lower()}.joblib"
    joblib.dump(modelo, modelo_filename)
    
    # Estructura del JSON para este modelo
    evaluation_metrics[nombre_modelo] = {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "auc_roc": float(roc_auc),
        "confusion_matrix": cm_list,
        "roc_curve": {
            "fpr": fpr_selected,
            "tpr": tpr_selected
        },
        "feature_importances": {}
    }
    
    # Importancia de Variables (si aplica)
    if nombre_modelo == "Random_Forest":
        importances = modelo.feature_importances_
        feature_imp_dict = {feat: float(imp) for feat, imp in zip(features, importances)}
        # Ordenar de mayor a menor
        feature_imp_sorted = dict(sorted(feature_imp_dict.items(), key=lambda item: item[1], reverse=True))
        evaluation_metrics[nombre_modelo]["feature_importances"] = feature_imp_sorted
        
    elif nombre_modelo == "XGBoost":
        importances = modelo.feature_importances_
        feature_imp_dict = {feat: float(imp) for feat, imp in zip(features, importances)}
        # Ordenar de mayor a menor
        feature_imp_sorted = dict(sorted(feature_imp_dict.items(), key=lambda item: item[1], reverse=True))
        evaluation_metrics[nombre_modelo]["feature_importances"] = feature_imp_sorted

# Guardar métricas en un archivo JSON
metrics_filename = "model_evaluation_metrics.json"
with open(metrics_filename, "w", encoding="utf-8") as f:
    json.dump(evaluation_metrics, f, indent=4, ensure_ascii=False)

print(f"Todas las métricas y datos de evaluación guardados en '{metrics_filename}'")
print("Entrenamiento completado de forma exitosa.")
