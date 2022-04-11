# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 20:42:28 2021

@author: maxma
"""
import scrapy
import json

class SpiderForTable(scrapy.Spider):

    name = "table_spider"
    mas_of_href = []

    f = open("file_of_href.txt")
    for i in f:
        mas_of_href.append(i)

    start_urls = mas_of_href

    def start_requests(self):
        #url = self.mas_of_href[56]
        for url in self.mas_of_href:
            yield scrapy.Request(url, callback=self.parse)
        #yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):

        def get_models(str, word):

          re_mas = []
          index = 0
          count = str.count(word)
          for i in range(count):
            last = str.find(word, index)
            if last != -1:
                first = str.rfind(">", index, last)
                str_for_copy = str[first + 1: last]
                index = last + len(word)
                re_mas.append(str_for_copy)

          return re_mas


        def get_data(str, word):
            re_mas = []
            index = 0
            parametr = ""
            count = str.count(word)
            for i in range(count):
                pre_str = ""
                last = str.find(word, index)
                if last != -1:
                    first = str.rfind(">", index, last)
                    if str[first - 2: first] == "br":
                        pre_first = str.rfind(">", index, first - 3)
                        pre_str = str[pre_first + 1: first - 3]
                    str_for_copy = pre_str + str[first + 1: last]
                    index = last + len(word)
                    re_mas.append(str_for_copy)

            if len(re_mas) > 0:
                parametr = re_mas[0]
                del re_mas[0]
            return parametr, re_mas

        print("11111111111111")

        item = {"Название": {},
                "Модели": {
                    "none": [],
                    "none": []
                },
                "Размеры": {
                    "Длина (м)": [
                        "none",
                        "none"
                    ],
                    "Размах крыла (м)": [
                        "none",
                        "none"
                    ],
                    "Высота (м)": [
                        "none",
                        "none"
                    ],
                    "Площадь крыла (кв.м)": [
                        "none",
                        "none"
                    ]
                },
                "Вес": {
                    "Макс. взлетный вес (кг)": [
                        "none",
                        "none"
                    ],
                    "Макс. посадочный вес (кг)": [
                        "none",
                        "none"
                    ],
                    "Вес пустого (кг)": [
                        "none",
                        "none"
                    ],
                    "Макс. вес без топлива (кг)": [
                        "none",
                        "none"
                    ],
                    "Макс. коммерческая загрузка (кг)": [
                        "none",
                        "none"
                    ],
                    "Емкость топливных баков (л)": [
                        "none",
                        "none"
                    ],
                    "Макс. запас топлива (кг)": [
                        "none",
                        "none"
                    ]
                },
                "Летные данные": {
                    "Макс. дальность полета (км)": [
                        "none",
                        "none"
                    ],
                    "Дальность полета с макс. загрузкой (км)": [
                        "none",
                        "none"
                    ],
                    "Макс. крейсерская скорость (км/ч)": [
                        "none",
                        "none"
                    ],
                    "Максимальная скорость (км/ч)": [
                        "none",
                        "none"
                    ],
                    "Потолок (макс. высота полета) (м)": [
                        "none",
                        "none"
                    ],
                    "Длина разбега (м)": [
                        "none",
                        "none"
                    ],
                    "Длина пробега (м)": [
                        "none",
                        "none"
                    ],
                    "Двигатели": [
                        "none",
                        "none"
                    ],
                    "Удельный расход топлива (г/пасс.-км)": [
                        "none",
                        "none"
                    ],
                    "Часовой расход топлива (кг)": [
                        "none",
                        "none"
                    ]
                },
                "Пассажирский салон": {
                    "Кол-во кресел (эконом)": [
                        "none",
                        "none"
                    ],
                    "Кол-во кресел (эконом/ бизнес)": [
                        "none",
                        "none"
                    ],
                    "Кол-во кресел (эконом/ бизнес/ первый)": [
                        "none",
                        "none"
                    ],
                    "Шаг кресел эконом класса (см)": [
                        "none",
                        "none"
                    ],
                    "Длина салона (м)": [
                        "none",
                        "none"
                    ],
                    "Ширина салона (м)": [
                        "none",
                        "none"
                    ],
                    "Высота салона (м)": [
                        "none",
                        "none"
                    ],
                    "Ширина прохода (м)": [
                        "none",
                        "none"
                    ],
                    "Ширина кресла эконом (м)": [
                        "none",
                        "none"
                    ]
                }
                }


        zapros_for_data = "//tr"

        table = response.xpath(zapros_for_data).extract()

        key_word = "</strong>"
        count = table[3].count(key_word)
        mas_of_data = []
        for i in range(count):
            mas_of_data.append("none")
        for i in item:
            for j in item[i]:
                item[i][j] = mas_of_data
        auto = get_models(table[3], key_word)

        zapros_for_name = '//h1'
        name = response.xpath(zapros_for_name).extract()
        first = name[0].find(">")
        last = name[0].rfind("<")
        item["Название"] = name[0][first + 1:last]

        item["Модели"] = auto


        list_of_headers = response.xpath("//h4/text()").extract()
        list_of_headers = list_of_headers[0: len(list_of_headers) - 3]

        k = 0
        for i in table[5: len(table)]:
            key_word = "</td>"
            parametr, auto = get_data(i, key_word)
            for j in range(len(auto)):
                if auto[j] == "":
                    auto[j] = "none"
            if len(auto) == 0:
                k = k + 1
            else:
                if len(parametr) > 4:
                    item[list_of_headers[k]][parametr] = auto


        #print(item)
        for j in range(len(item["Название"])):
            if item["Название"][j] == "/":
                str = item["Название"][:j] + "_" + item["Название"][j + 1:]
                item["Название"] = str
        with open(item["Название"] + ".json", "w", encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=1)


