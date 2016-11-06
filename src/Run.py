"""
Created on Oct 11, 2016
@author: Ben Thomas
"""
import time
from Socket import openSocket
from Start import joinRoom
from Settings import RATE, CACHE
from Tools import getUser, getMessage, textAnalysis
from Socket import sendMessage

#PyQtGraph Setup
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys

win = pg.GraphicsWindow()
win.setWindowTitle('Twitch Disposition')
win.resize(800, 800)

p1 = win.addPlot(title="Intensity")
p2 = win.addPlot(title="Neutrality")
p3 = win.addPlot(title="Negativity")
p4 = win.addPlot(title="Positivity")
p1.setYRange(-1.25, 1.25, padding=0)
p1.setLabel("bottom", "Chat")
p2.setYRange(-.25, 1.25, padding=0)
p3.setYRange(-.25, 1.25, padding=0)
p4.setYRange(-.25, 1.25, padding=0)
data1 = np.random.normal(size=10)
data2 = np.random.normal(size=10)
data3 = np.random.normal(size=10)
data4 = np.random.normal(size=10)
curve1 = p1.plot(data1)
curve2 = p2.plot(data2)
curve3 = p3.plot(data3)
curve4 = p4.plot(data4)
ptr1 = 0

def update(net, neu, neg, pos):
    global data1, data2, data3, data4, curve1, curve2, curve3, curve4, ptr1
    data1[:-1] = data1[1:]  # shift data in the array one sample left
    data2[:-1] = data2[1:]
    data3[:-1] = data3[1:]
    data4[:-1] = data4[1:]
    # (see also: np.roll)
    data1[-1] = net
    data2[-1] = neu
    data3[-1] = neg
    data4[-1] = pos
    ptr1 += 1
    curve1.setData(data1)
    curve1.setPos(ptr1,0)
    curve2.setData(data2)
    curve2.setPos(ptr1, 0)
    curve3.setData(data3)
    curve3.setPos(ptr1, 0)
    curve4.setData(data4)
    curve4.setPos(ptr1, 0)

#create socket to send information and receive information from chat
s, connected = openSocket()
print(connected)
joinRoom(s)
response = ""
netTotal = 0.0
neuTotal = 0.0
negTotal = 0.0
posTotal = 0.0
avgTotal = 0.0
netAvg = 0.0
neuAvg = 0.0
negAvg = 0.0
posAvg = 0.0
start = time.time()
avgElapsedBtwnMessageList = [5, 5, 5, 5, 5]

messageHistory = [] #list to hold messages for analysis

while connected:
    print("running")
    response = response + s.recv(1024).decode("utf-8")
    temp = str.split(response, "\n")
    response = temp.pop()
    print("Temp: " + str(temp))
    #if response == "PING :tmi.twitch.tv\r\n":
    if temp[0] == "PING :tmi.twitch.tv\r":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("PONG'ed")
    else:
        print("else")
        end = time.time()
        elapsedBtwnMessage = end - start
        avgElapsedBtwnMessageList.append(elapsedBtwnMessage)
        avgElapsedBtwnMessageList.pop(0)
        start = time.time()
        print("Time between last message: " + str(elapsedBtwnMessage))
        print(str("Last 5 time between messages: " + str(avgElapsedBtwnMessageList)))
        avgElapsedBtwnMessage = (sum(avgElapsedBtwnMessageList)/len(avgElapsedBtwnMessageList)*1.0)
        if avgElapsedBtwnMessage > 5:
            CACHE = 1
        elif elapsedBtwnMessage < 0.1:
            CACHE = 1
        elif avgElapsedBtwnMessage < 0.5:
            CACHE = 1
        else:
            CACHE = 1
        print("Message history cache length: " + str(CACHE))
        for line in temp:
            print("Line " + line)
            user = getUser(line)
            message = getMessage(line)
            messageHistory.append(message)
            if len(messageHistory) >= CACHE:
                netAvg, neuAvg, negAvg, posAvg = textAnalysis(messageHistory, CACHE)
                #update(negAvg)
                avgTotal += 1 #the number of averages done for the total average of averages, the netAvg is the average emotion of a specific sample set for example. -1 being the most negative and 1 being the most positive. netTotal is all the netAvgs summed
                netTotal += netAvg
                neuTotal += neuAvg
                negTotal += negAvg
                posTotal += posAvg
                messageHistory.clear()
                print("Avg Net Emotion: " + str(netAvg) + "  Avg Neutrality: " + str(neuAvg) + "  Avg Negativity: " + str(negAvg) + "  Avg Positivity: " + str(posAvg))
                print("Total Avg Net Emotion: " + str(netTotal/avgTotal) + " Total Avg Neutrality: " + str(neuTotal/avgTotal) + " Total Avg Negativity: " + str(negTotal/avgTotal) + " Total Avg Positivity: " + str(posTotal/avgTotal))
            print(user + " typed: " + message)
        update(netAvg, neuAvg, negAvg, posAvg)
        pg.QtGui.QApplication.processEvents()

win.close()