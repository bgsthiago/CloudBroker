from flask import Flask, request, jsonify, render_template, redirect
# from bson.objectid import ObjectId
import json
import threading
import sys
import time
import requests

provedor = Flask(__name__)
port = int(sys.argv[1])
# url = "https://cloudbroker2019.herokuapp.com/{route}"
url = "http://localhost:5000/{route}"


def divulga():

    with open(f'info/{port}.json', 'r') as req:
        r = requests.post(url.format(route='divulgar'), data=req)
        return r.json(), r.status_code


@provedor.route('/usar', methods=['POST'])
def usar():

    data = ''
    with open(f'info/{port}.json', 'r+') as req:
        data = json.load(req)

    received_data = request.json
    id = int(received_data['id'])
    em_uso = data['maquinas'][id]['em_uso']

    if em_uso == False:
        data['maquinas'][id]['em_uso'] = True
        # req['maquina'][received_data['id']]['em_uso'] = True
        with open(f'info/{port}.json', 'w+') as req:
            json.dump(data, req, indent=2)
            # salva arquivo
            print(received_data)
        divulga()
        return jsonify({'mensagem': 'Máquina alocada com sucesso.'})
    else:
        return jsonify({'mensagem': 'Máquina já está em uso, por favor utilize outra máquina.'}), 409


@provedor.route('/liberar', methods=['POST'])
def liberar():

    data = ''
    with open(f'info/{port}.json', 'r+') as req:
        data = json.load(req)

    received_data = request.json
    id = int(received_data['id'])
    em_uso = data['maquinas'][id]['em_uso']

    if em_uso == True:
        data['maquinas'][id]['em_uso'] = False
        # req['maquina'][received_data['id']]['em_uso'] = True
        with open(f'info/{port}.json', 'w+') as req:
            json.dump(data, req, indent=2)
            # salva arquivo
            print(received_data)
        divulga()
        return jsonify({'mensagem': 'Máquina liberada com sucesso.'})
    else:
        return jsonify({'mensagem': 'Máquina não está em uso no momento.'}), 409        


if __name__ == "__main__":
    # divulga()
    provedor.run(host='localhost', debug=True, port=port)
