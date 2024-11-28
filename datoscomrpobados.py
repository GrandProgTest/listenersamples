from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para almacenar los datos recibidos
clientes = []

def normalizar_cliente(cliente):
    """
    Normaliza el cliente recibido asegurando que tenga todos los campos requeridos.
    Si falta algún campo, se rellena con un valor vacío.
    """
    campos_requeridos = ["id", "email", "nombre", "pais", "url"]
    cliente_normalizado = {campo: cliente.get(campo, "") for campo in campos_requeridos}
    return cliente_normalizado

@app.route('/person', methods=['POST'])
def agregar_cliente():
    """
    Recibe un cliente desde una solicitud POST y lo almacena en la lista.
    """
    nuevo_cliente = request.json  # Obtiene el cliente enviado en la solicitud
    cliente_normalizado = normalizar_cliente(nuevo_cliente)  # Normaliza el cliente
    clientes.append(cliente_normalizado)  # Lo almacena en la lista
    return jsonify({"message": "Cliente agregado con éxito", "cliente": cliente_normalizado}), 201

@app.route('/person', methods=['GET'])
def listar_clientes():
    """
    Retorna la lista completa de clientes almacenados.
    """
    return jsonify(clientes), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
