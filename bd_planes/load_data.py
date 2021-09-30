# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 21:55:45 2021

@author: maxma
"""

import json
import os
import psycopg2

#замечание: если ту, як, и так далее, то брать только последние буквы
#но это к краулерам

os.chdir ('c:/users/maxma/documents/bd_project/bd_planes/files/input')
datas = os.listdir()
path_out = 'c:/users/maxma/documents/bd_project/bd_planes/files/output/'

def func_kai():
    datas = os.listdir()
   # print(datas)
    j = 1 #порядковый номер записи габаритов 
    int(j)
    for i in datas:
        #открывает файлы в директории
       # print (j)
        with open(i, mode = 'r', encoding = 'utf-8') as f:
            nnn = json.load(f)    
       # itog = form_select(nnn, j)
      #  num_planes = len(itog)
       # print(itog)
      #  print(num_planes)
      #  for k in itog:
      #      improved(k)
      #      imp2(k)
       # j = j + num_planes
    return (nnn)  
        
def improved (mass):
    conn = psycopg2.connect(
         database="BD_Planes", 
         user='postgres', 
         password='Littorio', 
         host='localhost'
         )
     #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor() 
    zarpos_size = mass[1]
    cursor.execute(zarpos_size)
    
def imp2 (mass):
    conn = psycopg2.connect(
         database="BD_Planes", 
         user='postgres', 
         password='Littorio', 
         host='localhost'
         )
     #Setting auto commit false
    conn.autocommit = True

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor() 
    zarpos_model = mass[0] 
    cursor.execute(zarpos_model)
    # Preparing SQL queries to INSERT a record into the database.
   # Closing the connection
    conn.close()       


    
def form_select (inp_file, num):
    #формирует запрос
    #на вход получает .json файл
    #производит скрипт
   # print (num)
    code_error = 0
    counter = 0
    link = []
    plane_name = []
    plane_country = []
    plane_scheme = []
    plane_enj_num = []
    plane_enj_name = []
    plane_pass = []
    plane_loadout = []
    plane_length = []
    plane_ws = []
    plane_m_e = []
    plane_m_f = []
    for i in inp_file['Модели']:
        plane_name1 = str(inp_file['Название']) + ' ' + str(inp_file['Модели'][counter])#шьем имя
        plane_name.insert(counter, plane_name1) #шьем имя; если русские, то только букву
       #  print(plane_name[counter])
        plane_country.insert(counter, 'Неизвестно')
        plane_scheme.insert(counter, 'Моноплан') #де-факто, заглушка - придется самостоятельно заполнять
        enj = inp_file['Летные данные']['Двигатели']
        #правил тут
        if (enj[counter] == 'none' and counter == 0):
            plane_enj_num.insert(counter, 2)
            plane_enj_name = 'Неизвестно'
          #  print ('error 1')
            code_error = 1
        elif (enj[counter] == 'none' and counter > 0):
            if code_error == 1:
                plane_enj_num.insert(counter, 2)
                plane_enj_name = 'Неизвестно'
            else: 
                plane_enj_num.insert(0, plane_enj_num[0])
                plane_enj_name.insert(0, plane_enj_name[0])
              #  print ('error 2')
        else:
            enj_comma_pos = enj[counter].find(',', 0, len(enj[counter]))
            plane_enj_num.insert(counter, int(enj[counter][enj_comma_pos+2:enj_comma_pos+3]))
            plane_enj_name.insert(counter, enj[counter][:enj_comma_pos] )
           # print ('enj ok')
        salon = inp_file['Пассажирский салон']['Кол-во кресел (эконом)']
        if counter == 0:
          if salon[counter] == 'none':
                salon = inp_file['Пассажирский салон']['Кол-во кресел (эконом/ бизнес)']
                if salon[counter] == 'none':
                    salon = inp_file['Пассажирский салон']['Кол-во кресел (эконом/ бизнес/ первый)']
                    if salon[counter] == 'none':
                        salon = 100
        if counter > 0:
             if salon[counter] == 'none':
                salon = inp_file['Пассажирский салон']['Кол-во кресел (эконом/ бизнес)']
                if salon[counter] == 'none':
                    salon = inp_file['Пассажирский салон']['Кол-во кресел (эконом/ бизнес/ первый)']
                    if salon[counter] == 'none':
                        salon = 100
        salon_tire_pos = salon[counter].find('-', 0, len(salon[counter]))
      #  print (salon)
        if salon_tire_pos == -1:
            plane_pass.insert(counter, int(salon[counter]))
        else:
            plane_pass.insert(counter, int(salon[counter][salon_tire_pos+1:len(salon[counter])]))
        loadout = inp_file['Вес']['Макс. коммерческая загрузка (кг)']
        if loadout[counter] == 'none':
            plane_loadout.insert(counter, 'NULL')
        else:
            plane_loadout1 = cut_tire(loadout[counter])
            plane_loadout.insert(counter, round(float(cut_spare(plane_loadout1)), 1))
        length = inp_file['Размеры']['Длина (м)'] 
        plane_length.insert(counter, round(float(length[counter]), 1))
        wings_spread = inp_file['Размеры']['Размах крыла (м)'] 
        plane_ws1 = cut_tire(wings_spread[counter])
        plane_ws.insert(counter, round(float(cut_spare(plane_ws1)), 1))
        mass_empty = inp_file['Вес']['Вес пустого (кг)']
        if mass_empty[counter] == 'none':
            plane_m_e.insert(counter, 'NULL')
        else:   
            plane_m_e1 = cut_tire(mass_empty[counter])
            plane_m_e.insert(counter, round(float(cut_spare(plane_m_e1)), 1))
        mass_full = inp_file['Вес']['Макс. взлетный вес (кг)']
        if mass_full[counter] == 'none':
            plane_m_f.insert(counter, 'NULL')
        else:
            plane_m_f_1 = cut_tire(mass_full[counter])
            plane_m_f.insert(counter, round(float(cut_spare(plane_m_f_1)), 1))
        if counter>0:
            if (mass_full [counter] == mass_full [0] 
                and mass_empty[counter] == mass_empty[0] 
                and mass_empty[counter] == mass_empty[0]
                and wings_spread[counter] == wings_spread[0]
                and length[counter] == length[0]):
                link.insert(counter, num)
            else:
                 link.insert(counter, num + counter);    
        else: 
            link.insert(counter, num)
        counter = counter + 1  
    
    vyvod = [] #состоит из нескольких list_plane
    list_plane = []# plane
    counter = 0            
    for i in inp_file['Модели']:            
        path_scr = path_out + 'scr' + str(num + counter) + '.sql'
        out_file = open(path_scr, 'w')
        str_sql1 = "INSERT INTO models (models_Name, models_scheme_model, models_engines_number, models_engines_name, models_loadout, models_pass, models_size)  VALUES ('"
        str_sql1 = str_sql1 + plane_name[counter] + "', '"
        str_sql1 = str_sql1 + plane_scheme[counter] + "', "
        str_sql1 = str_sql1 + str(plane_enj_num[counter]) + ", '"
        str_sql1 = str_sql1 + plane_enj_name[counter] + "', "
        str_sql1 = str_sql1 + str(plane_loadout[counter]) + ", "
        str_sql1 = str_sql1 + str(plane_pass[counter]) + ", "
        str_sql1 = str_sql1 + str(link[counter]) + ");"
        str_sql2 = "INSERT INTO sizes (sizes_length, sizes_wings_spread, sizes_mass_empty, sizes_mass_full)  VALUES ("
        str_sql2 = str_sql2 + str(plane_length[counter]) + ", "
        str_sql2 = str_sql2 + str(plane_ws[counter]) + ", "
        str_sql2 = str_sql2 + str(plane_m_e[counter]) + ", "
        str_sql2 = str_sql2 + str(plane_m_f[counter]) + ");"
        str_sql = str_sql2 + str_sql1
        out_file.write(str_sql)
        out_file.close() 
       # print (i)
        list_plane.insert(0, str_sql1)
        list_plane.insert(1, str_sql2)
       # print (list_plane)
        vyvod.append(list_plane)
       # print (counter)
        counter = counter + 1
        list_plane = []
    
   
   # print (vyvod)
    return(vyvod)


def cut_spare (string):
   spare_pos = string.find(' ', 0, len(string))
   if not (spare_pos == -1):
       string_new = string[0:spare_pos] 
       string_new = string_new + string[spare_pos + 1:len(string)] 
    #   print (string_new)
       return (string_new)
   else: 
       return (string)

def cut_tire (string):
   spare_pos = string.find('-', 0, len(string))
   if not (spare_pos == -1):
       string_new = string[0:spare_pos-1]
       return (string_new)
   else: 
       return (string)
   

ass = func_kai() 
print (ass)
