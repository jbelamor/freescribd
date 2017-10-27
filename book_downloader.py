import requests
from lxml import html
import sys
import threading
import re
#example url
#https://es.scribd.com/doc/266031488/HURRA-Po-polsku-1-Podrecznik-Studenta

def process_script_cont(text):
    """ lo que se hace es coger la funcion js, y de forma guarra se saca la url que esta en ese sitio """
    url_pat=re.compile('https:\/\/html[0-9]*-f\.scribdassets\.com\/([^\/]*)\/pages\/([^\/]*)\.jsonp')
    return url_pat.findall(text[0])[0]

def download_pic(url, n):
    print('Downloading picture {} from {}'.format(n, url))
    r=requests.get(url, stream=True)
    m=open('prueba{}.jpg'.format(n),'wb')
    m.write(r.content)
    m.close()


book=requests.get(sys.argv[1])
book_tree=html.fromstring(book.content)
last_urls=[]
page=1
xpath_scripts='//div[2]/div/main/div[1]/div[2]/script[{}]/text()'
sc_aux=book_tree.xpath(xpath_scripts.format(page))
#print(sc_aux)
pic_url_base='http://html.scribd.com/{}/images/{}.jpg'

while(sc_aux!=[]):
    try:
        id_book,id_page=process_script_cont(sc_aux)
        sc_aux=book_tree.xpath(xpath_scripts.format(page))
        formated_url=pic_url_base.format(id_book, id_page)
        print(formated_url)
        threading.Thread(target=download_pic, args=(formated_url, page)).start()
        page+=1
        
    except:
        break
