import time
from Socket import sendMessage

def joinRoom(s):
    response = ""
    #print("test")
    loading = True
    while loading:
        response = response + s.recv(1024).decode("utf-8")
        temp = str.split(response, "\n")
        response = temp.pop()
        time.sleep(0.1)
        print("loading")

        for line in temp:
            print(line)
            loading = loadingComplete(line)
    # sendMessage(s, "Successfully joined chat")


def loadingComplete(line):
    if ("End of /NAMES list" in line):
    #if (">" in line):
        return False
    else:
        return True