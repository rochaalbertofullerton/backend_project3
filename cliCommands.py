import click, sqlite3, hashlib, uuid
from flask import Flask
from datetime import datetime, date
from cassandra.cluster import Cluster



app = Flask(__name__)

@app.cli.command()
@click.argument('title')
@click.argument('author')
@click.argument('text')
def postarticle( title, author, text):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    keyurl = '/article/' + title 
    session.execute('''INSERT INTO articles (articles_id, articles_title, articles_content, articles_created , articles_modified, articles_users_author, articles_url) Values(%s,%s,%s,%s,%s,%s,%s ) ''',(uuid.uuid4() ,title, text,datetime.now(),datetime.now(),author,keyurl,))



@app.cli.command()
@click.argument('id')
@click.argument('tag')
@click.argument('article_url')
def posttag( tag, article_url):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    setOfTag = {tag}
    value = session.execute('''Select articles_id, articles_created From articles Where articles_url = %s''',(article_url,))
    session.execute('''Update articles Set articles_tags = articles_tags + %s Where articles_id = %s And articles_created = %s''', (setOfTag, value[0].articles_id, value[0].articles_created,))


@app.cli.command()
@click.argument('content')
@click.argument('article_url')
@click.argument('author')
def postcomment(content, article_url):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    value = session.execute('''select articles_id, articles_created, articles_comments from articles where articles_url=%s''', (article_url,))
    lis=[]
    lis.append(content)
    session.execute('''update articles SET articles_comments = articles_comments + %s where articles_id = %s and articles_created = %s''',(lis,value[0].articles_id,value[0].articles_created,))


@app.cli.command()
@click.argument('name')
@click.argument('email')
@click.argument('password')
def postuser(name , email, password):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect('blog')
    hashedpassword = hashlib.md5(password.encode())
    session.execute('''INSERT INTO users (users_id, users_name, users_password) Values(%s,%s,%s) ''',(email,name, hashedpassword.hexdigest(),))
