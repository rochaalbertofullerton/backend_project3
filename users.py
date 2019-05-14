import flask, sqlite3, hashlib, requests
from datetime import datetime, date
from flask import request , jsonify
from flask import Response
from cassandra.cluster import Cluster

app = flask.Flask(__name__)


@app.route('/users', methods=['Post'])
def postUser():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    keyname = data["name"]
    keyemail = data["email"]
    keypassword = data["password"]
    hashedpassword = hashlib.md5(keypassword.encode())
    try:
        session.execute('''INSERT INTO users (users_id, users_name, users_password) Values(%s,%s,%s) ''',(keyemail,keyname, hashedpassword.hexdigest(),))
        return jsonify("CREATED") , 201
    except Exception as er:
        return str(er), 400


@app.route('/users', methods=['DELETE'])
def delete_user(): 
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    key = data["email"]
    try:
        session.execute('''Delete from users Where users_id= %s''',(key,))
        return '<h1>DELETED</h1>', 200
    except Exception as er:
        return str(er), 400

@app.route('/users', methods=['PATCH'])
def change_pwd(): 
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    keyemail = data ["email"]
    keypassword = data["password"]
    hashedpassword = hashlib.md5(keypassword.encode())
    try:
        value = session.execute('''Select users_id From users Where users_id =%s''', (keyemail,))
        session.execute('''UPDATE users SET users_password =%s WHERE users_id=%s''' , (hashedpassword.hexdigest(),value[0].users_id,))
        return jsonify("UPDATED"), 202
    except Exception as er:
       return str(er), 404

@app.route('/users/auth')
def auth():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    a = {"status" : "ok"}
    b = {"status" : "bad" }
    auth = request.authorization
    try: 
        value = session.execute('''SELECT users_password FROM users WHERE users_id=%s''' , (auth.username,))
        if value[0].users_password == hashlib.md5(auth.password.encode()).hexdigest():
            return jsonify(a),200
        else:
            return jsonify(b),403
    except Exception as er:
        return str(er), 403

app.run(debug=True)

