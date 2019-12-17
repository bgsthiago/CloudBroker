from flask import Flask, request, jsonify, render_template, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import loads, dumps
from datetime import date
import json
import os


app = Flask(__name__)

# db config nuvem
# app.config['MONGO_DBNAME'] = 'heroku_ldzh9cl7'
# app.config['MONGO_URI'] = 'mongodb://heroku_ldzh9cl7:ut7hph7s95u3lq9qf019p1lol3@ds137263.mlab.com:37263/heroku_ldzh9cl7?heroretryWrites=false'

# db config local
# app.config['MONGO_DBNAME'] = 'cloudbroker'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cloudbroker'

# db get
mongo = PyMongo(app)
claudio = mongo.db.cloudbroker


@app.route('/')
def hello_stranger():
    return jsonify({'Hey, you': ''.join('You\'re finally awake.')})

# provedor
@app.route('/divulgar', methods=['POST'])
def acesso_provedor():
    received_data = loads(request.data.decode('utf-8'))
    print(received_data)
    # ans = {
    #        'qtd_vcpu': received_data['maquina']['qtd_vcpu'],
    #        'qtd_ram': received_data['maquina']['qtd_ram'],
    #        'qtd_disco': received_data['maquina']['qtd_disco'],
    #        'preco': received_data['maquina']['preco'],
    #        'em_uso': received_data['maquina']['em_uso']}
    try:
        claudio.update({'nome':received_data['nome']}, received_data, upsert = True)
    except:
        return jsonify({'Message': 'Error.'}), 400

    # print('CADASTRADO COM SUCESSO:\nvCPUS : ', vCPU, '\nRAM :',
    #       RAM, 'GB\nHD :', HD, 'GB\nPREÇO R$', PRECO)

    return jsonify(dumps(received_data)), 201

# cliente


@app.route('/encontrar', methods=['POST'])
def busca():
    received_data = json.load(request.files['datas'])
    vCPU = received_data['vCPU']
    RAM = received_data['RAM']
    HD = received_data['HD']
    a = mongo.db.test1.find({"$and": [{'vCPU': {"$gte": vCPU}}, {'RAM': {"$gte": RAM}}, {
                            'HD': {"$gte": HD}}, {'Disp': 1}]}).sort('RS').limit(1)
    try:
        print('Foi Achado essa VM:\n')
        print(a[0])
        msg = 'Foi Achado um com as seguintes configuraçoes:\nvCPUS : ', str(a[0]['vCPU']), '\nRAM :', str(a[0]['RAM']), '  GB\nHD :', str(
            a[0]['HD']), '  GB\nPREÇO R$ ', str(a[0]['RS']), '\nLink de Acesso: 127.0.0.1:', str(a[0]['Prov']), '\nMaquina : ', str(a[0]['Maq'])
        resposta = {'Mensagem': ''.join(msg)}
    except:
        msg = 'Nenhum Recurso com essas especificações foi encontrado'
        print(msg)
        resposta = {'Mensagem': ''.join(msg)}
    return jsonify(resposta)


@app.route('/utilizar', methods=['POST'])
def cliente_usa():
    received_data = json.load(request.files['datas'])
    try:
        a = mongo.db.test1.update(
            {'Prov': received_data['Prov'], 'Maq': received_data['Maq']}, {'$set': {'Disp': 0}})
        print('Um registro alterado')
        msg = 'Sucesso'
    except:
        print('Erro, maquina inexistente')
        msg = 'Erro'
    return jsonify({'Mensagem': msg})


@app.route('/liberar', methods=['POST'])
def cliente_liberando():
    received_data = json.load(request.files['datas'])
    try:
        a = mongo.db.test1.update(
            {'Prov': received_data['Prov'], 'Maq': received_data['Maq']}, {'$set': {'Disp': 1}})
        print('Um registro alterado')
        msg = 'Sucesso'
    except:
        print('Erro, maquina inexistente')
        msg = 'Erro'
    return jsonify({'Mensagem': msg})


if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
