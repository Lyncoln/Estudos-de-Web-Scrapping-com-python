# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:41:31 2019

@author: Lyncoln
"""

import scrapy
import numpy as np 
from scrapy.crawler import CrawlerProcess

# Função que corrige as notas para serem calculadas no cr. 
# Se sua nota foi menor que 6, será verificado a nota da vs
# se a nota da vs foi maior ou igual a  6, a nota será substituida para 6
# Caso o contrário a nota sera calculada pela sua soma com a nota da vs dividida por 2    
def corrigir(nota,vs) :
    ind = 0
    for i in range(0,len(nota)):
        if(nota[i] < 6):
            if(vs[ind] > 6) :
                nota[i] = 6.0
                ind = ind + 1
            else:
                nota[i] = (nota[i] + vs[ind])/2
                ind = ind+1       
    return(nota)

class CRUFF(scrapy.Spider):
    name = 'calculaCR'
    login_url = 'https://app.uff.br/iduff/login.uff'
    start_urls=[login_url]
    
#Irá preencherr a aba login e senha do iduff
    
    def parse(self, response):
        token = response.css('input[name="login"]::attr(value)').extract_first()
        data = {
                "login" : token,
                "login:id" : "SEU LOGIN AQUI",
                "login:senha" : "SUA SENHA AQUI.",
                "login:btnLogar" : "Logar",
                "javax.faces.ViewState" : "j_id1"
                }       
        
        yield scrapy.FormRequest(url = self.login_url, formdata = data, callback = self.parse2)
        
#Vai até o link da aba histórico do site do iduff      
        
    def parse2(self, response):
        historico = response.xpath('//div[@id = "templatePrincipal2:j_id188:2:j_id189:0:j_id190_body"]/ul[3]//a/@href').extract_first()
        yield response.follow(url = historico,callback = self.parse3)
        
    
#Raspa as notas,vs e horários da tabela do histórico    
        
    def parse3(self,response):
        nota = response.xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[5]/text()').extract()
        hora = response.xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[8]/text()').extract()
        vs = response.xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[6]/text()').extract()
        nota = list(map(float, nota))
        hora = list(map(float, hora))
        vs = list(map(float, vs))
        corrigir(nota,vs)
        hora_total = sum(hora)
        
        
        pesos = np.array(nota) * np.array(hora)
        soma_pesos = sum(pesos)
        
        cr = soma_pesos / hora_total
        
        print("\n \n \n \n O seu CR é de : " + str(round(cr,1)))
        
        
        
    
        
       
       
process = CrawlerProcess()
process.crawl(CRUFF)
process.start()
