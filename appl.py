import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask,render_template,request
import requests
import sqlite3

app=Flask(__name__)

@app.route("/")
def index():
    return render_template('login.html')
@app.route("/sign_up")
def sign():
    return render_template('sign.html')
@app.route("/bo",methods=["POST"])
def bo():
  isbn=request.form.get("isbn")
  res=requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "GjzEgv35UVfhHuX56aOg", "isbns":isbn})
  print(type(res))
  if(res is None):
    return render_template('search.html')
  else:
    return render_template('reult.html',o=res.json())
@app.route("/rev",methods=["POST"])
def rev():
  rev=request.form.get("review")
  f=open("reviews.txt","a+")
  f.write(rev)
  f.close()
  return render_template('login.html')
@app.route("/tit",methods=["POST"])
def tit():
  conn=sqlite3.connect('boo.sqlite')
  cur=conn.cursor()
  tit=request.form.get("title")
  cur.execute('''SELECT isbn FROM books WHERE title = ? ''',(tit,))
  otit=cur.fetchone()
  conn.commit()
  if(otit is None):
    return render_template('search.html')
  else:
    isbn=otit[0]
    res=requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "GjzEgv35UVfhHuX56aOg", "isbns":isbn})
    return render_template('reult.html',o=res.json(),t=tit)
@app.route("/author",methods=["POST"])
def auth():
  conn=sqlite3.connect('boo.sqlite')
  cur=conn.cursor()
  author=request.form.get("author")
  cur.execute('''SELECT title,isbn FROM books WHERE author_id= (SELECT author_id FROM Authors WHERE name = ?)''',(author,) )
  oauth=cur.fetchall()
  conn.commit()
  if(oauth is None):
    return render_template('search.html')
  else:
    print(type(oauth))
    return render_template("aut.html",b=oauth,t=author)    
@app.route("/check",methods=["POST"])
def check():
  conn=sqlite3.connect('boo.sqlite')
  cur=conn.cursor()
  name=request.form.get("user_name")
  #print(type(name))
  passw=request.form.get("password")
  cur.execute(''' SELECT passwo FROM Users WHERE name= ? ''',(name,))
  opass=cur.fetchone()
  if(opass is None):
    return render_template('login.html')
  conn.commit()
  if(opass[0] == passw):
    return render_template('search.html')
  else:
    return render_template('login.html')
@app.route("/buf",methods=["GET","POST"])
def buf():
  return render_template("search.html")
@app.route("/one",methods=["GET","POST"])
def fist():
    conne=sqlite3.connect('boo.sqlite')
    cure=conne.cursor()
    name=request.form.get("user_name")
    passw=request.form.get("password")
   # print(name,passw)
    cure.execute('''SELECT name FROM Users WHERE name= ? ''',(name,))
    names=cure.fetchall()
    conne.commit()
   # print(names)
    for n in names:
      print(n)
      print(name)
      if(n[0] == name):
        return render_template('login.html')
    print(" new user ")
    connec=sqlite3.connect('boo.sqlite')
    curs=connec.cursor()
    curs.execute(''' INSERT INTO Users(name,passwo) VALUES (?,?)''',(name,passw))
    connec.commit()
    return render_template("search.html")

