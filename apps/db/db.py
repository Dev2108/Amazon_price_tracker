import mysql.connector

import os
import dotenv
dotenv.load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('mysql_host'),
  user=os.getenv('mysql_user'),
  password=os.getenv('db_pwd'),
  database=os.getenv('db')
)
#create1="CREATE TABLE Products (product_id INT(200) NOT NULL AUTO_INCREMENT, product_Name VARCHAR(255), PRIMARY KEY(product_id))"
#mySql_insert_query = """INSERT INTO Laptop (Id, Name, Price, Purchase_date) 
                        #VALUES 
                        #(10, 'Lenovo ThinkPad P71', 6459, '2019-08-14') """

#sqlselect= "select * from Laptop"
#create2="CREATE TABLE Price (listed_price VARCHAR(255), date_time datetime default now(), product_id INT ,FOREIGN KEY(product_id) REFERENCES Products(product_id ))"
create3="CREATE TABLE `alert` (`user_email` VARCHAR(255) NOT NULL,`product_id` INT NOT NULL,`threshold` INT NOT NULL,FOREIGN KEY (`product_id`) REFERENCES `Products`(`product_id`) )"
mycursor = mydb.cursor()
#mycursor.execute(create1)
#mycursor.execute(create2)
mycursor.execute(create3)


mydb.commit()


mycursor.close()