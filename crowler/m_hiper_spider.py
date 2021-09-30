# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 20:41:30 2021

@author: maxma
"""
import scrapy


class SpiderForHref(scrapy.Spider):
    name = "hiper_spider"
    start_urls = ["https://www.airlines-inform.ru/commercial-aircraft/"]

    def parse(self, response, **kwargs):
        text_of_order = "//li"
        table = response.xpath(text_of_order).extract()
        result_mas_of_href = []
        mas_of_planes = []
        for i in table:
           k = i.find("commercial-aircraft")
           if k != -1:
               mas_of_planes.append(i)
        mas_of_planes = mas_of_planes[28:len(mas_of_planes)]
        for i in mas_of_planes:
            first = i.find('https')
            last = i.rfind('html')
            result_mas_of_href.append(i[first:last+4])
        for i in result_mas_of_href:
            print(i)
        with open("file_of_href.txt", "w") as f:
            for i in result_mas_of_href:
                f.write(i + '\n')
            f.close()


