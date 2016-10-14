"""
Created on Oct 11, 2016
@author: bthom
"""
import socket
from Settings import HOST, PORT, PASS, USER, CHANNEL

#open socket function to allow "Run" function to call on connection
'''
Sockets provide the communication mechanism between two computers using TCP.
A client program creates a socket on its end of the communication and attempts to connect that socket to a server.
When the connection is made, the server creates a socket object on its end of the communication.
'''
def openSocket():
    try:
        s = socket.socket()
        s.connect((HOST, PORT))
        #s.send("PASS " + PASS + "\r\n")
        s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
        #s.send("NICK?" + USER + "\r\n")
        s.send("NICK {}\r\n".format(USER).encode("utf-8"))
        #s.send("JOIN #" + CHANNEL + "\r\n")
        s.send("JOIN # {}\r\n".format(CHANNEL).encode("utf-8"))
        return s, True
    except Exception as e:
        print(str(e))
        return False, False

#bot greets chat
def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message #will look like "PRIVMSG #freebrunch :message"
    #send is a standard socket function
    s.send((messageTemp + "\r\n").encode("utf-8"))
    print("Sent: " + messageTemp)