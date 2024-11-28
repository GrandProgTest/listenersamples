from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista para almacenar los datos recibidos
clientes = []

@app.route('/person', methods=['POST'])
def agregar_cliente():
    """
    Recibe un cliente desde una solicitud POST y lo almacena en la lista.
    """
    nuevo_cliente = request.json  
    clientes.append(nuevo_cliente)  
    return jsonify({"message": "Cliente agregado con éxito", "cliente": nuevo_cliente}), 201

@app.route('/person', methods=['GET'])
def listar_clientes():
    """
    Retorna la lista completa de clientes almacenados.
    """
    return jsonify(clientes), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
