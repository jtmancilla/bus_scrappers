from lxml import html
# Depending on page
import requests
from selenium import webdriver
import time


class Base:
    """
    General class for bus lines scrappers.
    Receives html pointers for:
    origin, destination, departure, arrival, type of the service,
    enterprise, price of the service.
    """
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
        self.xpath_origin = 'definir'
        self.xpath_destination = 'definir'
        self.xpath_departure = 'definir'
        self.xpath_arrival = 'definir'
        self.xpath_enterprise = 'definir'
        self.xpath_type_service = 'definir'
        self.xpath_sale_price = 'definir'
        self.xpath_descount_price = 'definir'

    def origen_destino(self):
        """
        Retrieving origin and destination.
        :self.xpath_destination: html pointer for origin.
        :self.xpath_destination: html pointer for destination.
        return: origin, destination.
        """
        origin = self.html.xpath(self.xpath_origin)
        destination = self.html.xpath(self.xpath_destination)
        origen = map(self.limpieza_texto, origin)
        destino = map(self.limpieza_texto, destination)
        return origen, destino
    
    def salida_llegada(self):
        """
        Retrieving departure and arrival.
        :self.xpath_departure: html pointer for deptarture.
        :self.xpath_arrival: html pointer for arrival.
        return: departure, arrival.
        """
        departure = self.html.xpath(self.xpath_departure)
        arrival = self.html.xpath(self.xpath_arrival)
        salida = map(self.limpieza_texto, departure)
        llegada = map(self.limpieza_texto, arrival)
        return salida, llegada
    
    def tipo_servicio(self):
        """
        Retrieving type of service.
        :self.xpath_name: html pointer for type of service.
        return: type.
        """
        type_service = self.html.xpath(self.xpath_type_service)
        tipo_servicio = map(self.limpieza_texto, type_service)
        return tipo_servicio

    def empresa(self):
        """
        Retrieving enterprise.
        :self.xpath_enterprise: html pointer for enterprise.
        return: enterprise.
        """
        enterprise = self.html.xpath(self.xpath_enterprise)
        empresa = map(self.limpieza_texto, enterprise)
        return empresa
    
    def precio(self):
        """
        Retrieving price of service.
        :self.xpath_sale_price: html pointer for price.
        return: clean price.
        """
        price = self.html.xpath(self.xpath_sale_price)
        precio = map(self.limpieza_precio, price)
        return precio
    

    def precio_descuento(self):
        """
        Retrieving price of service.
        :self.xpath_descount_price: html pointer for price.
        return: clean descount_price.
        """
        descount_price = self.html.xpath(self.xpath_descount_price)
        precio_descuento = map(self.limpieza_precio, descount_price)
        return precio_descuento


    def limpieza_texto(self,strin):
        strin2 = ' '.join(strin.split())
        return strin2
        
    def limpieza_precio(self,strin):
        strin = ' '.join(strin.split())
        strin = strin.replace("$", "")
        strin = strin.replace("MXN", "")
        strin = strin.replace(",", "")
        return strin
    
    def wrap_info(self):
        origen, destino = self.origen_destino()
        salida, llegada = self.salida_llegada()
        tipo = self.tipo_servicio()
        empresa = self.empresa()
        precio = self.precio()
        precio_descuento = self.precio_descuento()
        info = [origen, destino, salida, llegada, tipo, empresa, precio,precio_descuento]
        return info

class Clickbus(Base):
    def __init__(self, url):
        Base.__init__(self)
        self.store_id = 1
        self.url = url
        #self.page = requests.get(self.url, headers=self.headers)
        #self.html = html.fromstring(self.page.content)
        #self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Chrome("/Users/jamancilla/Dropbox/Projects/bus_scrappers/chromedriver")
        self.driver.get(self.url)
        time.sleep(15)
        self.page = self.driver.page_source
        self.driver.quit()
        self.html = html.fromstring(self.page)
        self.base = '//div[@class="trip-information"]'
        self.xpath_origin = self.base+'//div[@class="info-row station from ng-binding"]//text()'
        self.xpath_destination = self.base+'//div[@class="info-row station to ng-binding"]//text()'
        self.xpath_departure = self.base+'//div[@class="info-row schedule departure ng-binding"]//text()'
        self.xpath_arrival = self.base+'//div[@class="info-row schedule arrival ng-binding"]//text()'
        self.xpath_enterprise = self.base+'//div[@class="company info-container"]//span[@class="hidden ng-binding"]//text()'
        self.xpath_type_service = '//div[@class="trip-services"]//span[@class="service-class ng-binding"]//text()'
        self.xpath_sale_price = self.base+'//div[@class="normal-price" or @class="normal-price cancel"]//span[@itemprop="price"]//text()'
        self.xpath_descount_price= self.base+'//div[@class="offer-price ng-scope" or @class="normal-price"]//span[@itemprop="offer" or @itemprop="price"]//text()'
