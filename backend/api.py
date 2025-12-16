"""
-------------------------------------------------------------------------
PROYECTO: PREDICCIÓN HOSPITALARIA (Samsung Innovation Campus)
ARCHIVO: api.py
DESCRIPCIÓN: API Backend para predicción de estancia y demanda usando IA
             y datos climáticos en tiempo real.

DEPENDENCIAS NECESARIAS:
Para ejecutar este código, asegúrate de tener instaladas las siguientes
librerías en tu entorno de Python (terminal):

pip install fastapi uvicorn pandas scikit-learn joblib requests pydantic

NOTA SOBRE VERSIONES:
- fastapi: Para crear la API.
- uvicorn: Servidor para correr la API.
- pandas: Para manejar los datos en tablas.
- scikit-learn: Necesaria para que funcionen los modelos .pkl cargados.
- joblib: Para cargar los archivos .pkl.
- requests: Para conectarse a OpenWeatherMap (Internet).
-------------------------------------------------------------------------
"""

import pandas as pd
import joblib
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# --- 1. CONFIGURACIÓN ---

# ¡IMPORTANTE!
OPENWEATHER_API_KEY = "c4928901293ce06a0dbf1f02d94b3b04"

# Coordenadas de Santo Domingo, RD (Referencia: Zona Metro)
LAT = 18.4861
LON = -69.9312

# Iniciar la App
app = FastAPI(title="Pro-Hosp API", version="3.1 Connected")

# Configurar permisos (CORS) para que el Frontend pueda entrar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. CARGA DE MODELOS ---
model_stay = None
model_block = None
model_demand = None
MODELOS_OK = False
FECHA_REFERENCIA = pd.to_datetime("2023-01-01")

try:
    print("🔄 Cargando cerebros de la IA...")
    model_stay = joblib.load("model_stay.pkl")
    model_block = joblib.load("model_block.pkl")
    model_demand = joblib.load("model_demand.pkl")
    MODELOS_OK = True
    print("✅ Modelos cargados exitosamente.")
except Exception as e:
    print(f"❌ Error Crítico: No se encontraron los modelos .pkl: {str(e)}")
    MODELOS_OK = False

# --- 3. ESTRUCTURAS DE DATOS (Schemas) ---

class PacienteInput(BaseModel):
    Department: str
    Ward_Type: str
    Ward_Facility: str
    Type_of_Admission: str
    Illness_Severity: str
    Age: str
    Hospital_type: int
    Hospital_city: int
    Hospital_region: int
    Available_Extra_Rooms_in_Hospital: int
    Bed_Grade: float
    Patient_Visitors: int
    City_Code_Patient: float
    Admission_Deposit: float

class DemandaInput(BaseModel):
    date: str  # Formato: "YYYY-MM-DD"

# --- 4. FUNCIONES AUXILIARES ---

def get_live_weather():
    """
    Obtiene clima real de Santo Domingo desde OpenWeatherMap.
    Traduce (Mapea) los datos numéricos a categorías para la IA.
    """
    try:
        # Llamada 1: Clima general
        url_weather = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=metric"
        res_weather = requests.get(url_weather, timeout=5).json()

        # Llamada 2: Contaminación del aire
        url_air = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}"
        res_air = requests.get(url_air, timeout=5).json()

        # Extraer datos crudos
        main_data = res_weather["main"]
        wind_data = res_weather["wind"]
        pollutants = res_air["list"][0]["components"]
        aqi_number = res_air["list"][0]["main"]["aqi"] # Viene 1, 2, 3, 4, 5

        # --- AQUÍ ESTÁ EL MAPEO ---
        # Convertimos el número de la API a la palabra que espera el modelo
        aqi_map = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        # Si llega un numero raro, usamos "Moderate" por defecto
        aqi_status = aqi_map.get(aqi_number, "Moderate") 

        return {
            "temperature": main_data["temp"],
            "humidity": main_data["humidity"],
            "wind_speed": wind_data["speed"],
            "pm25": pollutants["pm2_5"],
            "pm10": pollutants["pm10"],
            "no2": pollutants["no2"],
            "so2": pollutants["so2"],
            "co": pollutants["co"],
            "o3": pollutants["o3"],
            "aqi": float(aqi_number * 20), # Escala visual para el frontend
            "status": aqi_status, # Texto mapeado (Ej: "Good")
            "is_simulated": False
        }

    except Exception as e:
        print(f"⚠️ Alerta: Falló la conexión a OpenWeather ({e}). Usando simulación.")
        # FALLBACK: Promedios de Santo Domingo si falla internet
        return {
            "temperature": 31.0, "humidity": 78.0, "wind_speed": 12.0,
            "pm25": 15.0, "pm10": 35.0, "no2": 12.0, "so2": 5.0,
            "co": 0.8, "o3": 25.0, "aqi": 60.0,
            "status": "Moderate",
            "is_simulated": True
        }

# --- 5. ENDPOINTS DE LA API ---

@app.get("/")
def home():
    return {"status": "online", "system": "Hospital Demand Predictor v3.1"}

@app.post("/predict_patient")
def predict_patient(data: PacienteInput):
    """ Predice estancia y riesgo de bloqueo de camas """
    if not MODELOS_OK:
        raise HTTPException(status_code=500, detail="Modelos no cargados")

    try:
        # Preprocesamiento
        input_dict = data.dict()
        # Corregir nombre de columna (los espacios en Python son delicados)
        input_dict['Type of Admission'] = input_dict.pop('Type_of_Admission')
        
        df = pd.DataFrame([input_dict])
        
        # Predicción
        pred_dias = model_stay.predict(df)[0]
        pred_riesgo = model_block.predict(df)[0]

        return {
            "estancia_estimada": pred_dias,
            "riesgo_bloqueo": int(pred_riesgo),
            "mensaje": "ALERTA: Paciente de Larga Estancia" if pred_riesgo == 1 else "Estancia Standard"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en datos: {str(e)}")

@app.post("/predict_demand")
def predict_demand(data: DemandaInput):
    """ 
    Predice demanda respiratoria cruzando fecha + clima real
    """
    if not MODELOS_OK:
        raise HTTPException(status_code=500, detail="Modelos no cargados")
    
    try:
        # 1. Obtener clima (Real o Simulado)
        weather = get_live_weather()

        # 2. Armar el DataFrame para el modelo
        input_data = {
            "date": data.date,
            "AQI": weather["aqi"],
            "PM2.5": weather["pm25"],
            "PM10": weather["pm10"],
            "NO2": weather["no2"],
            "SO2": weather["so2"],
            "CO": weather["co"],
            "O3": weather["o3"],
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "wind_speed": weather["wind_speed"],
            "AirQuality_Status": weather["status"]
        }
        
        df_input = pd.DataFrame([input_data])
        
        # 3. Ingeniería de Fechas
        df_input["date"] = pd.to_datetime(df_input["date"])
        df_input["date_num"] = (df_input["date"] - FECHA_REFERENCIA).dt.days
        df_input = df_input.drop(columns=["date"])

        # 4. Predicción
        prediction = model_demand.predict(df_input)[0]

        return {
            "fecha": data.date,
            "admisiones_respiratorias_esperadas": float(prediction),
            "clima_usado": weather
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando demanda: {str(e)}")

# Para correr esto localmente:
# uvicorn api:app --reload