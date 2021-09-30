# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:46:10 2021

@author: maxma
"""
import json
import psycopg2
import connection as conect

#conn = psycopg2.connect()
#cur = conn.cursor()

def get_vendors_name (name_plane):
    
    conn = None
    try:
        params = conect.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        zapros = "select mods.models_id, mods.models_name, mods.models_engines_name, mods.models_pass, szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full from models mods, sizes szs where mods.models_size = szs.sizes_id and mods.models_name = '" + name_plane + "';"
        cur.execute(zapros)
       # print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
        i = 0
        finalObj = {}
        while row is not None: #тут все сканируется
            js = tuple_to_json (row)
            finalObj[i] = js
            i = i + 1
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return (finalObj)


def get_vendors_be_like (name_plane):
    
    conn = None
    try:
        params = conect.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        zapros = "select mods.models_id, mods.models_name, mods.models_engines_name, mods.models_pass, szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full from models mods, sizes szs where mods.models_size = szs.sizes_id and mods.models_name like '" + name_plane + "';"
        cur.execute(zapros)
       # print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
        i = 0
        finalObj = {}
        while row is not None: #тут все сканируется
           # print(row)
            js = tuple_to_json (row)
           # print (js)
            finalObj[i] = js
            i = i + 1
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return (finalObj)



def get_vendors():
    """ query data from the vendors table """
    conn = None
    try:
        params = conect.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        zapros = "select mods.models_id, mods.models_name, mods.models_engines_name, mods.models_pass, szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full from models mods, sizes szs where mods.models_size = szs.sizes_id;"
        cur.execute(zapros)
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
        i = 0
        finalObj = {}
        while row is not None: #тут все сканируется
            js = tuple_to_json (row)
            finalObj[i] = js
            i = i + 1 
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return (finalObj)



def get_vendors_kai():
    """ query data from the vendors table """
    conn = None
    try:
        params = conect.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        zapros = "select mods.models_id, mods.models_name, mods.models_engines_name, mods.models_pass, szs.sizes_length, szs.sizes_wings_spread, szs.sizes_mass_full from models mods, sizes szs where mods.models_size = szs.sizes_id;"
        cur.execute(zapros)
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()
        i = 0
        finalObj = {}
        while row is not None: #тут все сканируется
            js = tuple_to_json (row)
            finalObj[i] = js
            i = i + 1 
            row = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return (finalObj)





def tuple_to_json (tuple_row):
    dict_prep = {"Name": '', "Engines name": '', "Passenger capacity": 0, "Hull length": 0, "Wings spread": 0, "Full mass": 0}
    dict_prep ["Name"] = tuple_row [1]
    dict_prep ["Engines name"] = tuple_row [2]
    dict_prep ["Passenger capacity"] = str(tuple_row [3])
    dict_prep ["Hull length"] = str(tuple_row [4])
    dict_prep ["Wings spread"] = str(tuple_row [5])
    dict_prep ["Full mass"] = str(tuple_row [6])
  #  print (dict_prep)
    js_file = json.dumps(dict_prep, indent = 4).decode('unicode-escape').encode('utf8')
    
    return js_file
   # print('ok')
  # path_file = 'c:/users/maxma/documents/bd_project/bd_planes/files/zapros/' + dict_prep['Name'] + '.json'
  #  fle = open(path_file, 'w')  
  #  fle.write(js_file)
  #  fle.close
#oooo = get_vendors_name('Focke-Wulf Fw.200C Condor C-3/U-4') 
#oooo = get_vendors_be_like('%Boeing%') 
oooo = get_vendors() 
print (oooo)
print (type(oooo))
    