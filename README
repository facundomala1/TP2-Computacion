# 🚀 TP2 Computación: Analizador Web CLI

Este proyecto es un script de línea de comandos (CLI) en **Python** que analiza una URL y extrae información clave sobre su estructura, contenido y rendimiento.

## 📋 Características Principales

- **Extracción de Metadatos**: Obtiene el título, la descripción y las etiquetas Open Graph (`og:title`, `og:description`, etc.).
- **Análisis Estructural**: Cuenta la jerarquía de encabezados de la página (`h1`, `h2`, `h3`, ...).
- **Recolección de Enlaces**: Lista todos los enlaces (`<a>`) encontrados.
- **Métricas de Rendimiento**: Mide el tiempo de carga (`load_time_ms`), el tamaño total de la página (`total_size_kb`) y el número de peticiones (`num_requests`).
- **Captura de Pantalla**: Genera un *screenshot* del sitio analizado.
- **Salida JSON**: Devuelve un informe estructurado y fácil de procesar con todos los datos recolectados.

## 🧩 Estructura del Proyecto

El repositorio está organizado en varios módulos para separar las responsabilidades:

- **cli.py**: Contiene la lógica principal del script, incluyendo la interfaz de línea de comandos.
- **common**: Contiene funciones comunes utilizadas por varios módulos.
- **processor**: Contiene el procesamiento de la información extraída.
- **scraper**: Contiene la capa de extracción de datos de la web.
- **server_processing.py**: Contiene el procesamiento de datos en el servidor.
- **server_scraping.py**: Contiene la capa de extracción de datos en el servidor.
- **requirements.txt**: Lista de dependencias necesarias para el proyecto.
- **LICENSE**: Licencia del proyecto.


## 🛠️ Instalación

1. **Cloná este repositorio**

   ```bash
   git clone https://github.com/facundomala1/TP2-Computacion.git
   cd TP2-Computacion

2. **Instala las dependencias**

   ```bash
   pip install -r requirements.txt

## Modo de uso

El script puede ejecutarse desde la línea de comandos con las siguientes opciones:
- `python cli.py <URL>`: Analiza la URL y muestra un informe detallado.
- `python cli.py --screenshot <URL>`: Analiza la URL y genera un *screenshot* del sitio.
- `python cli.py --performance <URL>`: Analiza la URL y muestra métricas de rendimiento.
- `python cli.py --metadata <URL>`: Analiza la URL y muestra metadatos clave.
- `python cli.py --links <URL>`: Analiza la URL y lista todos los enlaces encontrados.
- `python cli.py --json <URL>`: Analiza la URL y devuelve un informe estructurado en formato JSON.

### Ejemplo de salida

{
  "title": "Ejemplo de página web",
  "description": "Esta es una página de ejemplo.",
  "headings": {"h1": 1, "h2": 3},
  "links": ["https://www.otro-ejemplo.com", "/contacto"],
  "load_time_ms": 1200,
  "total_size_kb": 245.6,
  "num_requests": 18
}

---
End code/documentation snippets.
