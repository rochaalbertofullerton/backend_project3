import flask ,sqlite3, hashlib, requests
from cassandra.cluster import Cluster
from datetime import datetime, date
from flask import request, jsonify
app = flask.Flask(__name__)



# POST A NEW COMMENT ON AN ARTICLE

@app.route('/comments/<path:article>', methods=['POST'])
def postComment(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    keycomment = data["comment"]
    keyurl = '/article/' + article

    try:
        value = session.execute('''select articles_id, articles_created, articles_comments from articles where articles_url=%s''', (keyurl,))
        lis=[]
        lis.append(keycomment)
        session.execute('''update articles SET articles_comments = articles_comments + %s where articles_id = %s and articles_created = %s''',(lis,value[0].articles_id,value[0].articles_created,))
        return 'Added', 200
            
    except Exception as er:
        return str(er),400




# DELETE AN INDIVIDUAL COMMENT 
@app.route('/comments/<article>', methods=['DELETE'])
def deleteComment(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    deleteCommentFromIndex = data['index']
    url = '/article/' + article
    try:
        value = session.execute('''Select articles_id, articles_created From articles Where articles_url = %s''', (url,)) 
        session.execute(''' Delete articles_comments[%s] from articles Where articles_id = %s And articles_created = %s''',(deleteCommentFromIndex, value[0].articles_id, value[0].articles_created,))
        return "OKAY", 200
    except Exception as er:
        return str(er), 400

    
# RETRIEVE THE NUMBER OF COMMENTS ON A GIVEN ARTICLE

@app.route('/comments/<path:article>', methods=['GET'])
def getcommentsforarticle(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    keyarticle = '/article/' + article

    try:
        value = session.execute('''Select articles_comments From articles Where articles_url = %s''', (keyarticle,))
        
        return jsonify(len(value[0].articles_comments)),200
    except Exception as er:
        return str(er), 400



# RETRIEVE THE 'N' MOST RECENT COMMENTS ON AN URL
@app.route('/comments/get/<path:article>', methods=['GET'] )
def getNthArticle(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    key = data["count"]
    keyarticle = '/article/' + article
    try:
        value = session.execute('''Select articles_comments From articles Where articles_url = %s''', (keyarticle, ))
        lis = value[0].articles_comments
        return jsonify(lis[:key]), 200
    except Exception as er:
        return str(er), 400






app.run(debug=True)