Ben Thomas - Twich Sentiment Analysis Chatbot 
**Twitch Disposition**
===============================

# **About**

**"Twitch Disposition"** is a **Twich Chatbot** that performs sentimental analysis on the chat in a given Twitch channel. The bot connects to twitch chat through Twitch's Chat API and applies **VADER** (Valence Aware Dictionary and sEntiment Reasoner) within the **Natural Language Toolkit**. The application is presented through "PyQtGraph", a pure-Python graphics library for PyQt. PyQtGraph leverages the GUI toolkit PyQt5 and the scientific computing package NumPy. 

### VADER

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
Sentiment Analysis of Social Media Text. Eighth International Conference on
Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media. It is fully open-sourced under the [MIT License](http://choosealicense.com/).

### Natural Language Toolkit (NLTK)

[NLTK](http://www.nltk.org/) is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.

Thanks to a hands-on guide introducing programming fundamentals alongside topics in computational linguistics, plus comprehensive API documentation, NLTK is suitable for linguists, engineers, students, educators, researchers, and industry users alike. NLTK is available for Windows, Mac OS X, and Linux. Best of all, NLTK is a free, open source, community-driven project.

### PyQtGraph

[PyQtGraph](http://www.pyqtgraph.org/) is a pure-python graphics and GUI library built on [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) / PySide and [numpy](http://www.numpy.org/). It is intended for use in mathematics / scientific / engineering applications. Despite being written entirely in python, the library is very fast due to its heavy leverage of numpy for number crunching and Qt's GraphicsView framework for fast display. PyQtGraph is distributed under the MIT open-source license. 

Copyright (c) 2012  University of North Carolina at Chapel Hill
Luke Campagnola (luke.campagnola@gmail.com)

#### Directory Structure

All project files are located in the **"src"** source folder.
The **"pyqtgraph"** folder holds the pyqtgraph graphics library utilized.

* **Run.py** is the implementation of the program. It initializes and updates the graphics window while maintaing the twitch chatbot connection.  
* **Settings.py** holds the twitch chat API settings like host name, port #, API authentification number, channel to connect to, etc. 
* **Socket.py** creates the socket object that provides the communication mechanism between script and IRC channel. 
* **Start.py** contains the function for the twitch bot to join chat room. 
* **Tools.py** contains the analysis tools that the bot applies to chat entries. These include simple tasks like findind out which user said what and complicated tasks like applying VADER to messages. 
* **Vader.py** is the lexicon and rule-based sentiment analysis tool that analyzes text samples and spits out metrics. Open sourced under MIT license. 
* **vader_sentiment_lexicon.txt** is the word bank the VADER tool relys on for evaluating messages. For expample if the word "hate" is fed through VADER tool, it will find the word in the lexicon.txt file and see that it is associated with negativity. 

## How to "Run" 

Twitch Disposition is not compiled into an executable. The best way to run the program is to open the "src" folder in your Python IDE of choice. From here there are three steps to get the program running. 
1. Edit the "CHANNEL" variable "Settings.py" file to match the twitch streamer whose chat room you would like to analyze. NOTE the channel name needs to be in all lowercase. 
2. Ensure you have all the dependent packages for your Python Interpreter (PyQt5, nltk, numpy).
3. Run the "Run.py" file. 
When you are finished stop the script through your Python IDE. 

#### Contributing

Anyone is welcome to re-use the code used in this project.

#### References

* [Python](https://www.python.org/)
* [Twitch API](https://dev.twitch.tv/)
* [NLTK](http://www.nltk.org/)
* [VADER](https://github.com/cjhutto/vaderSentiment)
* [PyQtGraph](http://www.pyqtgraph.org/)

#### Contact Me

For any questions please email me at _bthomas2622@gmail.com_

#### License

The content of this repository is not licensed. 