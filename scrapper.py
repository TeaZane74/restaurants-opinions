from attr import attr
import pandas as pd
from bs4 import BeautifulSoup 
import urllib.request
from urllib.error import HTTPError
import time
from random import random
import re

from sklearn.metrics import classification_report 
parser = 'html.parser' # or 'lxml' (preferred) or 'html5lib', if installed 
resp = urllib.request.urlopen('https://www.yelp.fr/search?cflt=restaurants&find_loc=Paris%2C+Paris%2C+FR&sortby=review_count&start=0') 
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset')) 
first = True
sites = dict()
df = None


list_url = ["https://www.yelp.fr/search?find_desc=&find_loc=lyon&sortby=review_count","https://www.yelp.fr/search?find_desc=&find_loc=lille&sortby=review_count&start=","https://www.yelp.fr/search?cflt=restaurants&find_loc=Paris%2C+Paris%2C+FR&sortby=review_count&start="]

for page in range(0,25):
    time.sleep(random()*10+1)
    try :
        resp = urllib.request.urlopen(f'https://www.yelp.fr/search?find_desc=&find_loc=lyon&sortby=review_count&start={page*10}') 
    except HTTPError:
        print('Bloqué')
        break

    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset')) 
    
    for link in soup.find_all('a', href=True): 
        if "name=" in str(link):
            sites[link["name"]] = link['href']
print(sites)


for i in sites.keys():
    time.sleep(random()*10+1)
    print(i)
    for nb_comment in range (0,10):
        time.sleep(random()*10+1)
        try :
            resp = urllib.request.urlopen(f'https://www.yelp.fr/{sites[i]}?start={nb_comment*10}') 
        except HTTPError:
            print('Bloqué')
            break
            
        soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    

        price = soup.find_all("span", class_="css-1ir4e44")
        for text in price :
            if '€' in text.getText():
                pri = text.getText().count('€')


        for bloc_comment in soup.find_all("li", class_="margin-b5__09f24__pTvws border-color--default__09f24__NPAKY"):
            stars = bloc_comment.find_all("div", class_ = re.compile(r"i-stars__09f24__M1AR7 i-stars--regular-[1-5].*ayzG"))
            for text in stars:
                star = int(text['aria-label'].replace(' étoiles', ''))
                



            comment = bloc_comment.find_all("p")
            for text in comment:
                comm = text.getText()
                
                
            name = i.replace('’',"'")
            comm = comm.replace('\u20ac','euros').replace('\uff0c',',').replace('\u0117','e')
            comm = comm.replace('\u0153','oe').replace('\u2026','...').replace('\u0152','OE').replace('\xa0','')
            
            report = {'nom':name, 'prix':pri,'etoile' : star, 'avis':comm}


            df = pd.DataFrame([report])

            try :
                if first == True : 
                    df.to_csv("bdd_avis_restaurant.csv", mode='a+', encoding='utf-8', sep="|",header=True,index=False)
                    first = False
                else :
                    df.to_csv("bdd_avis_restaurant.csv", mode='a+', encoding='utf-8', sep="|",header=False, index=False)
            except UnicodeEncodeError as error:
                print(error)
    


