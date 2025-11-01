# server_processing.py

import socketserver
import argparse
import json
import concurrent.futures
from typing import Union  # Para compatibilidad con Python 3.8

# Importamos las funciones que este servidor sabe ejecutar
from processor.screenshot import take_screenshot
from processor.performance import analyze_performance

# Creamos un diccionario para mapear nombres de tareas a funciones
TASK_REGISTRY = {
    'screenshot': take_screenshot,
    'performance': analyze_performance
}

# server_processing.py

class TaskHandler(socketserver.BaseRequestHandler):
    """
    El manejador de solicitudes para nuestro servidor.
    Se crea una instancia de esta clase por cada conexión recibida.
    """

    def handle(self):
        print(f"▶️ Conexión recibida de: {self.client_address[0]}")
        
        try:
            # 1. Recibir los datos del socket
            data = b""
            while True:
                chunk = self.request.recv(4096)
                if not chunk:
                    break
                data += chunk
                if len(chunk) < 4096:
                    break
            
            if not data:
                print("⚠️ Conexión cerrada sin recibir datos.")
                return

            # 2. Deserializar el mensaje JSON
            message = json.loads(data.decode('utf-8'))
            task_name = message.get("task")
            url = message.get("url")

            if not task_name or not url:
                raise ValueError("Mensaje inválido, faltan 'task' o 'url'")

            print(f"⚙️ Tarea recibida: '{task_name}' para la URL: {url}")

            # 3. Obtener la función correcta del registro
            task_function = TASK_REGISTRY.get(task_name)
            if not task_function:
                raise ValueError(f"Tarea desconocida: {task_name}")

            # 4. Enviar la tarea al pool de procesos
            future = self.server.process_pool.submit(task_function, url)
            
            # 5. Obtener el resultado usando .result()
            #    Aumentamos el timeout a 90s para estar seguros.
            result = future.result(timeout=90) # <-- ¡AQUÍ ESTÁ EL CAMBIO!
            
            response = {"status": "success", "data": result}
            print(f"✅ Tarea '{task_name}' completada.")

        except Exception as e:
            print(f"❌ Error procesando la solicitud: {e}")
            response = {"status": "error", "message": str(e)}
        
        # 6. Serializar la respuesta y enviarla de vuelta
        self.request.sendall(json.dumps(response).encode('utf-8'))



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    Un servidor TCP que maneja cada conexión en un hilo separado.
    Esto es crucial para que pueda atender a múltiples peticiones del Servidor A a la vez.
    """
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, process_pool):
        super().__init__(server_address, RequestHandlerClass)
        self.process_pool = process_pool


def main():
    HOST, PORT = "localhost", 8081 # Usaremos el puerto 8081 para este servidor

    # Crear el pool de procesos que se compartirá entre todas las conexiones
    # Usará tantos procesos como núcleos de CPU tengas.
    with concurrent.futures.ProcessPoolExecutor() as pool:
        print("🚀 Servidor de Procesamiento iniciado.")
        print(f"🏊 Pool de {pool._max_workers} procesos trabajadores creado.")
        
        with ThreadedTCPServer((HOST, PORT), TaskHandler, process_pool=pool) as server:
            print(f"👂 Escuchando en {HOST}:{PORT}")
            # Mantener el servidor corriendo hasta que se interrumpa (Ctrl+C)
            server.serve_forever()

if __name__ == "__main__":
    main()
    
def main():
    # 1. Crear el parser de argumentos
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument("-i", "--ip", default="localhost", help="Dirección de escucha")
    parser.add_argument("-p", "--port", type=int, default=8081, help="Puerto de escucha")
    # El enunciado menciona -n para el número de procesos, ProcessPoolExecutor lo elige automáticamente.
    # Dejarlo así es una implementación válida y eficiente.

    # 2. Parsear los argumentos
    args = parser.parse_args()

    # 3. Usar los argumentos para iniciar el servidor
    with concurrent.futures.ProcessPoolExecutor() as pool:
        print("🚀 Servidor de Procesamiento iniciado.")
        print(f"🏊 Pool de {pool._max_workers} procesos trabajadores creado.")
        
        # Usa args.ip y args.port en lugar de valores fijos
        with ThreadedTCPServer((args.ip, args.port), TaskHandler, process_pool=pool) as server:
            print(f"👂 Escuchando en {args.ip}:{args.port}")
            server.serve_forever()

if __name__ == "__main__":
    main()