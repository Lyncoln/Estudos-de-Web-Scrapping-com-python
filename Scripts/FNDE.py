# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:53:14 2019

@author: Lyncoln
"""


import scrapy
from scrapy.crawler import CrawlerProcess
import os

localdetrabalho = "C:/Users/Hp/Documents/DIRETORIO DE TRABALHO DO R/FNDE Simas/"
os.chdir(localdetrabalho)

arquivo = open('resultado2018.txt','w')


class pegaExcel(scrapy.Spider):
    name = 'Excel'
   
    parte1 = 'https://www.fnde.gov.br/distribuicaosimadnet/selecionar?numeroEntidade=000000'
    parte2 = '&anoPrograma=2018&codigoPrograma=01&ufSelecionada=RJ&criterios='       
    comutacoes = []
        
    for i in range(0,1000000):
        num = str(i)
        while(len(num)<6):
            num = '0' + num
        comutacoes.append(num)
            
        
    i = 0 
    links = []
        
    for numero in comutacoes :
        links.append(parte1+comutacoes[i]+parte2) 
        i = i+1
            
    start_urls = links
        
    def parse(self, response):
        pag = response.xpath('//*[@id="pesquisar"]/div[4]/a[1]/@href').extract_first()
        if(pag):
            arquivo.write(str(pag)+'\n')
       
      
       
process = CrawlerProcess()
process.crawl(pegaExcel)
process.start()
arquivo.close() 