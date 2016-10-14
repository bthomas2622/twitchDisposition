#Read functions
def getUser(line):
    parsedLine = line.split(":", 2)
    print(parsedLine)
    user = parsedLine[1].split("!", 1)[0]
    return user

def getMessage(line):
    separate = line.split(":", 2)
    print(separate)
    message = separate[2]
    return message