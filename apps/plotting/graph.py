
import sys

import mysql.connector
import matplotlib.pyplot as plt

import logging

import os
import dotenv
dotenv.load_dotenv()


def connection():
   mydb = mysql.connector.connect(
   host=os.getenv('mysql_host'),
   user=os.getenv('mysql_user'),
   password=os.getenv('db_pwd'),
   database=os.getenv('db')
    )
   return mydb

def product_id_input(mydb,pid):
    cursor=mydb.cursor()
    logging.info("connection is done")
 
    query ='''SELECT * FROM Price WHERE product_id = %s'''
    cursor.execute(query,(pid,))
   
    data=cursor.fetchall()
    print(data)
    return data


def main():
    pid = sys.argv[1] 
    mydb=connection()
    result = product_id_input(mydb,pid)
    
    price=[result[0][0]]
 
    datetime=[result[0][1]]

    for i in range(1,len(result)):
       
        price.append(result[i][0])
        datetime.append(result[i][1])
  
    plt.plot( datetime,price)
    plt.xlabel('Datetime')
    plt.ylabel('Price')
    plt.xticks(rotation = 45)
    plt.show()

if __name__ == '__main__':
    main()