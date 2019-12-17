from flask import Flask, request, jsonify, render_template, redirect
# from bson.objectid import ObjectId
import json
import threading
import sys
import requests

provedor = Flask(__name__)
port = int(sys.argv[1])
# url = "https://cloudbroker2019.herokuapp.com/{route}"
url = "http://localhost:5000/{route}"


def divulga():
    with open(f'info/{port}.json', 'r') as req:
        r = requests.post(url.format(route='divulgar'), data=req)
        return r.json(), r.status_code


def receiver():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))

    while True:
        data, source = s.recvfrom(1500)
        data = data.decode('utf-8')
        message = json.loads(data)

        t = threading.Thread(target=handle_message,
                             args=(message, my_id))
        t.start()


t = threading.Thread(target=receiver, args=())
t.start()

if __name__ == "__main__":
    provedor.run(host='localhost', debug=True, port=5001)
