# BACKEND: main.py adaptado para Replit con FastAPI y Selenium
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

app = FastAPI()

# Permitir acceso desde cualquier origen (Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos
class InscripcionData(BaseModel):
    link: str
    usuario: str
    password: str
    whatsapp: str

@app.post("/inscribir")
async def inscribir(data: InscripcionData):
    try:
        # Configurar Selenium con Chromium en Replit
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # Replit usa esta ruta para el ejecutable de Chromium
        chrome_options.binary_location = "/usr/bin/chromium-browser"

        driver = webdriver.Chrome(options=chrome_options)

        # 1. Ir al curso
        driver.get(data.link)
        time.sleep(5)

        # 2. Login
        driver.find_element(By.NAME, "cuil").send_keys(data.usuario)
        driver.find_element(By.NAME, "password").send_keys(data.password)
        driver.find_element(By.XPATH, "//button[contains(text(),'Ingresar')]").click()
        time.sleep(5)

        # 3. Aceptar acuerdo e inscribir
        driver.find_element(By.ID, "acuerdo").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Confirmar')]").click()
        time.sleep(3)

        # 4. WhatsApp Web (se omite en Replit headless)
        # Normalmente se abriría WhatsApp Web para enviar mensaje
        # Pero no es visible ni funcional en modo headless sin interfaz

        driver.quit()

        return {"message": "✅ Inscripción realizada con éxito. (Mensaje WhatsApp omitido en Replit)"}

    except Exception as e:
        print("Error:", e)
        return {"message": "❌ Error durante el proceso: " + str(e)}
