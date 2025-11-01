# processor/screenshot.py

import os
# 1. AÑADE ESTA IMPORTACIÓN
from typing import Union
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import base64

# 2. MODIFICA ESTA LÍNEA DE LA FUNCIÓN
def take_screenshot(url: str) -> Union[str, None]:
    """
    Toma una captura de pantalla de una URL y la devuelve como una cadena base64.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto(url, timeout=60000, wait_until='domcontentloaded')
            page.wait_for_timeout(1000)

            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()

            base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
            return base64_image

    except PlaywrightTimeoutError:
        print(f"Timeout al intentar tomar screenshot de {url}.")
        return None
    except Exception as e:
        print(f"Error al tomar screenshot de {url}: {e}")
        return None

# --- Bloque de prueba (sin cambios) ---
def main():
    test_url = "https://www.github.com"
    print(f"📸 Tomando screenshot de: {test_url}")

    base64_data = take_screenshot(test_url)

    if base64_data:
        output_filename = "test_screenshot.png"
        with open(output_filename, "wb") as f:
            f.write(base64.b64decode(base64_data))
        print(f"✅ Screenshot guardado exitosamente como '{output_filename}'")
    else:
        print("❌ Falló la toma del screenshot.")

if __name__ == "__main__":
    main()