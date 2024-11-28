from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para almacenar los datos recibidos
clientes = []

def normalizar_cliente(cliente, campos_requeridos):
    """
    Normaliza el cliente recibido asegurando que tenga todos los campos requeridos.
    Si falta algún campo, se rellena con un valor vacío.
    """
    cliente_normalizado = {campo: cliente.get(campo, "") for campo in campos_requeridos}
    return cliente_normalizado

@app.route('/person/<campo>', methods=['POST'])
def agregar_cliente(campo):
    """
    Recibe un cliente desde una solicitud POST y lo almacena en la lista.
    Verifica que el campo obligatorio según la ruta esté presente.
    """
    nuevo_cliente = request.json  # Obtiene el cliente enviado en la solicitud

    # Lista de todos los posibles campos con el campo de la ruta como obligatorio
    campos_posibles = ["id", "email", "nombre", "pais", "url"]
    if campo not in campos_posibles:
        return jsonify({"error": f"El campo '{campo}' no es válido"}), 400

    # Verificar que el campo obligatorio esté presente
    if campo not in nuevo_cliente or not nuevo_cliente[campo]:
        return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    # Normalizar cliente y agregarlo a la lista
    cliente_normalizado = normalizar_cliente(nuevo_cliente, campos_posibles)
    clientes.append(cliente_normalizado)
    return jsonify({"message": "Cliente agregado con éxito", "cliente": cliente_normalizado}), 201

@app.route('/person', methods=['GET'])
def listar_clientes():
    """
    Retorna la lista completa de clientes almacenados.
    """
    return jsonify(clientes), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
