from calendar import WEDNESDAY
from random import choice
import app.MongoFunctions
from app.MongoFunctions import *
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import psycopg2
from psycopg2 import Error
from jinja2 import Template
from json2html import *
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange
from flask_bootstrap import Bootstrap

user="postgres"
password="YUV45G"
host="80.249.150.39"
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
    if tuple_row[2] == None:
        dict_prep["Engines name"] = "tuple_row[2]"
    else:
        dict_prep["Engines name"] = tuple_row[2]
    dict_prep["Passenger capacity"] = str(tuple_row[3])
    dict_prep["Hull length"] = str(tuple_row[4])
    dict_prep["Wings spread"] = str(tuple_row[5])
    dict_prep["Full mass"] = str(tuple_row[6])
    js_file = json.dumps(dict_prep, indent = 4, ensure_ascii = 'true')
    return js_file

def tuple_to_json_for_planes(tuple_row):
    dict_prep = {"Name": '', "Engines name": '', "Models engines number": '',  "Models loadout": 0, "Models passanger capacity": 0}
    dict_prep["Name"] = tuple_row[1]
    dict_prep["Engines name"] = tuple_row[5]
    dict_prep["Models engines number"] = str(tuple_row[4])
    if tuple_row[6] == None:
        dict_prep["Models loadout"] = "No data"
    else:
        dict_prep["Models loadout"] = str(tuple_row[7])
    dict_prep["Models passanger capacity"] = str(tuple_row[8])
    js_file = json.dumps(dict_prep, indent = 4, ensure_ascii = 'true')
    return js_file

def tuple_to_json_for_emissions(tuple_row):
    dict_prep = {"Plane": '', "distance": 0, "fuel_value": 0, "useful waeght": 0, "emissions": 0, "emissions per hundred km": 0, "emissions passenger per 100 km": 0}
    dict_prep["Plane"] = tuple_row[0]
    dict_prep["distance"] = str(tuple_row[1])
    dict_prep["fuel_value"] = str(tuple_row[2])
    dict_prep["useful waeght"] = str(tuple_row[3])
    dict_prep["emissions"] = str(tuple_row[4])
    dict_prep["emissions per hundred km"] = str(tuple_row[5])
    dict_prep["emissions passenger per 100 km"] = str(tuple_row[6])
    js_file = json.dumps(dict_prep, indent = 4, ensure_ascii = 'true')
    return js_file

def to_json(cur, index):
    row = cur.fetchone()
    i = 0
    finalObj = {}
    while row is not None: #тут все сканируется
        if index == 1:
            js = tuple_to_json(row)
        if index == 2:
            js = tuple_to_json_for_planes(row)
        if index == 3:
            js = tuple_to_json_for_emissions(row)
        finalObj[i] = js
        i = i + 1
        row = cur.fetchone()
    return (finalObj)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HIDABbfuihebfwhbfuhfb0987'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/interactive_map/*": {"origins": "*", "supports_credentials": True}})
app.url_map.strict_slashes = False
Bootstrap(app)

# здесь начинается API переклбчения между страницами сайта

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

# здесь начинается API к MongoDB

@app.route("/interactive_map/get_all/", methods=['GET'])
@cross_origin(supports_credentials=True)
def get_all():
    if request.method == 'GET':
        res = stat(open_json(0))
        return jsonify(res)

@app.route("/interactive_map/get_by_date/", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def get_by_date_api():
    if request.method == 'GET':
        return jsonify(open_json(0));
    if request.method == 'POST':
        content = request.get_json();
        res = stat(get_by_date(content));
        print(content);
        return jsonify(res);

@app.route("/interactive_map/airoports/", methods=['GET'])
@cross_origin(supports_credentials=True)
def airports():
    if request.method == 'GET':
        return jsonify(list_airoports())

@app.route("/interactive_map/filter_air/", methods=['POST'])
@cross_origin(supports_credentials=True)
def filter_air():
    if request.method == 'POST':
        air_list = request.get_json()
        print(air_list)
        data = open_json(0)
        res =stat(filter_air_local(data, air_list))
        print(res)
        return jsonify(res)

@app.route("/interactive_map/filter_air_by_date/", methods=['POST'])
@cross_origin(supports_credentials=True)
def filter_air_by_date():
    if request.method == 'POST':
        print(request.get_json())
        data = get_by_date(request.get_json()[0])
        air_list = request.get_json()[1]
        res = stat(filter_air_local(data, air_list))
        print(request.get_json())
        return jsonify(res)

@app.route("/interactive_map/filter_area_get_by_date/", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def filter_area_get_by_date():
    if request.method == 'POST':
        date = request.get_json()[0]
        by_date = get_by_date(date)
        xy = request.get_json()[1]
        res = stat(filter_area_local(by_date, xy))
        return jsonify(res)

@app.route("/interactive_map/filter_area_filter_air/", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def filter_area_filter_air():
    if request.method == 'POST':
        air_list = request.get_json()[0]
        data = open_json(0)
        print(request.get_json())
        filt_air = filter_area_local(data, air_list)
        xy = request.get_json()[1]
        res = stat(filter_area_local(filt_air, xy))
        return jsonify(res)

@app.route("/interactive_map/filter_area_filter_air_by_date/", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def filter_area_filter_air_by_date():
    if request.method == 'POST':
        air_list = request.get_json()[1]
        xy = request.get_json()[2]
        date = request.get_json()[0]
        by_date = get_by_date(date)
        print(request.get_json())
        filt_air = filter_air_local(by_date, air_list)
        res = stat(filter_area_local(filt_air, xy))
        return jsonify(res)

# формирование отчета по базе данных

@app.route('/test2/')
def test2():
    return render_template('test2.html')

# калькулятор выбросов

class Caclculator(FlaskForm):
    f = open('CO9.json')
    data = json.load(f)
    data = data["planes"]
    choice_list = []
    for key in data[0]:
        choice_list.append(key)
    plane_model = SelectField('Модель самолета', choices=choice_list, validators=[InputRequired()])
    plane_age = IntegerField('Срок эксплуатации транспартного средства [лет]', validators=[InputRequired()])
    monday = BooleanField('Пн')
    tuesday = BooleanField('Вт')
    wednesday = BooleanField('Ср')
    thersday = BooleanField('Чт')
    friday = BooleanField('Пт')
    saturday = BooleanField('Сб')
    sunday = BooleanField('Вс')
    all_days = BooleanField('Все')
    avarage_distance = IntegerField('Средняя дистанция полета [км]', validators=[InputRequired()])
    k = IntegerField('Коэффициент занятости пассажирокресел [%]', \
        validators=[InputRequired(), NumberRange(min=0, max=100, message="Введите в процентах")])
    avarage_cost_fuel = IntegerField('Средняя стоимость керосина [руб]', validators=[InputRequired()])
    avarage_cost_ticket = IntegerField('Средняя стоимость билета [руб]', validators=[InputRequired()])

@app.route('/calculator/')
def calculator():
    form = Caclculator()
    return render_template('calculator.html', form=form)

@app.route('/calculator/', methods=['POST'])
def work():
    form = Caclculator()
    items = []
    if form.validate_on_submit():
        if(form.monday.data == False and form.tuesday.data == False and form.wednesday.data == False and \
           form.thersday.data == False and form.friday.data == False and form.saturday.data == False and form.sunday.data == False):
            return render_template('calculator.html', form=form)
        else:
            items.append(form.plane_model.data)
            return render_template('calculator.html', form=form)

@app.route('/calculator/<plane>')
def work_plane(plane):
    no_space_plane = plane.replace("_", " ")
    f = open('CO9.json')
    data = json.load(f)
    plane_inf = data["planes"][0][no_space_plane]
    return jsonify({plane : plane_inf})

# здесь начниется API к PostgreSQL

@app.route('/aviation_statistics/', methods=['POST'])
def justdoit():
    index = request.form['index']
    if index == "Airbus":
        postgreSQL_select_Query = "Select * from models where models_name LIKE 'Airbus%'"
        return aviation_statistics(kwargs=postgreSQL_select_Query)
    if index == "Boeing":
        postgreSQL_select_Query = "Select * from models where models_name LIKE 'Boeing%'"
        return aviation_statistics(kwargs=postgreSQL_select_Query)
    if index == "ALL":
        postgreSQL_select_Query = "select mods.models_id, mods.models_name, mods.models_engines_name, \
                                   mods.models_pass, szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full \
                                   from models mods, sizes szs where mods.models_size = szs.sizes_id;"
        return aviation_statistics(kwargs=postgreSQL_select_Query)
    if index == "Антонов":
        postgreSQL_select_Query = "Select * from models where models_name LIKE 'Антонов%'"
        return aviation_statistics(kwargs=postgreSQL_select_Query)
    if index == "Сухой":
        postgreSQL_select_Query = "Select * from models where models_name LIKE 'Сухой%'"
        return aviation_statistics(kwargs=postgreSQL_select_Query)
    if index == "Выбросы":
        postgreSQL_select_Query = "select * from emissions"
        return aviation_statistics(kwargs=postgreSQL_select_Query)

@app.route('/aviation_statistics/')
def aviation_statistics(**kwargs):
    global connection
    db_connect()
    cursor = connection.cursor()
    index = 0
    if not kwargs or kwargs['kwargs'] ==  "select mods.models_id, mods.models_name, mods.models_engines_name, mods.models_pass, szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full from models mods, sizes szs where mods.models_size = szs.sizes_id;":
        postgreSQL_select_Query = "select mods.models_id, mods.models_name, mods.models_engines_name, mods.models_pass, szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full from models mods, sizes szs where mods.models_size = szs.sizes_id;"
        index = 1
    elif 'emissions' in kwargs['kwargs']:
        postgreSQL_select_Query = kwargs['kwargs']
        index = 3
    else:
        postgreSQL_select_Query = kwargs['kwargs']
        index = 2
    cursor.execute(postgreSQL_select_Query)
    models = to_json(cursor, index)
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
    app.run(debug=True)
    