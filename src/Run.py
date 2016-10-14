"""
Created on Oct 11, 2016
@author: bthom
"""
import time
from Socket import openSocket
from Start import joinRoom
from Settings import RATE
from Tools import getUser, getMessage
from Socket import sendMessage

#create socket to send information and receive information from chat
s, connected = openSocket()
print(connected)
joinRoom(s)
response = ""

while connected:
    print("running")
    response = response + s.recv(1024).decode("utf-8")
    temp = str.split(response, "\n")
    response = temp.pop()
    print(response)
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("PONG'ed")
    else:
        print("else")
        for line in temp:
            print(line)
            user = getUser(line)
            message = getMessage(line)
            print (user + " typed: " + message)
    time.sleep(1/RATE)