import datetime
import requests
import logging
import mysql.connector

import os
import dotenv
dotenv.load_dotenv()



from bs4 import BeautifulSoup
from mysql.connector import Error
from mysql.connector import errorcode

def scraper():
    speakers=[]
    for i in range(1,16):
        link="https://www.amazon.in/s?k=top+50+speakers&page="+str(i)+"&qid=1612250144&ref=sr_pg_"+str(i)

        

        site=requests.get(link).text
        
        s=BeautifulSoup(site,'lxml')
        main=s.findAll("div",attrs={'class':'s-include-content-margin s-border-bottom s-latency-cf-section'})

        for d in main:
    
            name=d.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal' }).text[0:100]
    
            if d.find('span', attrs={'class':'a-price-whole'}):
               
                Listed_price=d.find('span', attrs={'class':'a-price-whole'}).text
                
            else:
                Listed_price="NA"
            if d.find('span', attrs={'class':'a-price a-text-price'}):
                a=d.find('span', attrs={'class':'a-price a-text-price'})
                if a.find('span', attrs={'class':'a-offscreen'}):
                    Actual_price=a.find('span', attrs={'class':'a-offscreen'}).text
                else:
                    Actual_price="NA"
            if d.find('span', attrs={'class':'a-icon-alt'}):
                rating=d.find('span', attrs={'class':'a-icon-alt'}).text[0:3]
            else:
                rating="NA"
            dt=datetime.datetime.now()
            #print(dt)
         
            if Listed_price =='NA':
                
                continue

            speakers.append([name,Listed_price,Actual_price,rating,str(dt)])
    
    return speakers 

def inserting(speakers):

    mydb = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    cursor=mydb.cursor()
    n=len(speakers)
    # n=len(speakers)
    for i in range(n):
        logging.info('executed times',i)
        name=str(speakers[i][0])
      
        listed_price=str(speakers[i][1][0:].replace(',',''))
        print(listed_price)
       
        cursor.execute("SELECT product_id FROM Products WHERE product_Name = %s",(name,))
        res=cursor.fetchone()
       
        pid=None
        if res:
            pid=res[0]
        query='''insert into Price (listed_price, product_id) values (%s,%s)'''
        print(query)
        logging.info("person id is",pid)
       
        if pid:
          
            logging.info("in the if statement",pid)
            cursor.execute(query,(listed_price,pid,))
            mydb.commit()
        else:
         
            logging.info("else block",i)
            q1="insert into Products (product_name) values (%s)"
            cursor.execute(q1,(name,))
            mydb.commit()
            cursor.execute("SELECT product_id FROM Products WHERE product_Name = %s",(name,))
            res=cursor.fetchone()
            pid=res[0]

            cursor.execute(query, (listed_price,pid,))
            mydb.commit()
    mydb.close()

result=scraper()
inserting(result)