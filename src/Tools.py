from Vader import SentimentIntensityAnalyzer
from nltk import tokenize
import nltk
nltk.download('punkt')

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
    sentences = [] #master sentence list for a sample chat analysis
    sid = SentimentIntensityAnalyzer()
    for message in history:
        sent_list = tokenize.sent_tokenize(message) #sent_tokenize takes a paragraph and turns i into list of sentences
        sentences.extend(sent_list)
    for sentence in sentences:
        print(sentence)
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            print('{0}: {1}, '.format(k, ss[k]), end='')
        print()
    return
