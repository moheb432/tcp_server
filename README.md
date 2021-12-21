
# TCP_SERVER_MEDICAL_CHATBOT
### submitted to: Dr.Eman Marzban & Eng.Eman Ibrahim
### submitted by:
| name | BN |section|
| ------ | ---- |---------
| moheb ashraf shaker | 13 |2
| ahmed khaled hilal | 12 |2
| fatma osama  | 7 |2
| Aya Ehab Saleh  | 18 |1
| karin amir |10  |2

## project 
this project is build using python programing language 
with a socket programming using libraries : 
- pickle as format to send the 
- thread
- socket
## server      
the client fristly write his name then he  can choose between chatting with doctor 
![N|Solid](https://github.com/moheb432/tcp_server/blob/main/capture/cap1.PNG)

or to ask the medical bot for a simple diagnosis according to the following symptoms
- fever
- diarrhea
- heartburn
- breathing difficulty
- vomiting
- sneezing
- skin rash
- abdominal pain
- accoriding to the symptoms the bot can tell the patient about his symtopms and 
 recommend a drug for him

[![N|Solid](https://github.com/moheb432/tcp_server/blob/main/capture/2.PNG)] 
# server securing
> the server is made using scocekt programming TCP/IP method 
> 
> formatting  with pickle and utf-8
> 
> the server is secured using try and except if the client take more than 20 sec to respond
> 
> the server is secured using recv(len) 
> 
> where if the len(data)>1024 the server will forcelly close the client connection 

[![N|Solid](https://github.com/moheb432/tcp_server/blob/main/capture/cap3.PNG)]
 

# clients Dataset
> when client is connected the server saves his ip and port and his nick name as personal info  
> 
> it also record his symtomps and his vital signs heart rate,temp and blood pressure  
>
> then it can retrive this info next time he enter the server
> 

[![N|Solid](https://github.com/moheb432/tcp_server/blob/main/capture/3.PNG)](https://nodesource.com/products/nsolid)
for more info you can visit this [video]
