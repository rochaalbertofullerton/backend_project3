import flask, sqlite3, hashlib, requests
from datetime import datetime, date
from flask import request , jsonify
from cassandra.cluster import Cluster
app = flask.Flask(__name__)


#ADD TAGS FOR NEW URL  & ADD TAGS TO AN EXISTING URL
#The json must contain "id", "tag"
#Example ----> /tag/The Road Not Taken1 {Hit Enter}
#The author must be created before before an article you can post a tag
#If an error occurs it will reply with the error and 204 Not acceptable
@app.route('/tag/<path:article>', methods=['POST'])
def postTag(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    keytag = data["tag"]
    keyurl ='/article/' + article
    setOfTag = {keytag}
    try:
        value = session.execute('''Select articles_id, articles_created From articles Where articles_url = %s''',(keyurl,))
        session.execute('''Update articles Set articles_tags = articles_tags + %s Where articles_id = %s And articles_created = %s''', (setOfTag, value[0].articles_id, value[0].articles_created,))
        return '<h1> ADDED</h1>', 200
    except Exception as er:
        return str(er), 400

    
#REMOVE ONE OR MORE TAGS FROM AN INDIVIDUAL URL
#The json must contain  "tag"
#Example ----> /tag/The Road Not Taken1 {Hit Enter}
#If an error occurs it will reply with the error and 204 Not acceptable
@app.route('/tag/<path:article>', methods=['DELETE'])
def deleteArticle(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    key = data["tag"]
    keyurl ='/article/' + article
    try:
       value = session.execute('''Select articles_id, articles_created, articles_tags From articles Where articles_url = %s''',(keyurl,))
       setOfTag= value[0].articles_tags
       setOfTag.remove(key)
       value = session.execute('''Update articles Set articles_tags = %s Where articles_id = %s And articles_created = %s''', (setOfTag, value[0].articles_id, value[0].articles_created,))
       return '<h1> REMOVED </h1>', 200
    except Exception as er:
        return str(er), 400

    


#RETRIEVE THE A LIST URLS WITH A GIVEN TAG
#Example ----> /tag/The Road Not Taken1 {Hit Enter}
@app.route("/tag/get/<path:tagtoremove>", methods=['GET'])
def getarticleswithTag(tagtoremove):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    listOfUrls = []
    try:
        value = session.execute('''Select articles_tags, articles_url from articles''')
        for row in value:
            if  type(row.articles_tags ) != type(None) :
                if tagtoremove in row.articles_tags:
                    listOfUrls.append(row.articles_url)   
        return jsonify(listOfUrls), 200
    except Exception as er:
        return str(er), 400

#RETRIEVE THE TAGS FOR AN INDIVIDUAL URL
#Example ----> /tag/The Road Not Taken1 {Hit Enter}
@app.route('/tag/<path:article>', methods=['GET'])
def gettagforUrl(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')    
    key = '/article/' + article
    try:
        value = session.execute('''Select articles_tags From articles Where articles_url =%s''',(key,))
        return jsonify(value[0].articles_tags), 200
    except Exception as er:
        return str(er), 400
    



app.run(debug=True, port=8080)