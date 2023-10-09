import sqlite3
from flask import Blueprint, Flask, request, jsonify, render_template,session,send_from_directory,redirect,url_for,send_file
import requests
import json
import datetime
import os

import requests
import json
from bs4 import BeautifulSoup

import random
import string
#from aa import *
from gevent.pywsgi import WSGIServer
from flask_cors import CORS
import random

import textile

from xlrd import open_workbook

import xlwt 
from xlwt import Workbook
import datetime
from datetime import timedelta

import xlsxwriter 
import ast
import csv
import sqlite3






bill_api = Flask(__name__)



conn_bill = sqlite3.connect('bill.db', check_same_thread=False)

conn_bill.execute('''CREATE TABLE IF NOT EXISTS aimDB
         (id INTEGER NOT NULL PRIMARY KEY,
         Datetime timestamp,
         From_Date TEXT,
         To_Date TEXT,
         Name TEXT,
         Current_Unit TEXT,
         Last_Unit TEXT,
         Unit TEXT,
         Rent TEXT,
         Total_Amt TEXT,
         Elec_Bill TEXT
         );''')
conn_bill.commit()




def random_char(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))



@bill_api.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@bill_api.route('/home',methods=['GET','POST'])
def home():
    return render_template('index.html')

@bill_api.route('/insertdata',methods=['GET','POST'])
def insertdata():
    if request.method == "POST":
        From_Date=request.form['From_Date']
        To_Date=str(datetime.datetime.now())
        Name=request.form['Name']
        Current_Unit=request.form['Current_Unit']
        Last_Unit=request.form['Last_Unit']
        Unit=request.form['Unit']
        Rent=request.form['Rent']
        Rent=int(Rent)
        Unit=int(Unit)
        Current_Unit=int(Current_Unit)
        Last_Unit=int(Last_Unit)
        Elec_Bill=Current_Unit-Last_Unit
        Total_Bill=Elec_Bill*Unit
        Total_Bill=int(Total_Bill)
        Total_Amt=Total_Bill+Rent
        Total_Amt=int(Total_Amt)
        conn_bill.execute("INSERT INTO aimDB(Datetime,From_Date,To_Date,Name,Current_Unit,Last_Unit,Unit,Rent,Total_Amt,Elec_Bill) values(?,?,?,?,?,?,?,?,?,?)" ,(str(datetime.datetime.now()),From_Date,To_Date,Name,Current_Unit,Last_Unit,Unit,Rent,Total_Amt,Elec_Bill))
        conn_bill.commit()

        import re
        
        # Replace colons and periods in the To_Date variable with underscores
        To_Date = re.sub(r'[.:]', '_', To_Date) 
        # file io
        try:
            temp_name='_'+random_char(5)
            filetxtname=temp_name+'sample.txt'
            with open(filetxtname,"w") as k:
                k.write("\t        Binesh Bhati"+"\n")
                k.write("--------------------------------------------------------"+"\n")
                k.write("Noida Sector, Noida(U.P.) - 201301"+"\n")
                k.write("========================================================="+"\n")
                k.write("Date: "+To_Date+"\n")
                k.write("From_Date: "+From_Date+"\n")
                k.write("To_Date: "+To_Date+"\n")
                k.write("Tenant_Name: "+Name+"\n")
                k.write("Current_M_Unit: "+str(Current_Unit)+"\n")
                k.write("Last_M_Unit: "+str(Last_Unit)+"\n")
                k.write("Unit: "+str(Unit)+"\n")
                k.write("Rent: "+str(Rent)+"\n")
                k.write("========================================================="+"\n")
                k.write("Total_Amount: Rs."+str(Total_Amt)+"\n")
                k.write("Electricity_Bill: Rs."+str(Elec_Bill)+"\n")
                k.write("========================================================="+"\n")
                path=filetxtname
            return send_file(path,as_attachment=True)
        except:
            return redirect(url_for("index"))
    return redirect(url_for("index"))







@bill_api.route('/bill/admin', methods=['GET','POST'])
def login():
    if request.method == 'GET':
            return render_template('login_bill.html')

    elif request.method == 'POST':
        if request.form["password"]=="bill2ws":
            try:
                conn = sqlite3.connect('bill.db')
                cursor = conn.cursor()

                # Execute an SQL query to retrieve data from your database
                cursor.execute("SELECT * FROM aimDB ORDER BY ID DESC limit 10")
                data = cursor.fetchall()

                # Close the database connection
                conn.close()

                return render_template('admin.html', data=data)
            except Exception as e:
                print(e,'exception')


        else:
            return render_template('login_bill.html',error="Invalid Login/password")
        


@bill_api.route('/logout')
def logout():
    # return render_template('login_bill.html')
    return redirect(url_for("login"))


@bill_api.route('/bill/admin/downloadexcel', methods=['GET'])
def download_page():
    company='bill'
    a=conn_bill.execute('SELECT * FROM aimDB').fetchall()
    data=[]
    for i in a:
        #print(i)
        # c=i[3].replace("\'", "\"")
        # c=json.loads(c)
        From_Date=i[2]
        To_Date=i[3]
        Name=i[4]
        Current_Unit=i[5]
        Last_Unit=i[6]
        Unit=i[7]
        Rent=i[8]
        Elec_Bill=i[9]
        Total_Bill=i[10]

        #print(Unit)


        data.append({'From_Date':From_Date,'To_Date':To_Date,
                     'Name':Name,'Current_Unit':Current_Unit,'Last_Unit':Last_Unit,
                     'Unit':Unit,'Rent':Rent,'Elec_Bill':Elec_Bill,
                     'Total_Bill':Total_Bill})
        
    wb = Workbook()
    chk=(os.path.isdir("static/BILL_Admin_Excel/"+str(company)))
    #print(chk)
    if chk==False:
        try:
            os.mkdir("static/BILL_Admin_Excel")
        except:
            pass
        try:
            os.mkdir("static/BILL_Admin_Excel/"+str(company))
        except:
            pass

    temp_name='_'+random_char(5)
    workbook = xlsxwriter.Workbook('static/BILL_Admin_Excel/'+company+'/bill'+temp_name+'.xlsx') 
    worksheet = workbook.add_worksheet() 

    worksheet.write(0, 0, 'From_Date') 
    worksheet.write(0, 1, 'To_Date') 
    worksheet.write(0, 2, 'Name')
    worksheet.write(0, 3, 'Current_Unit') 
    worksheet.write(0, 4, 'Last_Unit') 
    worksheet.write(0, 5, 'Unit')
    worksheet.write(0, 6, 'Rent')
    worksheet.write(0, 7, 'Elec_Bill')
    worksheet.write(0, 8, 'Total_Bill')
  

    count=1

    for k in data:
        worksheet.write(count, 0, k['From_Date'])
        worksheet.write(count, 1, k['To_Date'])
        worksheet.write(count, 2, k['Name'])
        worksheet.write(count, 3, k['Current_Unit'])
        worksheet.write(count, 4, k['Last_Unit'])
        worksheet.write(count, 5, k['Unit'])
        worksheet.write(count, 6, k['Rent'])
        worksheet.write(count, 7, k['Elec_Bill'])
        worksheet.write(count, 8, k['Total_Bill'])

        count=count+1

    workbook.close()

    return jsonify({'filename':'/static/BILL_Admin_Excel/'+company+'/bill'+temp_name+'.xlsx'})
    # return render_template('admin.html')






























if (__name__ == "__main__"):
    # http = WSGIServer(('0.0.0.0',7000), bill)
    # http.serve_forever()
    bill_api.run(debug=False, host='0.0.0.0')