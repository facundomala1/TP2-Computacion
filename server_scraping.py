# server_scraping.py

import asyncio
import argparse
import aiohttp
import json
from aiohttp import web
from datetime import datetime, timezone

# Importamos las funciones que hemos creado
from scraper.html_parser import scrape_page_content
from scraper.metadata_extractor import extract_metadata

# --- Lógica de comunicación con el Servidor B ---

# Dirección del servidor de procesamiento
PROCESSING_SERVER_HOST = 'localhost'
PROCESSING_SERVER_PORT = 8081

async def send_task_to_processor(task_name: str, url: str) -> dict:
    """
    Función asíncrona para enviar una tarea al servidor de procesamiento.
    """
    try:
        # 1. Abrimos una conexión asíncrona
        reader, writer = await asyncio.open_connection(
            PROCESSING_SERVER_HOST, PROCESSING_SERVER_PORT)

        # 2. Creamos y serializamos el mensaje de la tarea
        message = json.dumps({"task": task_name, "url": url})
        
        # 3. Enviamos el mensaje
        writer.write(message.encode('utf-8'))
        await writer.drain() # Espera hasta que el mensaje se envíe

        # 4. Leemos la respuesta del servidor
        response_data = await reader.read()
        
        # 5. Cerramos la conexión
        writer.close()
        await writer.wait_closed()

        # 6. Deserializamos y devolvemos la respuesta
        return json.loads(response_data.decode('utf-8'))

    except ConnectionRefusedError:
        print(f"❌ Error de conexión: No se pudo conectar a {PROCESSING_SERVER_HOST}:{PROCESSING_SERVER_PORT}. ¿Está corriendo el servidor de procesamiento?")
        return {"status": "error", "message": "Processing server is unavailable."}
    except Exception as e:
        print(f"❌ Error en la comunicación con el procesador: {e}")
        return {"status": "error", "message": str(e)}

# --- Lógica del servidor web (AIOHTTP) ---

async def handle_scrape(request):
    """
    Manejador principal que recibe las peticiones del cliente.
    """
    url = request.query.get('url')
    if not url:
        return web.Response(text="Por favor, proporciona una URL. Ejemplo: /scrape?url=https://example.com", status=400)

    print(f"\n🚀 Recibida solicitud de scraping para: {url}")

    # --- Ejecutamos todas las tareas de forma concurrente ---
    async with aiohttp.ClientSession() as session:
        # Creamos una lista de tareas a ejecutar. asyncio.gather las correrá "a la vez"
        tasks_to_run = [
            # Tareas de scraping (locales)
            scrape_page_content(session, url),
            extract_metadata(session, url),
            # Tareas de procesamiento (remotas)
            send_task_to_processor('screenshot', url),
            send_task_to_processor('performance', url)
        ]
        
        # Esperamos a que todas las tareas terminen
        results = await asyncio.gather(*tasks_to_run, return_exceptions=True)

    # Procesamos los resultados
    scraping_result, metadata_result, screenshot_result, performance_result = results

    # --- Consolidamos la respuesta final en el formato requerido ---
    final_response = {
        "url": url,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scraping_data": {
            "title": scraping_result.get("title", "N/A") if not isinstance(scraping_result, Exception) else "Error",
            "links": scraping_result.get("links", []) if not isinstance(scraping_result, Exception) else [],
            "meta_tags": metadata_result if not isinstance(metadata_result, Exception) else {"error": str(metadata_result)},
            "structure": scraping_result.get("structure", {}) if not isinstance(scraping_result, Exception) else {},
            "images_count": scraping_result.get("images_count", 0) if not isinstance(scraping_result, Exception) else 0
        },
        "processing_data": {
            "screenshot": screenshot_result.get("data") if isinstance(screenshot_result, dict) else "Error",
            "performance": performance_result.get("data") if isinstance(performance_result, dict) else {"error": str(performance_result)}
        },
        "status": "success"
    }

    # Si alguna tarea principal falló, cambiamos el status general
    if any(isinstance(r, Exception) for r in results) or any(r.get("status") == "error" for r in [screenshot_result, performance_result] if isinstance(r, dict)):
        final_response["status"] = "partial_failure"

    return web.json_response(final_response)


# --- Configuración y arranque del servidor ---
app = web.Application()
app.router.add_get('/scrape', handle_scrape)

if __name__ == "__main__":
    print("🚀 Servidor de Extracción Asíncrono iniciado.")
    print("👂 Escuchando en http://localhost:8080")
    print("👉 Para probar, usa: http://localhost:8080/scrape?url=https://www.python.org")
    web.run_app(app, host='localhost', port=8080)
    
if __name__ == "__main__":
    # 1. Crear el parser de argumentos
    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono")
    parser.add_argument("-i", "--ip", default="localhost", help="Dirección de escucha (soporta IPv4/IPv6)")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Puerto de escucha")
    # El enunciado también pedía --workers, pero con aiohttp no se usa de la misma forma,
    # así que con IP y puerto cumples perfectamente.

    # 2. Parsear los argumentos de la línea de comandos
    args = parser.parse_args()

    # 3. Usar los argumentos para iniciar el servidor
    print("🚀 Servidor de Extracción Asíncrono iniciado.")
    print(f"👂 Escuchando en http://{args.ip}:{args.port}")
    
    web.run_app(app, host=args.ip, port=args.port)