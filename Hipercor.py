# -*- coding: utf-8 -*-

import mysql.connector
from bs4 import BeautifulSoup
import urllib.request

#CONSTANTES

Superficie = 'Hipercor'
urlHipercorBase = 'https://www.hipercor.es/supermercado'
alergenoSG='/1853672072'
alergenoSL ='/824475013'


if __name__ == '__main__':
    pass


def createDB():
    connection =mysql.connector.connect(user='root', password='password',host='localhost',database='trabajotfg')
    exe=connection.cursor()
    exe.execute("""
    DROP TABLE PRODUCTO
    """)
    exe.execute("""
    CREATE TABLE PRODUCTO (
    SUPERFICIE VARCHAR (50),
    ALERGENO VARCHAR(30),
    MARCA VARCHAR (50),
    NOMBRE VARCHAR (100),
    CATEGORIA VARCHAR (50),
    PRECIO VARCHAR (10))
    """)
    exe.close()
    connection.close()

#Este metodo saca el nombre de la categoria, asi como los codigos necesarios para crear url.

def getCategorias():
    res=[]
    url = urllib.request.urlopen(urlHipercorBase)
    HtmlCode = url.read()
    SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores
    
    products=SoupObject.find_all('a',{"class":"top_menu-item"},limit=4) #limite segun se quiera

    for element in products:
        t1=element.text
        t2=element.get('href').split('/')[2]        
        res.append((t1,'/'+t2))
    return res
    

#Pagina de todas las categorias de alimentos sin lactosa, cojo los codigos de la categoria y monto urls con ellos. Esa url es pasada a otra funcion que extrae los objetos.
def getBrandFromString(brand):
    l= brand.split(' ')
    res=''
    for e in l:
        if(e.isupper()):
            res=res+' '+e
    return res.strip()

def getNameFromString(name):
    brand=getBrandFromString(name)
    res = name.replace(brand,'')
    '''
    l= name.split(' ')
    res=''
    for e in l:
        e.replace(brand,'')
        
        if(e.islower() | e.isnumeric()):
            res=res+' '+e'''
    return res.strip().capitalize()
    
def getObjectos(alergeno):
    alergenoAux='';
    connection =mysql.connector.connect(user='root', password='password',host='localhost',database='trabajotfg')
    mycursor = connection.cursor()
    #mycursor.execute("TRUNCATE TABLE PRODUCTO")
    listaCategorias = getCategorias()
    print(listaCategorias)
    if(alergeno == '/1853672072'):
        alergenoAux = "GLUTEN"
    else:
        alergenoAux="LACTOSA"
  
    for element in listaCategorias:
        urlCat=urlHipercorBase+element[1]+alergeno
        print("Categoria: "+element[0])
        url = urllib.request.urlopen(urlCat)
        HtmlCode = url.read()
        SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores
        SoupArticle = SoupObject.find_all("div",{"class":"product_tile-right_container"}, limit=4)
        for ArticleSimple in SoupArticle:
            try:
                ArticleBrand= getBrandFromString(ArticleSimple.find('a',{"class":"link event"}).get('title'))
                ArticleName= getNameFromString(ArticleSimple.find('a',{"class":"link event"}).get('title'))
                ArticlePrice = ArticleSimple.find('div',{"class":"prices-price _current"}).text
            except AttributeError:
                try:
                    ArticlePrice = ArticleSimple.find('div',{"class":"prices-price _offer"}).text
                except AttributeError:
                    ArticlePrice = ArticleSimple.find('div',{"class":"prices-price _current _no_pum"}).text

            print(ArticleBrand)
            print(ArticleName)
            print(ArticlePrice)
            #ArticleDictionary = {"brand":ArticleBrand,"name": ArticleName,"price":ArticlePrice}
            
            sqlQuery = "INSERT INTO producto (SUPERFICIE,ALERGENO,CATEGORIA, MARCA,NOMBRE,PRECIO) VALUES (%s,%s,%s, %s,%s,%s)"
            values = (Superficie,alergenoAux,element[0],ArticleBrand,ArticleName,ArticlePrice)
            mycursor.execute(sqlQuery, values)
    connection.commit()
    mycursor.close()
    connection.close()
        
#getCategorias()
createDB();
getObjectos(alergenoSG);
getObjectos(alergenoSL);



#getBrandFromString('NESTLE NESQUIK cacao instantáneo sin gluten bote 400 g')





