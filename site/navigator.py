from flask import Flask, render_template
import psycopg2
from psycopg2 import Error
from jinja2 import Template
from json2html import *
import json

user="postgres"
password="конфеденциально :) "
host="192.168.191.13"
port="5432"
database="BD_Planes"
flag = False
connecton = None

def db_connect():
    global connection
    if flag is False:
        try:
            connection = psycopg2.connect(user=user,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)
            print("Соединение с PostgreSQL открыто")
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

def db_disconnect():
    global connection
    if connection:
        connection.close()
        print("Соединение с PostgreSQL закрыто")

def tuple_to_json (tuple_row):
    dict_prep = {"Name": '', "Engines name": '', "Passenger capacity": 0, "Hull length": 0, "Wings spread": 0, "Full mass": 0}
    dict_prep["Name"] = tuple_row[1]
    dict_prep["Engines name"] = tuple_row[2]
    dict_prep["Passenger capacity"] = str(tuple_row[3])
    dict_prep["Hull length"] = str(tuple_row[4])
    dict_prep["Wings spread"] = str(tuple_row[5])
    dict_prep["Full mass"] = str(tuple_row[6])
    js_file = json.dumps(dict_prep, indent = 4, ensure_ascii = 'true')
    return js_file

def to_json(cur):
    row = cur.fetchone()
    i = 0
    finalObj = {}
    while row is not None: #тут все сканируется
        js = tuple_to_json(row)
        finalObj[i] = js
        i = i + 1
        row = cur.fetchone()
    return (finalObj)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/main/')
def main():
    return render_template('main.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/interactive_map/')
def interactive_map():
    return render_template('interactive_map.html')

@app.route('/aviation_statistics/')
def aviation_statistics():
    global connection
    db_connect()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select mods.models_id, mods.models_name, mods.models_engines_name, mods.models_pass, szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full from models mods, sizes szs where mods.models_size = szs.sizes_id;"
    cursor.execute(postgreSQL_select_Query)
    models = to_json(cursor)
    db_disconnect() 
    arr = []
    for k, v in models.items():
        arr.append(v)
    for idx, val in enumerate(arr):
        arr[idx] = eval(val)
    models = json2html.convert(json = arr)
    models = models.replace('border="1"', 'class="styled-table"')
    return render_template('aviation_statistics.html', json_obj = models)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

#. venv/bin/activate
#python3 navigator.py
