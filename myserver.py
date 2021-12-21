import socket as sock
import sys
from _thread import *
import pickle
import pandas as pd
import csv

symptoms=['fever','diarrhea','heartburn','breathing difficulty',
          'vomiting','sneezing', 'abdominal pain', 'headache', 'skin rash']
df= pd.DataFrame(columns = ['name','host', 'symptoms','heart rate',
                            "temp","blood pressure"])


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



def client_thread(connection,address,df):
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
    print(request)
    vital_signs=["heart rate =65 ","temp=35" ,"blood_pressure=180/60"]
    if request[0] == "d":
        while True:
            client.settimeout(20)
            request=connection.recv(1024)
            client.settimeout(None)
            suffer=pickle.loads(request)
            add=[str(address)]
            suff=[str(suffer)]            
            l=pd.DataFrame(list(zip([name],add,suff,[vital_signs[0]],
                                    [vital_signs[1]],[vital_signs[2]])),
                           columns=['name','host','symptoms','heart rate',
                                    "temp","blood pressure"])
            df=df.append(l)
            print(df) 
            with open(r'clients.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(df)
            diagnose(suffer)
            
            break
        
    elif request[0] =="c":
        client.send('you are now talking with real Doctor say hi'.encode('utf-8'))
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
    
        # df.to_csv(r"C:\Users\lenovo\Desktop\tcp_serverclients.csv")
    print("connection of this client is closed")
    connection.close()
    
server.listen(5)
while True:
    
    client,addr=server.accept()
    ThreadCount+=1
    print("client connected from\n",addr)
    start_new_thread(client_thread,(client,addr,df))
    
    print(f"the total no of client in server :: {ThreadCount}")



server.close()    

