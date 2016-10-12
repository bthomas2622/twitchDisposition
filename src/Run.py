"""
Created on Oct 11, 2016
@author: bthom
"""
import time
import re
from Socket import openSocket
from Start import joinRoom
from Settings import RATE

#create socket to send information and receive information from chat
s = openSocket()
joinRoom(s)

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0)  # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
        # for pattern in cfg.PATT:
        #     if re.match(pattern, message):
        #         ban(s, username)
        #         break
        time.sleep(1/RATE)