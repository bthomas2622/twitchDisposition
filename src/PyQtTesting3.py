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
from multiprocessing import Process, Manager
import collections

#PyQtGraph Setup
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import sys

class grapher():
    def __init__(self):

        #pyqtgraph stuff
        self.app = QtGui.QApplication([])

        #QtGui
        # app = QtGui.QApplication([])

        #Widget to hold everything
        self.w = QtGui.QWidget()

        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle('Twitch Disposition')
        self.win.resize(800, 800)

        self.p1 = self.win.addPlot(title="Net Sentiment")
        self.p2 = self.win.addPlot(title="Neutrality")
        self.win.nextRow()
        self.p3 = self.win.addPlot(title="Negativity")
        self.p4 = self.win.addPlot(title="Positivity")
        self.p1.setYRange(-1.25, 1.25, padding=0)
        self.p1.setLabel("bottom", "Chat")
        self.p2.setYRange(-.25, 1.25, padding=0)
        self.p3.setYRange(-1.25, .25, padding=0)
        self.p4.setYRange(-.25, 1.25, padding=0)
        # data1 = np.random.normal(size=10)
        self.data1 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.data2 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.data3 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.data4 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.curve1 = self.p1.plot(self.data1)
        self.curve2 = self.p2.plot(self.data2)
        self.curve3 = self.p3.plot(self.data3)
        self.curve4 = self.p4.plot(self.data4)
        self.ptr1 = 0

        self.layout = QtGui.QGridLayout()
        self.w.setLayout(self.layout)

        self.layout.addWidget(self.win, 0, 0)

        self.w.show()

    # def update(self, net, neu, neg, pos, msgCacheLength):
    #     print("Net: " + str(net) + " Neu: " + str(neu) + " Neg: " + str(neg))
    #     # data1[:-1] = data1[1:]  # shift data in the array one sample left
    #     self.data1 = np.roll(self.data1, -1) #shift data in the array one to the left
    #     self.data2 = np.roll(self.data2, -1) #shift data in the array one to the left
    #     self.data3 = np.roll(self.data3, -1) #shift data in the array one to the left
    #     self.data4 = np.roll(self.data4, -1) #shift data in the array one to the left
    #     self.data1[self.data1.shape[0] - 1] = net #replace oldest data point with new value, shape of an array is a tuple of integers giving the size of the array along each dimension. this is 1 dimension array
    #     self.data2[self.data2.shape[0] - 1] = neu
    #     self.data3[self.data3.shape[0] - 1] = neg*(-1.0)
    #     self.data4[self.data4.shape[0] - 1] = pos
    #     self.ptr1 += msgCacheLength #increment the plot by the volume of messages received
    #     # print(data1)
    #     # print(data2)
    #     # print(data3)
    #     # print(data4)
    #     self.curve1.setData(data1)
    #     self.curve1.setPos(ptr1,0)
    #     self.curve2.setData(data2)
    #     self.curve2.setPos(ptr1, 0)
    #     self.curve3.setData(data3)
    #     self.curve3.setPos(ptr1, 0)
    #     self.curve4.setData(data4)
    #     self.curve4.setPos(ptr1, 0)
    #     self.app.processEvents()

    def twitchBot(self):
        #create socket to send information and receive information from chat
        s, self.connected = openSocket()
        print(self.connected)
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
        def wrapper(self):
            self.connected = False

        self.btn = QtGui.QPushButton('press me')
        self.btn.clicked.connect(wrapper(self))
        self.layout.addWidget(self.btn, 1, 0)

        while self.connected:
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
                self.update(self, netAvg, neuAvg, negAvg, posAvg, CACHE)
                self.data1 = np.roll(self.data1, -1)  # shift data in the array one to the left
                self.data2 = np.roll(self.data2, -1)  # shift data in the array one to the left
                self.data3 = np.roll(self.data3, -1)  # shift data in the array one to the left
                self.data4 = np.roll(self.data4, -1)  # shift data in the array one to the left
                self.data1[self.data1.shape[0] - 1] = netAvg  # replace oldest data point with new value, shape of an array is a tuple of integers giving the size of the array along each dimension. this is 1 dimension array
                self.data2[self.data2.shape[0] - 1] = neuAvg
                self.data3[self.data3.shape[0] - 1] = negAvg * (-1.0)
                self.data4[self.data4.shape[0] - 1] = posAvg
                self.ptr1 += CACHE  # increment the plot by the volume of messages received
                # print(data1)
                # print(data2)
                # print(data3)
                # print(data4)
                self.curve1.setData(self.data1)
                self.curve1.setPos(self.ptr1, 0)
                self.curve2.setData(self.data2)
                self.curve2.setPos(self.ptr1, 0)
                self.curve3.setData(self.data3)
                self.curve3.setPos(self.ptr1, 0)
                self.curve4.setData(self.data4)
                self.curve4.setPos(self.ptr1, 0)
                #pg.QtGui.QApplication.processEvents()
                self.app.processEvents()

    def run(self):
        self.twitchBot

if __name__ == '__main__':
    m = grapher()
    m.twitchBot()