# client.py
import requests
import json

# URL del servidor de scraping
SERVER_URL = "http://localhost:8080/scrape"

# URL que quieres analizar
TARGET_URL = "https://www.wikipedia.org"

print(f"Solicitando análisis para: {TARGET_URL}")

try:
    # Hacemos la petición GET al servidor A
    response = requests.get(SERVER_URL, params={"url": TARGET_URL}, timeout=100)
    
    # Nos aseguramos de que la petición fue exitosa
    response.raise_for_status()
    
    # Imprimimos la respuesta JSON de forma legible
    data = response.json()
    print("\n✅ ¡Respuesta recibida exitosamente!")
    
    # Para no imprimir la imagen larguísima en base64, la omitimos
    if data.get("processing_data", {}).get("screenshot"):
        data["processing_data"]["screenshot"] = "¡Imagen recibida! (omitida por brevedad)"

    print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"\n❌ Error al conectar con el servidor: {e}")