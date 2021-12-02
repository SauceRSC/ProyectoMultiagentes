from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit

from numpy.ma import count
#from werkzeug import datastructures

app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

data = []
counter = 0
posts=0
pasos = 0
@app.route('/')
def root():
    global counter, data
    if(counter < len(data)):
        tmp = data[counter]
        counter+=1
    else:
        counter = 0
    return tmp

@app.route('/', methods = ['POST'])
def do_POST():
    global data, posts
    if request.method == 'POST':
        post_data = request.data
        #post_data_json = json.loads(post_data)
        data.append(post_data)
        posts+=1
        return str(posts)    

@app.route('/reset', methods = ['POST'])
def do_POSTReset():
    global data, posts, pasos
    if request.method == 'POST':
        post_data = request.data
        #post_data_json = json.loads(post_data)
        data = []
        posts = 0
        pasos = 0
        print("SERVER RESETEADO")
        return str("SERVER RESETEADO")  

@app.route('/pasos', methods = ['POST'])
def do_POSTPasos():
    global data, posts, pasos
    if request.method == 'POST':
        post_data = request.data
        #post_data_json = json.loads(post_data)
        pasos = post_data
        print("PASOS SETEADOS", pasos)
        return str(pasos) 

@app.route('/pasos', methods = ['GET'])
def do_GETPasos():
    global data, posts, pasos
    if request.method == 'GET':
        return str(pasos)

if __name__ == '_main_':
    app.run(host='localhost', port=port, debug=True)