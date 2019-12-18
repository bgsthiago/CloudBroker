from flask import Flask, request, jsonify, render_template, redirect
# from bson.objectid import ObjectId
import json
import threading
import sys
import requests

provedor = Flask(__name__)
# url = "https://cloudbroker2019.herokuapp.com/{route}"
url = "http://localhost:5000/{route}"
url_provedor = "http://localhost:{provedor}/{route}"

# {
#   "qtd_vcpu": 4,
#   "qtd_ram": 16,
#   "qtd_disco": 128
# }


def procura():
    with open('req.json', 'r') as req:
        r = requests.post(url.format(route='encontrar'), data=req)
        return r.json(), r.status_code


def usa(provedor, id):
    r = requests.post(url_provedor.format(
        provedor=provedor, route='usar'), json={"id": id})
    return r.json(), r.status_code


def libera(provedor, id):
    r = requests.post(url_provedor.format(
        provedor=provedor, route='liberar'), json={"id": id})
    return r.json(), r.status_code


if __name__ == "__main__":
    x = procura()
    print(x[0])
    print(x[1])
    if x[1] == 200:
        print('oi')
        print(usa(x[0]['provedor'], x[0]['maquina']))
        print(libera(x[0]['provedor'], x[0]['maquina']))

    #     provedor.run(host='localhost', debug=True, port=5015)
