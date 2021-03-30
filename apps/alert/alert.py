
import os
import sys

import mysql.connector
import dotenv
import logging

from mailjet_rest import Client
from twilio.rest import Client as smsClient
dotenv.load_dotenv()
def connection():
   
    mydb = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    return mydb
def update_db(mydb):
    cursor=mydb.cursor()
    query='''UPDATE `alert` SET `alert_status`=1 WHERE `alert_status`= 0'''
    cursor.execute(query)
    mydb.commit()

def alert_mail(mydb):
    cursor=mydb.cursor()
    query='''SELECT DISTINCT (SELECT `product_name` FROM `Products` pro WHERE pro.product_id = p.product_id) AS prod_name, a.threshold, p.product_id, p.listed_price, p.date_time,a.user_email,a.phone_no,a.alert_status
            FROM `alert` a JOIN `Price` p ON a.product_id = p.product_id
            WHERE p.date_time = (SELECT MAX(p2.date_time) FROM `Price` p2
            WHERE p2.product_id = p.product_id); '''
    cursor.execute(query)
    data=cursor.fetchall()
    #print(data)
    for i in data:
        prod_name=i[0]
        price=int(i[3])
        #print(price)
        threshold=i[1]
        #print(threshold)
        #print("alert_sent",i[7])
        if price > threshold or i[7]:
             
            print("the price is above threshold or the alert is already sent")
            
        else:
            #print('price drop')
            if i[5] and i[6]=='':
                api_key = os.getenv('api_key')
                api_secret = os.getenv('api_secret')
                sender_mail=os.getenv('sender_email')
                reciever_mail=i[5]
                #print(reciever_mail)
                print('mail')
                mailjet = Client(auth=(api_key, api_secret), version='v3.1')
                data = {
                  'Messages': [
                				{
                						"From": {
                								"Email": sender_mail,
                								"Name": "Amazon spraker Price Alert"
                						},
                						"To": [
                								{
                										"Email": reciever_mail,
                										"Name": "Subscriber"
                								}
                						],
                                        
                					
                                        "Subject": "Price Drop Alert",
                                        "HTMLPart": "<h3>Your wishlist Product "+i[0]+" price is drop and  Product's current price is <span>&#8377;</span>"+i[3]+" </h3> <br>  <p><span>Thanks & Regard</span> <br><span>Prashant Tripathi</span></p>"
 
                                    
                				}
                		]
                }
                result = mailjet.send.create(data=data)
                print(result.status_code)
                # print(result.json())
            if i[6] and i[5]=='':
                # and set the environment variables. See http://twil.io/secure
             acc_sid = os.getenv('acc_sid')
             auth_token = os.getenv('auth_token')
             client = smsClient(acc_sid, auth_token)
             print('mob')
             message = client.messages \
                             .create(
                                   body="Your wishlist  Product "+i[0]+" is below "+str(i[1])+" and the current price is "+str(i[3]),
                                   from_='+13467014751',
                                   to='+91 '+i[6]
                              )

             print(message.sid)
            if i[5] and i[6]:
                print('mob&mail')
                acc_sid = os.getenv('acc_sid')
                auth_token = os.getenv('auth_token')
                client = smsClient(acc_sid, auth_token)

                message = client.messages \
                                .create(
                                     body="Your wishlist Product "+i[0]+" is below "+str(i[1])+" and the current price is "+str(i[3]),
                                     from_='+13467014751',
                                     to='+91 '+i[6]
                                 )

                print(message.sid)
                api_key = os.getenv('api_key')
                api_secret = os.getenv('api_secret')
                sender_mail=os.getenv('sender_email')
                reciever_mail=i[5]
                mailjet = Client(auth=(api_key, api_secret), version='v3.1')
                data = {
                  'Messages': [
                				{
                						"From": {
                								"Email": sender_mail,
                								"Name": "Amazon speakers Price Alert"
                						},
                						"To": [
                								{
                										"Email": reciever_mail,
                										"Name": "Subscriber"
                								}
                						],
                                       
                						"Subject": "Price Drop Alert",
                                        "HTMLPart": "<h3>Your wishlist Product "+i[0]+" price is drop  and  Product's current price is <span>&#8377;</span>"+i[3]+" </h3> <br>  <p><span>Thanks & Regard</span> <br><span>Prashant Tripathi</span></p>"

                				}
                		]
                }
                result = mailjet.send.create(data=data)
                print(result.status_code)
                # print(result.json())



def alert():
    mydb = connection()
    alert_mail(mydb)
    update_db(mydb)

if __name__ == '__main__':
    alert()
