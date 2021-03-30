import os
import sys

import dotenv
import mysql.connector

from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_cors import CORS

dotenv.load_dotenv()
def connection():
    mydb = mysql.connector.connect(
    host=os.getenv('mysql_host'),
    user=os.getenv('mysql_user'),
    password=os.getenv('db_pwd'),
    database=os.getenv('db')
    )
    return mydb

def flask(mydb):
    cursor=mydb.cursor()
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def index():
        return redirect('https://dev2108.github.io/amazon_reg.form/')
    @app.route('/prod_details')
    def prod_details():
        cursor.execute("SELECT * FROM `Products` ORDER BY `product_id`")
        data = cursor.fetchall()
        return jsonify(data)

    @app.route('/success/')
    def success():
        return render_template('reg_success.html')

    @app.route('/register',methods = ['POST'])
    def register():
       if request.method == 'POST':
          email= request.form['email']
          pid=request.form['products']
          threshold=request.form['threshold']
          mobile=request.form['mobile']
         
          query='''INSERT INTO `alert` (`user_email`,`product_id`,`threshold`,`phone_no`) VALUES (%s,%s,%s,%s)'''
          cursor.execute(query,(email,pid,threshold,mobile))
          mydb.commit()
          return redirect(url_for('success'))
       else:
          return redirect(url_for('success'))

    @app.route('/price_details/<int:pid>/<int:interval>')
    def price_details(pid,interval):
        cursor.execute('''SELECT (SELECT `listed_price` FROM `Price` WHERE `product_id` =%s ORDER BY `date_time` DESC LIMIT 1 ) AS `latest_price`,
                        MAX(`listed_price`) AS `highest_price`, MIN(`listed_price`) AS `lowest_price` FROM `Price`
                        WHERE `product_id`=%s AND `date_time` > NOW() - INTERVAL %s DAY ;''',(pid,pid,interval,))
        data = cursor.fetchall()
        return jsonify(data)

    @app.route('/plot_price/<int:pid>/<int:interval>')
    def price_analysis(pid,interval):
        cursor.execute('''SELECT `listed_price`,`date_time` FROM `Price` WHERE `date_time` > NOW() - INTERVAL %s DAY AND `product_id` = %s;
        ''',(interval,pid,))
        data=cursor.fetchall()
        return jsonify(data)

    return app

if __name__ == '__main__':
    mydb=connection()
    app=flask(mydb)
    app.run()