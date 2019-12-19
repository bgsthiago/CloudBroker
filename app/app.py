from flask import Flask, request, jsonify, render_template, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from datetime import date
import json
import os


app = Flask(__name__)

# db config nuvem
app.config['MONGO_DBNAME'] = 'heroku_ldzh9cl7'
app.config['MONGO_URI'] = 'mongodb://heroku_ldzh9cl7:ut7hph7s95u3lq9qf019p1lol3@ds137263.mlab.com:37263/heroku_ldzh9cl7?retryWrites=false'

# db config local
# app.config['MONGO_DBNAME'] = 'cloudbroker'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/cloudbroker'

# db get
mongo = PyMongo(app)
claudio = mongo.db.cloudbroker


@app.route('/')
def hello_stranger():
    return jsonify({'Hey, you': ''.join('You\'re finally awake.')})


@app.route('/lista')
def lista():
    for x in claudio.find():
        print(x)
    return 'String'

# provedor
@app.route('/divulgar', methods=['POST'])
def acesso_provedor():
    received_data = loads(request.data.decode('utf-8'))
    print(received_data)
    try:
        for each in received_data['maquinas']:

            claudio.update(
                {'nome': each['nome'], 'id': each['id']}, each, upsert=True)

    except Exception as e:
        print(e)
        return jsonify({'Message': 'Error.'}), 400

    return jsonify(dumps(received_data)), 201

# cliente


@app.route('/encontrar', methods=['POST'])
def busca():
    received_data = loads(request.data.decode('utf-8'))
    vcpu = received_data['qtd_vcpu']
    mem = received_data['qtd_ram']
    disco = received_data['qtd_disco']

    a = claudio.find({"$and": [{'qtd_vcpu': {"$gte": vcpu}}, {'qtd_ram': {"$gte": mem}},
                               {'qtd_disco': {"$gte": disco}}, {'em_uso': False}]}).sort('preco').limit(1)
    print(type(a))
    try:
        print('Foi Achado essa VM:\n')
        print(a[0])

        resposta = {'provedor': a[0]['nome'], 'maquina': a[0]['id'], 'preco': a[0]['preco'],
                    'qtd_vcpu': a[0]['qtd_vcpu'], 'qtd_ram': a[0]['qtd_ram'], 'qtd_disco': a[0]['qtd_disco'], 'acesso': "http://localhost:{provedor}/usar".format(provedor=a[0]['nome'])}
    except:
        print('Nenhum Recurso com essas especificações foi encontrado')
        return jsonify({'Message': 'Error. Nao foi encontrado'}), 400
    return jsonify(resposta)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
