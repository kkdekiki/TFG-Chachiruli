'''
Created on 30 oct. 2018

@author: Luis
'''
import mysql.connector
from bs4 import BeautifulSoup
import urllib.request

if __name__ == '__main__':
    pass

urlCarrefourBase = 'https://www.carrefour.es/supermercado/'
urlCatBase ='/c?Nr=AND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%29&Ntt=sin+lactosa&prtId='


def createDB():
    connection =mysql.connector.connect(user='root', password='password',host='localhost',database='trabajotfg')
    exe=connection.cursor()
    exe.execute("""
    CREATE TABLE PRODUCTO (
    MARCA VARCHAR (50),
    NOMBRE VARCHAR (100),
    CATEGORIA VARCHAR (50),
    PRECIO VARCHAR (10))
    """)
    exe.close()
    connection.close()

#Este metodo saca el nombre de la categoria, asi como los codigos necesarios para crear url.

def getCodeSinLactosa():
    lista2_0=[]
    urlSinLactosa=urlCarrefourBase+'/c?Ntt=sin+lactosa'
    url1 = urllib.request.urlopen(urlSinLactosa)
    HtmlCode = url1.read()
    SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores
    
    listaLevel2=SoupObject.find_all('li',{"class":"level2-item"},limit=4) #limite segun se quiera
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
    connection =mysql.connector.connect(user='root', password='password',host='localhost',database='trabajotfg')
    mycursor = connection.cursor()
    mycursor.execute("TRUNCATE TABLE PRODUCTO")
    res = []
    listaCodes = getCodeSinLactosa()
  
    for element in listaCodes:
        #print(element[0]) #Categoria
        urlCat=urlCarrefourBase+element[1]+urlCatBase+element[2]
        url1 = urllib.request.urlopen(urlCat)
        HtmlCode = url1.read()
        SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores
        SoupArticle = SoupObject.find_all('article', limit=4)
        
        for ArticleSimple in SoupArticle:
            ArticleName= ArticleSimple.find('h2').a.text.strip()
            ArticlePrice = ArticleSimple.find('p',{"class":"price"}).text.strip()
            ArticleBrand = ArticleSimple.find('p',{"class":"name-marca"}).a.text.strip()
            ArticleDictionary = {"brand":ArticleBrand,"name": ArticleName,"price":ArticlePrice}
            
            sql = "INSERT INTO producto (CATEGORIA, MARCA,NOMBRE,PRECIO) VALUES (%s, %s,%s,%s)"
            val = (element[0],ArticleBrand,ArticleName,ArticlePrice)
            mycursor.execute(sql, val)
            
        #print("Termina esta categoria")
    connection.commit()
    mycursor.close()
    connection.close()
    #print(res)
    #return res
        


#https://www.carrefour.es/supermercado/c?Ntt=sin+lactosa
getObjectsSinLactosa()









