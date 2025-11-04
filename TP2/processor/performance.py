# processor/performance.py

import time
from typing import Dict, Any, Union
from playwright.sync_api import sync_playwright, Page, Route, TimeoutError as PlaywrightTimeoutError

def analyze_performance(url: str) -> Union[Dict[str, Any], None]:
    """
    Analiza el rendimiento de carga de una URL usando Playwright.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            requests_info = []

            def handle_response(response):
                """Función que se ejecuta por cada respuesta recibida."""
                try:
                    # Guardamos el tamaño del cuerpo de la respuesta
                    size = len(response.body())
                    requests_info.append({"size": size})
                except Exception:
                    # A veces el cuerpo no es accesible (ej. redirecciones), lo ignoramos
                    requests_info.append({"size": 0})

            # --- MODIFICADO: Escuchamos el evento 'response' en lugar de 'route' ---
            # Es más directo para lo que necesitamos.
            page.on("response", handle_response)

            start_time = time.time()
            
            # --- MODIFICADO: Cambiamos la condición de espera a 'domcontentloaded' ---
            page.goto(url, timeout=60000, wait_until='domcontentloaded')
            
            # Damos un par de segundos extra para que se capturen más respuestas de red
            page.wait_for_timeout(2000)
            
            end_time = time.time()
            
            browser.close()

            load_time_ms = int((end_time - start_time) * 1000)
            num_requests = len(requests_info)
            total_size_bytes = sum(req['size'] for req in requests_info)
            total_size_kb = round(total_size_bytes / 1024, 2)

            return {
                "load_time_ms": load_time_ms,
                "total_size_kb": total_size_kb,
                "num_requests": num_requests
            }

    except PlaywrightTimeoutError:
        print(f"Timeout al analizar el rendimiento de {url}.")
        return None
    except Exception as e:
        print(f"Error al analizar el rendimiento de {url}: {e}")
        return None

# --- Bloque de prueba (sin cambios) ---
def main():
    test_url = "https://www.google.com"
    print(f"🚀 Analizando rendimiento de: {test_url}")
    performance_data = analyze_performance(test_url)
    if performance_data:
        import json
        print("✅ Análisis completado:")
        print(json.dumps(performance_data, indent=2))
    else:
        print("❌ Falló el análisis de rendimiento.")

if __name__ == "__main__":
    main()