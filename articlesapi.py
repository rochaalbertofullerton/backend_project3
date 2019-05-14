import flask, requests,  json, uuid
from cassandra.cluster import Cluster
from datetime import datetime, date
from flask import request , jsonify
from cassandra.query import ordered_dict_factory 
app = flask.Flask(__name__)



#POST A NEW ARTICLE
#This route gets activited when a POST is made. It does expect json 
#The json must contain and id, text, title, author
#The author must be created before before an article can be posted, the author is a foreign key
#If an error occurs it will reply with the error and 406 Not acceptable
@app.route('/article', methods=['POST'])
def postArticle():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    keytext = data["text"]
    keytitle = data["title"]
    keyauthor = data["author"]
    keyurl = '/article/' + keytitle.replace(" ", "") 
    try:
        session.execute('''INSERT INTO articles (articles_id, articles_title, articles_content, articles_created , articles_modified, articles_users_author, articles_url) Values(%s,%s,%s,%s,%s,%s,%s ) ''',(uuid.uuid4() ,keytitle, keytext,datetime.now(),datetime.now(),keyauthor,keyurl))

        return jsonify("CREATED") , 201
    except Exception as er:
        return str(er), 400


#RETREVE AN INDIVIDUAL ARTICLE
#This route get activated when you pass an article name after the the root file of '/article/
#Example ----> /article/The Road Not Taken1 {Hit Enter}
#If an error is occurs a 204 status will be returned not content found else if no error is found it will return a 200 OK
@app.route("/article/<path:article>", methods=['GET'])
def getArticle(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    key = '/article/' + article

    try:
        value = session.execute('''SELECT articles_content FROM articles WHERE articles_url=%s''' , (key,))
        return jsonify(value[0]),200

    except:
        return '<h1>Article Does Not Exist</h1>', 400

# EDIT AN INDIVIDUAL ARTICLE
#This route gets activited when a PATCH is made. It does expect json 
#The json must contain  "text"
#Example ----> /article/The Road Not Taken1 {Hit Enter}
#If an error occurs it will reply with the error and 204 There was no article with that url
@app.route("/article/<path:article>", methods=['PATCH'])
def patchArticle(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    keyid = '/article/' + article
    keytext = data ["text"]
    try:
        value = session.execute('''Select articles_id , articles_created from articles Where articles_url = %s''', (keyid,))
        session.execute('''UPDATE articles SET articles_content=%s, articles_modified=%s WHERE articles_id=%s and articles_created=%s''' , (keytext, datetime.now(), value[0].articles_id,value[0].articles_created,))
        return jsonify("UPDATED"), 202

    except Exception as er:
        return str(er), 406

       

#DELETE A SPECIFIC EXISTING ARTICLE
#This route gets activited when a DELETE is made. It does expect json 
#The json must contain and id
#If an error occurs it will reply with the error and 204 There was no article with that id
@app.route("/article/<path:article>", methods=['DELETE'])
def deleteArticle(article):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    key = '/article/' + article
    try:
        value = session.execute('''SELECT articles_id, articles_created FROM articles WHERE articles_url =%s''', (key,))
        session.execute('''Delete From articles Where articles_id = %s and articles_created=%s''',(value[0].articles_id,value[0].articles_created,))
        return jsonify("Deleted"), 200
    except Exception:
        return '<h1>Article Does Not Exist...</h1>', 406

#RETRIEVE THE ENITRE CONTENTS (INCLUDING ARTICLE TEXT) FOR THE N MOST RECENT ARTICLE


@app.route('/article/content', methods=['GET'] )
def getArticleContent():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    key = data['count']
    json_list=[]

    try:
        value = session.execute('''Select * From articles limit %s''', (key,))
        for row in value:
            jsun={}
            jsun['articles_title'] = row.articles_title
            jsun['articles_content'] =row.articles_content
            jsun['articles_users_author']=row.articles_users_author
            jsun['articles_modified']= row.articles_modified
            jsun['articles_url']= row.articles_url
            jsun['articles_comments']= row.articles_comments
            if type(row.articles_tags) != type(None):
                jsun['articles_tags']=list(row.articles_tags)
            else:
                jsun['articles_tags']= 'null'
            json_list.append(jsun)
        return jsonify(json_list),200

    except Exception as er:
        return str(er), 400




#RETRIEVE METADATA FOR THE  N MOST RECENT ARTICLES, INCLUDING TITLE, AUTOR, DATE, AND URL
#This route gets activated the param "count" which allows the user to enter how many article they want. It must be in the body in json
#This route will get the most recent article added to the database
#It will RETURN the whole row with all informtion 
#If an error is occurs a 204 status will be returned not content found else if no error is found it will return a 200 OK 

@app.route('/article', methods=['GET'] )
def getNthArticle():
    json_list =[]
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    data = request.get_json()
    key = data["count"]
    try:
        value =session.execute('''Select articles_title, articles_content, articles_users_author, articles_modified, articles_url From articles  limit %s''',(key,))
        for row in value:
            jsun={}
            jsun['articles_title'] = row.articles_title
            jsun['articles_content'] =row.articles_content
            jsun['articles_users_author']=row.articles_users_author
            jsun['articles_modified']= row.articles_modified
            jsun['articles_url']= row.articles_url
            json_list.append(jsun)

        return jsonify(json_list)

    except Exception as er:
        return str(er), 406



app.run(debug=True) 
