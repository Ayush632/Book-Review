import sqlite3
import pandas as pd
import os

class readCSVintoDB():
    def importCSVintoDB(self):
        csvfile = "./books.csv"
        df = pd.read_csv(csvfile,sep=',')
        dp = (df[['isbn','title','author','year']])
        print(dp)
        myConn = sqlite3.connect('boo.sqlite')
        dbCursor = myConn.cursor()
        dbCreateTable = '''CREATE TABLE IF NOT EXISTS books 
                               ( 
                                  isbn varchar(256),
                                   title varchar,
                                   author_id integer,
                                   year integer);
                            CREATE TABLE IF NOT EXSISTS Authors
                            (
                                author_id  integer PRIMARY KEY AUTOINCREMENT UNIQUE
                                name varchar
                            )
                                 '''

        dbCursor.execute('''CREATE TABLE IF NOT EXISTS books 
                               ( 
                                  isbn varchar(256),
                                   title varchar,
                                   author_id integer,
                                   year integer)''')
        dbCursor.execute('''CREATE TABLE IF NOT EXISTS Authors
                            (
                                author_id  integer PRIMARY KEY AUTOINCREMENT UNIQUE,
                                name varchar UNIQUE
                            )
                                 ''')
        myConn.commit()
        print(type(dp['author'][0]))
        for i in range(0,5000):
            dbCursor.execute(''' INSERT OR IGNORE INTO Authors(name) VALUES (?) ''',(dp['author'][i],))
        myConn.commit()
        for i in range(0,5000):
            dbCursor.execute(''' INSERT INTO books(isbn,title,author_id,year) VALUES (?,?,(SELECT author_id FROM Authors WHERE name=(?)),?)''',(dp['isbn'][i],dp['title'][i],dp['author'][i],dp['year'][i],))
        myConn.commit()
test1 = readCSVintoDB()
test1.importCSVintoDB()
                    


