# common/protocol.py

import asyncio
import json
from typing import Dict, Any

async def send_task_to_processor(task: Dict[str, Any], host: str, port: int) -> Dict[str, Any]:
    """
    Se conecta al servidor de procesamiento, envía una tarea y espera la respuesta.
    """
    try:
        # Abre una conexión asíncrona con el servidor de procesamiento
        reader, writer = await asyncio.open_connection(host, port)

        # Prepara y envía el mensaje
        message = json.dumps(task).encode('utf-8')
        print(f"▶️  Enviando tarea '{task.get('task')}' al Servidor B...")
        writer.write(message)
        await writer.drain() # Espera a que el mensaje se envíe completamente

        # Cierra el canal de escritura para indicar que no enviaremos más datos
        writer.close_write()

        # Lee la respuesta del servidor
        response_data = await reader.read()
        print(f"◀️  Respuesta recibida del Servidor B.")

        # Cierra la conexión
        writer.close()
        await writer.wait_closed()

        return json.loads(response_data.decode('utf-8'))

    except ConnectionRefusedError:
        error_msg = "Error: La conexión con el servidor de procesamiento fue rechazada."
        print(f"❌ {error_msg}")
        return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"Error en la comunicación con el servidor de procesamiento: {e}"
        print(f"❌ {error_msg}")
        return {"status": "error", "message": error_msg}