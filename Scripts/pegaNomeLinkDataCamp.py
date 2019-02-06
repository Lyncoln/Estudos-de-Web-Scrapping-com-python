# -*- coding: utf-8 -*-
from scrapy import Selector
import requests

#Código para pegar nome e links de cursos na plataforma data camp
url = 'https://www.datacamp.com/courses/all'
html = requests.get( url ).content
sel = Selector( text = html )
cursos = sel.css('div.course-block')
print(len(cursos))
nomes = cursos.css('h4.course-block__title::text').extract()
links = cursos.css('a.course-block__link::attr(href)').extract()
for i in range(0,len(links)):
     print(nomes[i]+": ")
     print(links[i]+"\n")

#