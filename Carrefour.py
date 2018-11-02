import mysql.connector
from bs4 import BeautifulSoup
import urllib.request

#CONSTANTES
Superficie = 'Carrefour'
urlCarrefourBase = 'https://www.carrefour.es/supermercado/'
alergenoSG='sin+gluten'
alergenoSL ='sin+lactosa'


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

def getCodeAlergeno(alergeno):
    res=[]
    urlAlergeno=urlCarrefourBase+'/c?Ntt='+alergeno
    url = urllib.request.urlopen(urlAlergeno)
    HtmlCode = url.read()
    SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores
    
    products=SoupObject.find_all('li',{"class":"level2-item"},limit=4) #limite segun se quiera
    for element in products:
        t1=element.a.text.split('\xa0')[0]
        t2=element.a.get('href').split('/')[2]
        t3=element.a.get('href').split('prtId=')[1]
        
        res.append((t1,t2,t3))
    print(res)
    return res

#Pagina de todas las categorias de alimentos sin lactosa, cojo los codigos de la categoria y monto urls con ellos. Esa url es pasada a otra funcion que extrae los objetos.
 
    
def getObjectos(alergeno):
    urlCatBase ='/c?Nr=AND%28product.shopCodes%3A004320%2Cproduct.salepointWithActivePrice_004320%3A1%2COR%28product.siteId%3AbasicSite%29%29&Ntt='+alergeno+'&prtId='
    alergenoAux='';
    connection =mysql.connector.connect(user='root', password='password',host='localhost',database='trabajotfg')
    mycursor = connection.cursor()
    #mycursor.execute("TRUNCATE TABLE PRODUCTO")
    listaCodes = getCodeAlergeno(alergeno)
    if(alergeno == 'sin+gluten'):
        alergenoAux = "GLUTEN"
    else:
        alergenoAux="LACTOSA"
  
    for element in listaCodes:
        urlCat=urlCarrefourBase+element[1]+urlCatBase+element[2]
        url = urllib.request.urlopen(urlCat)
        HtmlCode = url.read()
        SoupObject = BeautifulSoup(HtmlCode,"html.parser") #Se pone la segunda opcion para que no de errores
        SoupArticle = SoupObject.find_all('article', limit=4)
        
        for ArticleSimple in SoupArticle:
            ArticleName= ArticleSimple.find('h2').a.text.strip()
            ArticlePrice = ArticleSimple.find('p',{"class":"price"}).text.strip()
            ArticleBrand = ArticleSimple.find('p',{"class":"name-marca"}).a.text.strip()
            ArticleDictionary = {"brand":ArticleBrand,"name": ArticleName,"price":ArticlePrice}
            
            sqlQuery = "INSERT INTO producto (SUPERFICIE,ALERGENO,CATEGORIA, MARCA,NOMBRE,PRECIO) VALUES (%s,%s,%s, %s,%s,%s)"
            values = (alergenoAux,element[0],ArticleBrand,ArticleName,ArticlePrice)
            mycursor.execute(sqlQuery, values)
    connection.commit()
    mycursor.close()
    connection.close()
        

createDB();
getObjectos(alergenoSG);
getObjectos(alergenoSL);









