from Vader import SentimentIntensityAnalyzer
from nltk import tokenize
import nltk
nltk.download('punkt')

#Read functions
def getUser(line):
    parsedLine = line.split(":", 2)
    #print(parsedLine)
    user = parsedLine[1].split("!", 1)[0]
    return user

def getMessage(line):
    separate = line.split(":", 2)
    #print(separate)
    message = separate[2]
    return message

def textAnalysis(history, volume):
    sentences = [] #master sentence list for a sample chat analysis
    sid = SentimentIntensityAnalyzer()
    intensity = 0.0 #sentiment intensity, known as compound in VADER
    pos = 0.0 #sentiment positivity
    neg = 0.0 #sentiment negativity
    neu = 0.0 #sentiment nuetrality
    for message in history:
        sent_list = tokenize.sent_tokenize(message) #sent_tokenize takes a paragraph and turns i into list of sentences
        sentences.extend(sent_list)
    for sentence in sentences:
        print(sentence)
        ss = sid.polarity_scores(sentence)
        intensity += ss["compound"]
        neu += ss["neu"]
        neg += ss["neg"]
        pos += ss["pos"]
        # for k in sorted(ss):
        #     print('{0}: {1}, '.format(k, ss[k]), end='')
        # print()
    return intensity/len(sentences), neu/len(sentences), neg/len(sentences), pos/len(sentences) #returning the average values of sentiment for inputted text
