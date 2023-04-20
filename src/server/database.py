import sqlite3
import tempfile
import os
from flask import Response

tmpdir = tempfile.gettempdir()
path_db = os.path.join(tmpdir, 'tables.db')

def create_db():
    conn = sqlite3.connect(path_db)
    c = conn.cursor() #create cursor

    # Create table device
    c.execute("""CREATE TABLE IF NOT EXISTS device (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_code text NOT NULL UNIQUE,
        date_time text

    )""")

    # Create table sac_dm
    c.execute("""CREATE TABLE IF NOT EXISTS sac_dm (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value real,
        device_code text NOT NULL,
        date_time text

    )""")

    #id_device INTEGER NOT NULL Chave estrangeira da tabela DEVICE,
    # Create table accelerometer_register
    c.execute("""CREATE TABLE IF NOT EXISTS accelerometer_register (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_code TEXT NOT NULL,
        date_time text,
        ACx float,
        ACy float,
        ACz float

    )""")
    conn.commit()
    conn.close()
          
# Function to insert data into device table
def insert_data_device(data):
    try:
        with sqlite3.connect(path_db) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO device (device_code, date_time) VALUES (?, ?)", data)
            conn.commit()
            return Response(status=200, response="Dados inserido com sucesso!")
    except Exception as e:
        return Response(status=500, response=str(e))
        
# Function to insert data into sac_dm table
def insert_data_sac_dm(data):
    try:
        with sqlite3.connect(path_db) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO sac_dm (value, device_code, date_time) VALUES (?, ?, ?)", data)
            print("Dados inserido com sucesso")
            conn.commit()
            return Response(status=200, response="Dados inserido com sucesso!")
    except Exception as e:
        return Response(status=500, response=str(e))

# Function to insert data into accelerometer_register table
def insert_data_accelerometer_register(data):
    try:
        with sqlite3.connect(path_db) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO accelerometer_register (device_code, date_time, ACx, ACy, ACz) VALUES (?, ?, ?, ?, ?)", data)
            print("Dados inserido com sucesso")
            conn.commit()
            return Response(status=200, response="Dados inseridos com suesso!")
    except Exception as e:
        return Response(status=500, response=str(e))

# Function to get all data from device table
def get_all_data():
    conn = sqlite3.connect(path_db)
    c = conn.cursor()
    c.execute("SELECT * FROM device")
    data = c.fetchall()
    conn.close()
    return data

# Function to get all data from accelerometer_data table
def get_all_accelerometer_data():
    conn = sqlite3.connect(path_db)
    c = conn.cursor()
    c.execute("SELECT * FROM accelerometer_register")
    data = c.fetchall()
    conn.close()
    return data