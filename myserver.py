import socket as sock
import sys
from _thread import *
import pickle
import pandas as pd
import csv
import os
from os import path
from csv import DictWriter
import datetime

THIS_FOLDER= path.dirname(path.abspath(__file__))


symptoms=['fever','diarrhea','heartburn','breathing difficulty',
          'vomiting','sneezing', 'abdominal pain', 'headache', 'skin rash']
          
field_names = ['Name','Address','Date','Time' ,'Symptoms','Heart Rate',
                            "Temp","Blood Pressure"]


try:
    server =sock.socket(sock.AF_INET,sock.SOCK_STREAM)
except sock.error as err:
    print("FAILED to create server")
    print("Reason:"+str(err))
    sys.exit()


target_host="127.0.0.1"
target_port=5555
ThreadCount=0

try:
    server.bind((target_host,target_port)) 
    print("Server is ON")

except sock.error as err:
    print("FAILED to bind server")
    print("Reason:"+str(err))
    sys.exit()


def diagnose(s):
    if len(s) == len(symptoms):
         client.send('you may have covid-19 please Consult a doctor ASAP '.encode('utf-8'))
    elif len(s) > 1:
        if'heartburn' and 'diarrhea' and 'vomiting' in s:
             client.send('you had Food poisoning or intestines infection suggested pill : Sulfatrim '.encode('utf-8'))
        elif 'fever' and 'vomiting' in s:
             client.send('you had stomach flu suggested pill : promethazine '.encode('utf-8'))
        elif 'breath difficulty' and 'vomiting' and 'diarrhea' in s:
             client.send('you had Fever food poison and Asthma suggested pill : antinnal and Zithromax '.encode('utf-8'))    
        elif 'fever' and 'abdominal pain' and 'diarrhea' in s:
             client.send('you had Colon inflammation suggested pill : Spasmomen '.encode('utf-8'))
        elif 'sneezing' and 'skin rash' and 'abdominal pain' in s:
             client.send('you had Allergy suggested pill : Zyrtec '.encode('utf-8'))     
        elif 'heartburn' and 'breathing difficulty' in s:
             client.send('you had Acid reflux suggested pill : lansoprazole '.encode('utf-8'))         
        elif 'breathing difficulty' and 'vomiting' in s:
             client.send('you had Panick attack suggested pill : Zithromax '.encode('utf-8'))
        elif 'fever' and 'headache' in s:
             client.send('you had Flu or Viral infection suggested pill : Panadol or Paracetamol '.encode('utf-8'))
        else:
             client.send('Diagnosis not found'.encode('utf-8'))
    elif len(s)==1 :
        if 'headache' in s:
             client.send('suggested pill : Panadol '.encode('utf-8'))
        elif 'fever' in s:
             client.send('suggested pill : Paracetamol '.encode('utf-8'))
        elif 'vomiting' in s:
             client.send('suggested pill : Motilium '.encode('utf-8'))
        elif 'diarrhea' in s:
             client.send('suggested pill : Antinal '.encode('utf-8'))
        elif 'heartburn' in s:
             client.send('suggested pill : lansoprazole '.encode('utf-8'))
        elif 'breathing difficulty' in s:
             client.send('suggested pill : Zithromax '.encode('utf-8'))
        elif 'skin rash' in s:
             client.send('suggested pill : Zyrtec '.encode('utf-8'))
        elif 'sneezing' in s:
             client.send('suggested pill : Zyrtec '.encode('utf-8'))
        elif 'abdominal pain' in s:
             client.send('suggested pill : Buscopan '.encode('utf-8'))
        else:
             client.send('Diagnosis not found'.encode('utf-8'))



def client_thread(connection,address):
     """"client thread 
     is function take 3 args 
     connection which is the client it self 
     address  it is the address of the client
     df is dataframe contain the statues of the former clients
     this function just get response(symptoms) form the client
     and add them into a list to send them to diagnose function
     """

     suffer=[]
     request=connection.recv(1024)
     request=pickle.loads(request)
     name=request[1]

     vitals=request[2]

     date=datetime.datetime.now().strftime('%Y-%m-%d')
     time=datetime.datetime.now().strftime('%I:%M %p')
     add=[str(address)]


     print(request)

     if request[0] == "d":
          client.send(('Hello {}, I am your DocBot\n Please,choose one symptom '.format(name)).encode('utf-8'))
          while True:
               client.settimeout(20)
               request=connection.recv(1024)
               client.settimeout(None)
               suffer=pickle.loads(request)
               suff=[str(suffer)] 
               
               data={'Name':name,'Address':add,"Date":date,"Time":time,'Symptoms':suff,'Heart Rate':vitals[0],'Temp':vitals[1],'Blood Pressure':vitals[2]}

               #df=df.append(l)
               print(data)

               try:
                    with open((path.join(THIS_FOLDER, "clients.csv")), 'a') as f:

                         dictwriter_object = DictWriter(f, fieldnames=field_names)
                         dictwriter_object.writerow(data)
               except:
                    print("There's a problem with saving the data, kindly try close the csv file if opened and check the field names")

               diagnose(suffer)

               break
        
     elif request[0] =="c":
          client.send(('Hello {},you are now talking with real Doctor, say hi'.format(name)).encode('utf-8'))
          while True:
               client.settimeout(20)
               request=connection.recv(1024)
               client.settimeout(None)
               request=request.decode("utf-8")
               if request=="f":
                    print("chat is closed")
                    break
               else:
                    print(request)
                    reply=str(input())
                    reply=reply.encode('utf-8')
                    client.send(reply)


          data={'Name':name,'Address':add,"Date":date,"Time":time,'Symptoms':"Discussed With Doctor",'Heart Rate':vitals[0],'Temp':vitals[1],'Blood Pressure':vitals[2]}
          print(data)

          try:
               with open((path.join(THIS_FOLDER, "clients.csv")), 'a') as f:

                    dictwriter_object = DictWriter(f, fieldnames=field_names)
                    dictwriter_object.writerow(data)
                    print("Data are Saved")
          except:
               print("There's a problem with saving the data, kindly try close the csv file if opened and check the field names")

               print("connection closed")
               connection.close()
    
server.listen(5)
while True:
    
    client,addr=server.accept()
    ThreadCount+=1
    print("client connected from\n",addr)
    start_new_thread(client_thread,(client,addr))
    
    print(f"the total no of client in server :: {ThreadCount}")



server.close()    

