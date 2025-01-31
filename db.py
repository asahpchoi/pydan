import sqlite3

def test():
    connection = sqlite3.connect("aquarium.db")

    cursor = connection.cursor()
    #cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
    cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
    cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")
    rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
    print(rows)
    connection.commit()

def log(filepath:str, filename: str, extraction :str):
    print(filename, extraction)
    connection = sqlite3.connect("ocr.db")
    cur = connection.cursor()
    
    cur.execute(f"insert into ocr values ('{filepath}:{filename.replace("'", "")}', '{extraction.replace("'", "")}')")
    #cur.execute("create table ocr (filename TEXT, extraction TEXT)")
    connection.commit()

def clear():
    connection = sqlite3.connect("ocr.db")
    cur = connection.cursor()
    cur.execute("delete from ocr")
    connection.commit()

 