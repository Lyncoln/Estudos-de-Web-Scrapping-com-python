import scrapy
from scrapy.crawler import CrawlerProcess

arquivo = open('resultado.txt','w')
#Apertar ctrl + . para reiniciar o kernel
# scrapy runspider [options] <spider_file>

class pegaExcel(scrapy.Spider):
    name = 'Excel'
   
    parte1 = 'https://www.fnde.gov.br/distribuicaosimadnet/selecionar?numeroEntidade=000000'
    parte2 = '&anoPrograma='       
    parte3 = '&codigoPrograma=01&ufSelecionada='
    parte4 = '&criterios='
    comutacoes = []
    
    UF = ["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
    ANO = ["2015","2016","2017","2018","2019"]    
    
    for i in range(0,1000000):
        num = str(i)
        while(len(num)<6):
            num = '0' + num
        comutacoes.append(num)
            
        
    i = 0 
    links = []
        
    for numero in comutacoes :
        for j in UF:
            for k in ANO:
                links.append(parte1+comutacoes[i]+parte2+ANO[j]+parte3+UF[k]+parte4) 
                i = i+1
        
            
    start_urls = links
        
    def parse(self, response):
        pag = response.xpath('//*[@id="pesquisar"]/div[4]/a[1]/@href').extract_first()
        if(pag):
            arquivo.write(str(pag)+'\n')
       
    
#    def parse(self, response):
#        try:
#            excel = response.xpath('//*[@id="pesquisar"]/div[4]/a[1]').extract()
#                       
#        except:
#            pass 
        
       
process = CrawlerProcess()
process.crawl(pegaExcel)
process.start()
arquivo.close() 