"""
Created on Oct 11, 2016
@author: bthom
"""
import time
from Socket import openSocket
from Start import joinRoom
from Settings import RATE, CACHE
from Tools import getUser, getMessage, textAnalysis
from Socket import sendMessage

#create socket to send information and receive information from chat
s, connected = openSocket()
print(connected)
joinRoom(s)
response = ""

messageHistory = [] #list to hold messages for analysis

while connected:
    print("running")
    response = response + s.recv(1024).decode("utf-8")
    temp = str.split(response, "\n")
    response = temp.pop()
    print("Temp: " + temp)
    #if response == "PING :tmi.twitch.tv\r\n":
    if temp[0] == "PING :tmi.twitch.tv\r":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("PONG'ed")
    else:
        print("else")
        for line in temp:
            print("Line " + line)
            user = getUser(line)
            message = getMessage(line)
            messageHistory.append(message)
            if len(messageHistory) == CACHE:
                wordCountAvg, capPercent = textAnalysis(messageHistory, CACHE)
                messageHistory.clear()
                print("Average Word Count: " + str(wordCountAvg))
                print("Percent Capitlized: " + str(capPercent) + "%")
            print (user + " typed: " + message)
    time.sleep(1/RATE)