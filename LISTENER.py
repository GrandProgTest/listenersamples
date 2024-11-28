import os
import time
import stomp
import requests  # Para hacer peticiones HTTP al servicio REST

def connect_and_subscribe(conn):
    conn.connect('admin', 'admin', wait=True)
    conn.subscribe(destination='/queue/test', id=1, ack='auto', headers={'transformation': 'jms-map-json'})

class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('mensaje recibido "%s"' % frame.body)

        # Procesamos el mensaje recibido
        partes = frame.body.split('|')  # Suponiendo que los campos están separados por '|'

        # Verificamos si el mensaje tiene el número correcto de partes (4 partes)
        if len(partes) == 4:
            # Creamos un diccionario con los datos del mensaje
            cliente = {
                "id": partes[0],
                "nombre": partes[1],
                "pais": partes[2],
                "url": partes[3]
            }

            # Dirección del servicio REST (asegúrate de que Flask esté corriendo en el puerto adecuado)
            url = "http://127.0.0.1:8080/person"
            
            # Enviar el cliente al servicio REST
            response = requests.post(url, json=cliente)
            
            # Verificamos la respuesta del servicio REST
            if response.status_code == 201:
                print(f"Cliente {cliente['nombre']} agregado correctamente.")
            else:
                print(f"Error al agregar cliente: {response.status_code}")
        else:
            print("Mensaje recibido no tiene el formato esperado. No se procesará.")
        
        print('mensaje procesado')

    def on_disconnected(self):
        print('desconectado')
        connect_and_subscribe(self.conn)

# Crear la conexión STOMP y suscribirse a la cola
conn = stomp.Connection([('localhost', 61613)], heartbeats=(4000, 4000))
conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)

# Mantener el listener en ejecución durante 120 segundos
print('Listener levantado por 120 segundos')
time.sleep(120)

# Desconectar la conexión STOMP después de 120 segundos
conn.disconnect()
