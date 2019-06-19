# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:33:57 2019

@author: tpc 02
"""

from selenium import webdriver
import time
import os

os.chdir("C://Users//tpc 02//Desktop//Acordao//Documentos")


#chrome_path = "C://Users//tpc 02//Desktop//chromedriver.exe"
#driver = webdriver.Chrome(chrome_path)
#driver.get("https://pesquisa.apps.tcu.gov.br/#/pesquisa/todas-bases/%20")   
#time.sleep(15)          
#driver.find_element_by_xpath('//*[@id="mdc-dialog-ajuda"]/div[1]/footer/button').click()
#           
#driver.find_element_by_xpath('//*[@id="termo_pesquisado"]').send_keys("portos portuários")
#driver.find_element_by_xpath('//*[@id="conteudo-principal"]/pesquisa/div/mat-sidenav-container/mat-sidenav-content/div/pesquisa-todas-bases/div/div[1]/div/div[1]/div/form/div/div/button/i').click()
#time.sleep(15)
#
#driver.find_element_by_xpath('//*[@id="link_resultado_0"]/h3').click()
#




chrome_path = "C://Users//tpc 02//Desktop//chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
driver.get("https://pesquisa.apps.tcu.gov.br/#/documento/acordao-completo/%2520portos%2520portu%25C3%25A1rios/%20/DTRELEVANCIA%20desc,%20NUMACORDAOINT%20desc/0/%20?uuid=a4eeaad0-92c8-11e9-828b-a1fcf3706dd6")
time.sleep(15)
driver.find_element_by_xpath('//*[@id="mdc-dialog-ajuda"]/div[1]/footer/button').click()           
#linha = driver.find_elements_by_xpath('//*[@id="topoDocumento"]/div/div/div[2]/div[2]')


#i = 0
proximo = driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/div/ul/li[2]/a/i')
time.sleep(10)
while(proximo):
    #i = i + 1
    nome = driver.find_element_by_xpath('//*[@id="conteudo_processo"]/a').text
    nome = nome.replace("/","_")
    linha = driver.find_elements_by_class_name('documento')
#    arq = open('arquivo_'+str(i)+'.rtf', 'w')
    with open('processo'+nome+'.rtf', 'w', encoding='utf-8') as arq:
        for x in linha:
            arq.write(x.text+'\n')
    arq.close()
    
    proximo.click()
    time.sleep(10)
    


