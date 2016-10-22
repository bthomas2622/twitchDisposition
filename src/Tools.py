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

def textAnalysis(history, volume):
    totalWords = 0.0
    upperCase = 0.0
    lowerCase = 0.0
    for message in history:
        words = message.split(" ")
        totalWords += len(words)
        for word in words:
            if word[0].isupper():
                upperCase += 1
            else:
                lowerCase += 1
    avgWords = round(totalWords / volume, 1)
    capPercentage = int(((upperCase / lowerCase)*100))
    return avgWords, capPercentage
