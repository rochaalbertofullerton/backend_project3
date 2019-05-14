import flask,requests
from datetime import datetime, date
from flask import request , jsonify
from flask import Response
from feedgen.feed import FeedGenerator

app = flask.Flask(__name__)

@app.route('/summary', methods=['GET'])
def getsummary():
    req= requests.get('http://localhost/article',json={"count" : 10} , auth=('admin@email.com', 'adminpassword'))
    value = req.json()
    
    
   
    fg = FeedGenerator()
    fg.title('Summary of 10 newest articles')
    fg.link( href='http://localhost/feed/summary' )
    fg.subtitle('This is a cool feed!')
    fg.language('en')


    for x in value:
        fe = fg.add_entry()
        fe.title(x.get('articles_title',''))
        fe.category(term= "Author "+ x.get('articles_users_author',''))
        fe.category(term= "Date "+ x.get('articles_modified', ''))
        fe.link(href="http://localhost"+x.get('articles_url',''))
  
    fg.rss_file('summary_10.xml')
 
    
    return "RSS FILE CREATED summary_10.xml", 200

@app.route('/summary/content', methods=['GET'])
def getcontent():
    req= requests.get('http://localhost/article/content',json={"count" : 10} , auth=('admin@email.com', 'adminpassword'))
    value = req.json()
    fg = FeedGenerator()
    fg.title('A full feed')
    fg.link( href='http://localhost/feed/summary/content' )
    fg.subtitle('This is a cool feed!')
    fg.language('en')
    
    for x in value:
        fe = fg.add_entry()
        fe.content(x.get('articles_content',''))
        if x.get('articles_tags','') != 'null':
            for v in x.get('articles_tags',''):
                fe.category(term= 'Tag: '+ v)
        else:
            fe.category(term= 'Tag: None')
        if type(x.get('articles_comments','')) == type(None):
            count = '0'
        else:
            count = str(len(x.get('articles_comments','')))
        fe.category(term = 'Comment Count: '+ count)
      
    fg.rss_file('content.xml')
    return "YOUR CONTENT WAS CREATED content.xml", 200

@app.route('/summary/comments', methods=['GET'])
def getcomments():
    req= requests.get('http://localhost/article',json={"count" : 10} , auth=('admin@email.com', 'adminpassword'))
    value = req.json()
    fg = FeedGenerator()
    fg.title('A full feed')
    fg.link( href='http://localhost/feed/summary/comments' )
    fg.subtitle('This is a cool feed!')
    fg.language('en')
   
    for x in value:
        split = x.get('articles_url','').split('/')
        reqcomment=requests.get('http://localhost/comment/get/'+split[2],json={"count" : 30} , auth=('admin@email.com', 'adminpassword'))
        fe = fg.add_entry()
        fe.content(x.get('articles_url', ''))
        if reqcomment.status_code == 200:
            for v in reqcomment.json():
                fe.category(term= v)
        else:
            fe.category(term="None")

    fg.rss_file('comments.xml')
    return "YOUR COMMENTS WAS CREATED comments.xml", 200

app.run()
  