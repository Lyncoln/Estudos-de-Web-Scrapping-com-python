import scrapy

#Há um problema com o site, quando você altera de página para acessar novas casas,
#o site sempre irá mostrar as 12 primeiras casas, em qualquer que seja a aba
#para isso dividi o código em 2 etapas, a primeira etapa ele irá pegar 
#as 12 primeiras casas que sempre se repetem, e em seguida, irá executar um
#loop para sempre pegar as 12 casas da parte de baixo do site



class mapaCultura(scrapy.Spider):
    name = "cultura"
    # Começar
    def start_requests( self ):
        site = 'http://mapadecultura.rj.gov.br/categoria/espacos-culturais?page=1#ancora'
        yield scrapy.Request(url = site, callback = self.parse)

    #Primeira etapa consiste em pegar todos as casas que estão presentes na segunda caixa
    #De apresentação do site
    
    
    
    def parse(self, response):
        segundoquadro = response.xpath('//*[@id="conteudo"]/div[5]/ul[2]//li/h3/a/@href').extract() 
        proxima = response.css('.proxima > a::attr(href)').extract_first()
        for link in segundoquadro :
            yield response.follow(url = link, callback = self.parse2)
        if(proxima):
            yield response.follow(url = proxima, callback = self.parse)
        if(proxima is  None):
            print("\n \n \n \n\n \n \n \n \n \n \n --------- \n \n \n \n \n \n \n \n \n \n \n \n \n")
            yield response.follow(url = 'http://mapadecultura.rj.gov.br/categoria/espacos-culturais', callback= self.Comeco )
    
    #Por final, eu volto para primeira página e pego as 12 que sempre se repetem 
    def Comeco(self, response) :
        primeiroQuadro = response.xpath('//*[@id="conteudo"]/div[5]/ul[1]//li/h3/a/@href').extract()
        for link in primeiroQuadro :
            yield response.follow(url = link, callback = self.parse2)        
     
        
    def parse2(self, response):
        print("\n")
        #pagina = response.css('div#lateral').extract_first()
        titulo = response.css('h1::text').extract_first().strip()
        print(titulo +": \n" )
        #print(pagina)
        #print("--------- \n ---------\n ---------\n")
       
    
        
    
