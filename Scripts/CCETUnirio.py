# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:37:45 2019

@author: tpc 02
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException   
import time
import os

def checarExiste(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


os.chdir("C://Users//tpc 02//Desktop")
file1 = open("raspagemunirio4.txt","w")
chrome_path = "C://Users//tpc 02//Desktop//chromedriver.exe"


driver = webdriver.Chrome(chrome_path)
driver.get("http://www.unirio.br/")
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="searchGadget"]').click()           
driver.find_element_by_xpath('//*[@id="searchGadget"]').send_keys("CCET")
driver.find_element_by_xpath('//*[@id="searchGadget_form"]/div/input[2]').click()




## Navega entre os blocos de notícia
lista = driver.find_elements_by_xpath('//*[@id="search-results"]/dl//dt/a')
site = driver.current_url
aux = 0
for bloco in lista:
    listaNova = driver.find_elements_by_xpath('//*[@id="search-results"]/dl//dt/a')
    listaNova[aux].click()
    texto = driver.find_element_by_xpath('//*[@id="content"]').text
#    texto = driver.find_element_by_xpath('//*[@id="parent-fieldname-title"]').text
    file1.write(texto + '\n \n')
    time.sleep(1)
#    driver.get(site)
    driver.execute_script("window.history.go(-1)") 
    aux = aux + 1
    time.sleep(1)
##
 
    
while(checarExiste('//span[@class="next"]/a')):
    driver.find_element_by_xpath('//span[@class="next"]/a').click()
    time.sleep(1)
    lista = driver.find_elements_by_xpath('//*[@id="search-results"]/dl//dt/a')
#    site = driver.current_url
    aux = 0
    for bloco in lista:
        listaNova = driver.find_elements_by_xpath('//*[@id="search-results"]/dl//dt/a')
        listaNova[aux].click()
        texto = driver.find_element_by_xpath('//*[@id="content"]').text
#       texto = driver.find_element_by_xpath('//*[@id="parent-fieldname-title"]').text
        file1.write(texto + '\n \n')
        time.sleep(1)
#        driver.get(site)
        driver.execute_script("window.history.go(-1)") 
        aux = aux + 1
        time.sleep(1)

        
file1.close()