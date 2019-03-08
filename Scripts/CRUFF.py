# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 17:41:31 2019

@author: Lyncoln
"""

import scrapy
import numpy as np 
from scrapy.crawler import CrawlerProcess
from selenium import webdriver




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
    custom_settings = {
        'LOG_ENABLED':'False',
    }
    name = 'calculaCR'
    login_url = 'https://app.uff.br/iduff/login.uff'
    start_urls=[login_url]
    login = "SEU LOGIN"
    senha = "SUA SENHA"
    #
    
    #
    
    
    

    

    print("\n Spider em ação : \n \n \n")
    
#Irá preencherr a aba login e senha do iduff
    
    def parse(self, response):
        token = response.css('input[name="login"]::attr(value)').extract_first()
        data = {
                "login" : token,
                "login:id" : self.login,
                "login:senha" : self.senha,
                "login:btnLogar" : "Logar",
                "javax.faces.ViewState" : "j_id1"
                }       
        
        yield scrapy.FormRequest(url = self.login_url, formdata = data, callback = self.parse2)
        
#Vai até o link da aba histórico do site do iduff      
        
    def parse2(self, response):
        historico = response.xpath('//div[@id = "templatePrincipal2:j_id188:2:j_id189:0:j_id190_body"]/ul[3]//a/@href').extract_first()
        if(historico):
            yield response.follow(url = historico,callback = self.parse3)
        else :
            
            #matriculas = []
            #opcoes = response.xpath('//li[@class="extraUserActions"]/a/text()').extract()
            #for itens in opcoes:
            #    
            #    matriculas.append(itens.split())
            #    
            #matriculas = np.array(matriculas)
            #matriculas = matriculas[:,2]
            #print("Você tem as seguintes matrículas :", end = "")
            #for mat in matriculas :
            #    print(mat + ", ", end = "")
             
            
            #Daqui para baixo estamos programando com selenium
            chrome_path = r'E:\Download\chromedriver.exe'         
            driver = webdriver.Chrome(chrome_path)
            driver.get(response.url)
            #Colocando o cpf no campo login
            driver.find_element_by_xpath("//*[@id='login:id']").send_keys(self.login)
            #Colocando a senha no campo senha
            driver.find_element_by_xpath("//*[@id='login:senha']").send_keys(self.senha)
            #Clicar no botão
            driver.find_element_by_xpath("//*[@id='login:btnLogar']").click()
            #Matriculas disponíveis 
            print("Você possui as seguintes matrículas :")
            
            
            mat = driver.find_elements_by_xpath('//li[@class="extraUserActions"]/a')
            numero = 1
           
            for x in mat :
                print(str(numero)+": "+x.text)
                numero = numero + 1
                
            
            desejada = int(input("Qual matrícula você quer acessar? [ Escolha entre 1 e "+str(len(mat))+" ]\n"))
            #Vai achar sua matricula desejada
            matricula = mat[desejada - 1]
            #Vai clicar nela
            matricula.click()
            #Vai até a aba histórico
            driver.find_element_by_xpath('//div[@id="templatePrincipal2:j_id189:2:j_id190:0:j_id191"]/div/ul[3]/li/a').click()
            #Vai pegar o vetor de notas
            nota = driver.find_elements_by_xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[5]')            
            nota = [x.text for x in nota]
            nota = list(map(float, nota))
            #Vai pegar o vetor de hotas
            hora = driver.find_elements_by_xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[8]')            
            hora = [x.text for x in hora]
            hora = list(map(float, nota)) 
            #Vai pegar o vetor de vs
            vs = driver.find_elements_by_xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[6]')            
            vs = [x.text for x in vs]
            vs = list(map(float, nota))
            corrigir(nota,vs)
            print(nota)
            hora_total = sum(hora)
        
        
            pesos = np.array(nota) * np.array(hora)
            soma_pesos = sum(pesos)
        
            cr = soma_pesos / hora_total
        
            print(cr)
           

    
#Raspa as notas,vs e horários da tabela do histórico    
        
    def parse3(self,response):
        nota = response.xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[5]/text()').extract()
        hora = response.xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[8]/text()').extract()
        vs = response.xpath('//tbody[@id="historico:tblDisciplinasHistorico:tb"]//td[6]/text()').extract()
        nome = response.xpath('//tr[1]/td[3]/text()').extract_first().split()
        nota = list(map(float, nota))
        hora = list(map(float, hora))
        vs = list(map(float, vs))
        corrigir(nota,vs)
        hora_total = sum(hora)
        
        
        pesos = np.array(nota) * np.array(hora)
        soma_pesos = sum(pesos)
        
        cr = soma_pesos / hora_total
        
       # print(nome.capitalize()+", o seu CR é de :" + str(round(cr,1)))
        [print(x.capitalize(), end = " ") for x in nome]
        print(", o seu CR é: ",round(cr,1))
        
        
    
        
       
       
process = CrawlerProcess()
process.crawl(CRUFF)
process.start()
