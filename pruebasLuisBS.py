'''
Created on 28 oct. 2018

@author: Luis
'''

#IMPORTACIONES

from bs4 import BeautifulSoup
import urllib.request
import mysql.connector


if __name__ == '__main__':
    pass

#Introduzco url y saco codigo html
#urlCarrefourBase = 'https://www.carrefour.es/supermercado'
#urlCarefourCategoria ='/N-szeq0k/c?Nr=AND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%29&Ntt=sin+lactosa&prtId=cat510001'
#'/N-zn66w/c?Nr=AND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%29&Ntt=sin+gluten&prtId=cat20019'
#urlp=urlCarrefourBase+urlCarefourCategoria

#url1 = urllib.request.urlopen(urlp)
#HtmlCode = url1.read()
#https://www.carrefour.es/supermercado/N-szeq0k/c?Nr=AND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%29&Ntt=sin+lactosa&prtId=cat510001
#Paso codigo html a objeto BeautifulSoap

#SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores

#print(SoupObject.prettify()) #Saca todo el codigo html.


#(SoupArticle) #Saca objeto etiqueta que contiene cada item
###################

urlCarrefourBase = 'https://www.carrefour.es/supermercado/'
#urlCarrefourBaseCat = 
# Este método saca el nombre de la categoria, asi como los codigos necesarios para crear url
def getCodeSinLactosa(): 
    lista2_0=[]
    urlSinLactosa=urlCarrefourBase+'/c?Ntt=sin+lactosa'
    url1 = urllib.request.urlopen(urlSinLactosa)
    HtmlCode = url1.read()
    SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores
    listaLevel2=SoupObject.find_all('li',{"class":"level2-item"},limit=4)
    #print(listaLevel2)
    #print(listaLevel2[0].a.get('href'))

    for element in listaLevel2:
        t1=element.a.text.split('\xa0')[0]
        t2=element.a.get('href').split('/')[2]
        t3=element.a.get('href').split('prtId=')[1]
        
        lista2_0.append((t1,t2,t3))
    print(lista2_0)
    return lista2_0
    
    
def getObjectsSinLactosa():
    #Pagina de todas las categorias de alimentos sin lactosa, cojo los codigos de la categoria y monto urls con ellos. Esa url es pasada a otra funcion que extrae los objetos.
    res = []
    urlCatBase ='/c?Nr=AND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%29&Ntt=sin+lactosa&prtId='
    listaCodes = getCodeSinLactosa()
    
    for element in listaCodes:
        print(element[0])
        urlCat=urlCarrefourBase+element[1]+urlCatBase+element[2]
        print(urlCat)
        url1 = urllib.request.urlopen(urlCat)
        HtmlCode = url1.read()
        SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores
        resaux=(element[0],getObjetosDentroCat(SoupObject)) #Extrae objetos de cada categoria, creada mediante lista de codes.
        res.append(resaux)
        print(resaux)
        print("Termina esta categoria")
    print(res)
    return res
        
    
def getObjetosDentroCat(SoupObject):
    
    res=[]
    SoupArticle = SoupObject.find_all('article', limit=4)
    for ArticleSimple in SoupArticle:
        ArticleName= ArticleSimple.find('h2').a.text.strip()
        ArticlePrice = ArticleSimple.find('p',{"class":"price"}).text.strip()
        ArticleBrand = ArticleSimple.find('p',{"class":"name-marca"}).a.text.strip()
        ArticleDictionary = {"brand":ArticleBrand,"name": ArticleName,"price":ArticlePrice}
        res.append(ArticleDictionary)
        #print("Marca: "+ArticleBrand+"\rNombre: "+ArticleDictionary["name"] + "\rPrecio "+ArticleDictionary["price"]+"\r\r") 
    
    return res


#https://www.carrefour.es/supermercado/c?Ntt=sin+lactosa
getObjectsSinLactosa()
