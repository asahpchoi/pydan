import sqlite3

def initUW(title, content):
    connection = sqlite3.connect("db/uw.db")
    cursor = connection.cursor() 
    cursor.execute(f"insert into uw values (\"{title}\", \"{content}\")")
    #cursor.execute("create table uw (title TEXT, content TEXT)")
    connection.commit()    



def getall():
    connection = sqlite3.connect("db/ocr.db")

    cursor = connection.cursor()
    rows = cursor.execute("select extraction from ocr").fetchall()
    srows = map(str, rows)
    return "\n".join(srows)
 
def getallrows():
    connection = sqlite3.connect("db/ocr.db")

    cursor = connection.cursor()
    rows = cursor.execute("select extraction from ocr").fetchall()
    return rows

def log(filepath:str, filename: str, extraction :str):
    print(filename, extraction)
    connection = sqlite3.connect("db/ocr.db")
    cur = connection.cursor()
    
    cur.execute(f"insert into ocr values ('{filepath}:{filename.replace("'", "")}', '{extraction.replace("'", "")}')")
    #cur.execute("create table ocr (filename TEXT, extraction TEXT)")
    connection.commit()

def clear():
    connection = sqlite3.connect("db/ocr.db")
    cur = connection.cursor()
    cur.execute("delete from ocr")
    connection.commit()

 