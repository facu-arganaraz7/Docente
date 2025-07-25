from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/inscribir")
async def inscribir(
    link: str = Form(...),
    cuil: str = Form(...),
    password: str = Form(...)
):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    print("▶️ Monitoreando habilitación de la inscripción...")
    driver.get(link)

    while True:
        try:
            # Espera y clic al botón "Preinscripciones Abiertas"
            boton = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[span[contains(text(), 'Preinscipciones Abiertas')]]")
            ))
            print("🟢 Botón encontrado. Abriendo formulario...")
            boton.click()

            # Espera a que aparezcan los inputs del modal
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "el-input__inner")))
            inputs = driver.find_elements(By.CLASS_NAME, "el-input__inner")

            if len(inputs) >= 2:
                inputs[0].send_keys(cuil)
                inputs[1].send_keys(password)
            else:
                raise Exception("❌ No se encontraron los campos para CUIL y contraseña.")

            # Clic en "Estoy de acuerdo"
            acuerdo = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'Estoy de acuerdo')]")
            ))
            acuerdo.click()
            print("✅ Acuerdo aceptado.")

            # Esperar a que el botón de preinscripción esté habilitado
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[span[contains(text(), 'REALIZAR Preinscripción')] and not(@disabled)]")
            ))

            boton_inscribir = driver.find_element(
                By.XPATH, "//button[span[contains(text(), 'REALIZAR Preinscripción')]]"
            )
            boton_inscribir.click()
            print("✅ Inscripción realizada correctamente.")
            break

        except Exception as e:
            print(f"⚠️ No se encontró botón o falló el proceso. Reintentando...\n{e}")
            time.sleep(1)
            driver.refresh()

    return {"status": "ok", "message": "✅ Inscripción finalizada con éxito"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
