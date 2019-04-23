# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:06:20 2019

@author: Lyncoln
"""

import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import time

class receita(scrapy.Spider):

    
    name = "rec"
    def __init__(self):
        self.headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        self.df = pd.DataFrame(columns = ["nome","ingredientes","site"])
    def start_requests( self ):
        site = 'https://www.tudogostoso.com.br/receitas/'
        
        yield scrapy.Request(url = site, callback = self.bloco_receita, headers=self.headers)
        
    def bloco_receita(self, response):
        bloco = response.xpath('//div[@class="card recipe-card recipe-card-with-hover  "]/a/@href').extract()
        proxima = response.xpath('//a[@class="next"]/@href').extract_first()
        for item in bloco:
            yield response.follow(url = item, callback = self.pega_receita, headers = self.headers)
        if(proxima):
            yield response.follow(url = proxima, callback = self.bloco_receita, headers = self.headers)
    def pega_receita(self, response):
        receita = response.xpath('//div[@class="recipe-title"]/h1/text()').get().strip()
        ingrediente = response.xpath('//div[@class="col-lg-8 ingredients-card"]//ul//text()').getall()
        aux = pd.DataFrame({"nome":[receita],
                            "ingredientes":[ingrediente],
                            "site":[response.url]})
        self.df = self.df.append(aux, ignore_index = True)
        self.df.to_csv("C://Users//Lyncoln//Desktop//text.csv")
        time.sleep(1)
        
    

        


        
    
            
        




process = CrawlerProcess()
process.crawl(receita)
process.start()
