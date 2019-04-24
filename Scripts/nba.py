#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 07:20:41 2019

@author: 216054055
"""


import scrapy
from scrapy.crawler import CrawlerProcess
import numpy as np
from datetime import datetime
import pandas as pd

class nba(scrapy.Spider):
    name = "dsfadsfgef"
    start_urls = ["https://www.basketball-reference.com/leagues/NBA_2019_per_game.html?fbclid=IwAR0TjP63hgGFFyj01klfehVs1kcYrepTx-o-dlvFTZE6oChwyJeoJugeSas"]
    agora = datetime.now()
    def parse(self, response):
        nome = response.xpath("//thead//tr//text()").getall()
        nome = np.array(nome)
        nome = np.char.strip(nome)
        nome = nome[nome!=""]
        cam = response.xpath("//tbody//tr")
        df = pd.DataFrame(columns=nome[1:])
        aux = list()
        i = 0
        for item in cam:
            for pos in range(30-1):
                aux.append(item.xpath("td["+str(pos+1)+"]//text()").get(default="NA"))
            df.loc[i] = aux
            i=i+1
            aux = []
        df.to_csv(r'/mnt/publica/1 AREA DO ALUNO/Lyncoln Sousa/data.csv')
        print(datetime.now() - self.agora )
            


process = CrawlerProcess()
process.crawl(nba)
process.start()