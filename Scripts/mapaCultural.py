import scrapy


class mapaCultura(scrapy.Spider):
    name = "cultura"
    # Começar
    def start_requests( self ):
        site = 'http://mapadecultura.rj.gov.br/categoria/espacos-culturais?page=1#ancora'
        yield scrapy.Request(url = site, callback = self.parse)
    # Primeira etapa
    def parse(self, response):
        links = response.css('h3 > a::attr(href)').extract()
        proxima = response.css('.proxima > a::attr(href)').extract_first()
        for link in links :
            yield response.follow(url = link, callback = self.parse2)
        if(proxima):
            yield response.follow(url = proxima, callback = self.parse)
            
            
      
        
        
        
    def parse2(self, response):
        print("\n")
        #pagina = response.css('div#lateral').extract_first()
        titulo = response.css('h1::text').extract_first().strip()
        print(titulo +": \n" )
        #print(pagina)
        #print("--------- \n ---------\n ---------\n")
       
    
        
    
