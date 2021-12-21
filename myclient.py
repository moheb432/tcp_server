import socket as sock
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUiType
import os
from os import path
import pickle
name=[]


target_host="127.0.0.1"
target_port=5555
THIS_FOLDER= path.dirname(path.abspath(__file__))
DIAGNOSE_CLASS,_=loadUiType(path.join(THIS_FOLDER, "diagnose.ui"))
MAIN_CLASS,_=loadUiType(path.join(THIS_FOLDER, "main.ui"))
CHAT_CLASS,_=loadUiType(path.join(THIS_FOLDER, "chat.ui"))


class Main(QtWidgets.QMainWindow,MAIN_CLASS):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.diagnose.clicked.connect(lambda:self.diagnose_pushButton_clicked())
        self.chat.clicked.connect(lambda:self.chat_pushButton_clicked())

    def diagnose_pushButton_clicked(self):
        
        name.append(self.name.toPlainText())
        
        Diagnose(self).show()
        self.close()

    def chat_pushButton_clicked(self):
        name.append(self.name.toPlainText())
       
        Chat(self).show()
        self.close()


class Diagnose(QtWidgets.QMainWindow,DIAGNOSE_CLASS):
    def __init__(self,parent=None):
        super(Diagnose,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_UI()
        
        self.client=0
        self.payload=[]
        
        self.start()
        
    def handle_UI(self):

        self.yes.setEnabled(False)
        self.no.setEnabled(False)
        self.fever.setEnabled(True)
        self.headache.setEnabled(True)
        self.diarrhea.setEnabled(True)
        # self.breathing_difficulty.setEnabled(True)
        self.vomiting.setEnabled(True)
        self.heartburn.setEnabled(True)
        self.sr.setEnabled(True)
        self.ab.setEnabled(True)
        #self.showDiagnose.setEnabled(False)

        #self.startbutton.clicked.connect(lambda :self.start())
        self.yes.clicked.connect(lambda :self.yesClicked())
        self.no.clicked.connect(lambda :self.noClicked())
        self.fever.clicked.connect(lambda :self.add("fever"))
        self.headache.clicked.connect(lambda :self.add("headache"))
        self.diarrhea.clicked.connect(lambda :self.add("diarrhea"))
        self.vomiting.clicked.connect(lambda :self.add("vomiting"))
        self.sneezing.clicked.connect(lambda :self.add("sneezing"))
        self.heartburn.clicked.connect(lambda :self.add("heartburn"))
        
        self.sr.clicked.connect(lambda :self.add("sneezing"))
        self.ab.clicked.connect(lambda :self.add("abdominal pain"))
        
        #self.showDiagnose.clicked.connect(lambda :self.send())

        
        
    def start(self):
        try:
            client_socket=sock.socket(sock.AF_INET,sock.SOCK_STREAM)
        except sock.error as err:
            self.browser.append("FAILED to create client")
            self.browser.append("Reason:"+str(err)) 
            sys.exit()

        try:
            client_socket.connect((target_host,target_port))
            self.browser.append("client is connected")
            self.client=client_socket

        except sock.error as err:
            self.browser.append("FAILED to connect client")
            self.browser.append("Reason:"+str(err))
            sys.exit()
        l=['d',name[0]]    
        self.client.send(pickle.dumps(l))
        self.browser.append("What do you feel?")


    def send(self):    
        data=pickle.dumps(self.payload)
        self.client.send(data)

    def recieve(self):     
        respond=self.client.recv(1024)
        respond=respond.decode("utf-8")
        self.browser.append(respond)
        self.browser.append("connection closed")
        self.client.close()

        
    
    def add(self,disease):

        if (disease in self.payload):
            self.browser.append("you already have chosen this")

        else:    
            self.payload.append(disease)
            self.browser.append(disease)

        self.fever.setEnabled(False)
        self.headache.setEnabled(False)
        self.diarrhea.setEnabled(False)
        self.sneezing.setEnabled(False)
        self.vomiting.setEnabled(False)
        self.heartburn.setEnabled(False)
        self.browser.append("Anything else?")
        self.yes.setEnabled(True)
        self.no.setEnabled(True)
        self.sr.setEnabled(False)
        self.ab.setEnabled(False)
        
    
    def yesClicked(self):
        self.fever.setEnabled(True)
        self.headache.setEnabled(True)
        
        self.diarrhea.setEnabled(True)
        self.sneezing.setEnabled(True)
        self.vomiting.setEnabled(True)
        self.heartburn.setEnabled(True)
        self.sr.setEnabled(True)
        self.ab.setEnabled(True)
        self.yes.setEnabled(False)
        self.no.setEnabled(False)

    def noClicked(self):
        self.yes.setEnabled(False)
        self.no.setEnabled(False)
        #self.payload.append('0')
        self.send()
        self.recieve()
        



class Chat(QtWidgets.QMainWindow,CHAT_CLASS):
    def __init__(self,parent=None):
        super(Chat,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.start()

        self.exit.clicked.connect(lambda :self.exitClicked())
        self.chatbox.returnPressed.connect(lambda: self.sendreply())
        self.refresh.clicked.connect(lambda: self.recieveClicked())
        self.back.clicked.connect(lambda: self.backClicked())
        self.back.hide()

    def start(self):
        try:
            client_socket=sock.socket(sock.AF_INET,sock.SOCK_STREAM)
        except sock.error as err:
            self.browser.append("FAILED to create client")
            self.browser.append("Reason:"+str(err))
            sys.exit()

        try:
            client_socket.connect((target_host,target_port))
            self.browser.append("client is connected")
            self.client=client_socket

        except sock.error as err:
            self.browser.append("FAILED to connect client")
            self.browser.append("Reason:"+str(err))
            sys.exit()
        
        self.client.send("c".encode("utf-8")) 
        respond=self.client.recv(1024)
        respond=respond.decode("utf-8")
        self.browser.append(str(respond))

    def exitClicked(self):
        self.client.send("f".encode("utf-8")) 
        self.browser.append("connection closed")
        self.client.close()
        self.exit.hide()
        self.chatbox.hide()
        self.refresh.hide()
        self.back.show()

    def backClicked(self):
        Main(self).show()
        self.close()


    def sendreply(self):
        reply = self.chatbox.text()
        self.chatbox.setText('')
        self.browser.append(reply)
        self.client.send(reply.encode("utf-8")) 

    def recieveClicked(self):
        respond=self.client.recv(1024)
        respond=respond.decode("utf-8")
        self.browser.append(str(respond))
      
def main():
    app = QtWidgets.QApplication(sys.argv)
    window= Main()
    window.show()  
    app.exec_() 


if __name__ == '__main__':
    main()

# client =sock.socket(sock.AF_INET,sock.SOCK_STREAM)

# client.connect(('127.0.0.1', 5555))

# while True:

#     request= str(input())

#     request=request.encode('ascii')

#     client.send(request)

#     response=client.recv(512)

#     response=response.decode('ascii')

#     print(response)

   


# #     client.close()
#  more=input("anything else?")

#                 if more.lower() == 'y':
#                     payload=str(input("what do you feel"))
#                 elif more.lower() == 'n':
#                     payload="n"
#                     client.send(payload.encode("utf-8"))
#                     respond=client.recv(1024)
#                     print(str(respond))
#                     break