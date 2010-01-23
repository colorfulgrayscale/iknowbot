"""
iKnow "bot"
Coded by Tejeshwar Sangameswaran
tejeshwar.s@gmail.com
http://www.colorfulgrayscale.com
"""


"""
!! NOTE: This program uses curses. therefore its not windows compatible
You can port this application to windows using WCurses available at
http://adamv.com/dev/python/curses/ 
"""

import curses
import console
from random import *

#Global variables
currentX = 1
currentY = 2
magicChar = 59 # 59 = ;
finishedChar = 39 # 39 = '
questionPhrases = list()
overlayActivated = False
finishedAnswer = False
currentPhrase = ""
phrasePosition=0
totalPhraseLength=0
answerPhrase = ""

def initInterface():
    #init curses and draw interface.
    global stdscr
    global width
    global height
    (width, height) = console.getTerminalSize()
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.cbreak()
    stdscr.clear()
    stdscr.border(0)
    stringLogo = """
 _ _                           _           _   
(_) | ___ __   _____      __   | |__   ___ | |_ 
| | |/ / '_ \ / _ \ \ /\ / /   | '_ \ / _ \| __|
| |   <| | | | (_) \ V  V /    | |_) | (_) | |_ 
|_|_|\_\_| |_|\___/ \_/\_/     |_.__/ \___/ \__|
                                              
"""    
    stdscr.addstr(1,width/2,stringLogo,curses.A_BLINK)
    #stdscr.addstr(2,(width/2)-5,'The All Knowing Bot',curses.A_DIM)
    stdscr.addstr(8,(width/2)-10,"Tejeshwar Sangam (tsangame@uark.edu)")
    stdscr.refresh()

def breakDownInterface():
    #clean up after curses
    curses.nocbreak()
    stdscr.keypad(0);
    curses.echo()
    curses.endwin()

def drawTextBox():
    #our textbox.
    stdscr.refresh()
    global tbox
    global tboxWidth
    global tboxHeight
    global tboxXpos
    global tboxYpos
    global paddingRight
    global paddingBottom
    tboxXpos = 12
    tboxYpos = 4
    paddingRight = 10
    paddingBottom = 3
    tboxHeight = height-tboxXpos - paddingBottom
    tboxWidth = width - paddingRight
    tbox=stdscr.subwin(tboxHeight, tboxWidth, tboxXpos, tboxYpos)
    tbox.box()
    tbox.addstr(0,1,"Ask me a Question!") #textbox header
    tbox.move(currentY, currentX)
    tbox.refresh()
    stdscr.refresh()

def drawAnswers():
    #answers dialog box
    global tboxWidth
    global tboxHeight
    global answerPhrase
    global tboxXpos
    global tboxYpos
    global paddingRight
    global paddingBottom    
    tbox.clear() # clean up text the user might have entered.
    stdscr.refresh()
    if(answerPhrase.strip()==""):
        answerPhrase = "Sorry, I only answer to TJ"
    if(answerPhrase.strip()=="dd"):
        answerPhrase = "Sorry, I'm afraid I don't know the answer to that question."
    replyTbox=stdscr.subwin(tboxHeight, tboxWidth, tboxXpos, tboxYpos)
    replyTbox.box()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    replyTbox.addstr(0,2,"iKnow bot Replies",curses.color_pair(1)) #reply box header
    replyTbox.addstr(2,2, str(answerPhrase) ,curses.color_pair(2))
    replyTbox.move(2, 1)
    replyTbox.refresh()
    stdscr.refresh()
    buffer = stdscr.getch() #wait for keypress

def addtoTbox(characterEntity):
    #prints text to our textbox
    global currentX
    global currentY
    if(characterEntity == 127): #handle backspaces
        if (currentX >= 2):
            currentX = currentX - 1
            tbox.move(currentY, currentX)
            tbox.refresh()
        return
    tbox.addch(currentY,currentX,characterEntity)
    tbox.refresh()
    if(currentX >= tboxWidth - 3):
        currentX = 1
        if(currentY >= tboxHeight-3):
            tbox.clear()
            drawTextBox()
            currentY = 2
        else: 
            currentY=currentY + 1
    else:    
        currentX = currentX + 1
        
def addOverlayText(characterEntity):
    #prints stalling overlay text
    global phrasePosition
    global totalPhraseLength
    global currentPhrase
    global answerPhrase
    global finishedAnswer 
    if(characterEntity==finishedChar): #if encouterd finished key
        finishedAnswer = True
    if(not finishedAnswer):
        answerPhrase = str(answerPhrase) + str(chr(characterEntity))
    if(phrasePosition>totalPhraseLength-1):
        return
    else:
        if(characterEntity==127): #handle backspace
            answerPhrase = answerPhrase[:-1]
        addtoTbox(ord(currentPhrase[phrasePosition]))
        phrasePosition = phrasePosition + 1
    
def handleText(currentInputChar):
    #handler decides what to do with entered character
    global overlayActivated
    if(currentInputChar==magicChar):
        if(overlayActivated):
            overlayActivated = False
        else:
            overlayActivated = True
        return
    #print ": " + str(currentInputChar)
    if(overlayActivated): #if in overlay mode, call overlay function
        addOverlayText(currentInputChar)
    else:
        addtoTbox(currentInputChar)
        
def populatePhrases():
    #list of phrases which are used to stall
    questionPhrases.append("hey iknow bot, my friend here asks the question ")
    questionPhrases.append("i have a question for you iknow bot, ")
    questionPhrases.append("help me answer this question iknow bot, ")
    questionPhrases.append("can you please tell me ")
    questionPhrases.append("my friend here wants to know ")
    questionPhrases.append("sorry to bother you again but ")
    questionPhrases.append("oh all knowing iknow bot, ")
    questionPhrases.append("this crazy person wants to know ")
    questionPhrases.append("please can you help me with this question ")

def initialize():
    #make sure we are adjusting the global values
    global pos
    global currentPhrase
    global totalPhraseLength
    global currentX
    global currentY
    global overlayActivated
    global phrasePosition
    global answerPhrase
    global finishedAnswer
    #setup the environment again
    initInterface()
    populatePhrases()
    drawTextBox()
    #clean up old variables and set back to default values.
    pos = randrange(len(questionPhrases))
    currentPhrase = questionPhrases[pos]
    totalPhraseLength = len(currentPhrase)
    currentX = 1
    currentY = 2
    overlayActivated = False
    finishedAnswer = False
    phrasePosition=0
    answerPhrase = ""
    tbox.move(currentY, currentX)
    stdscr.refresh()
    tbox.refresh()
 
if __name__=='__main__':
    initialize()
    while(True):
        inputChar = stdscr.getch()
        if inputChar == 27: #if 'Esc' key is pressed
            breakDownInterface()
            break
        if inputChar == 10: #if 'Return' key is pressed
            drawAnswers() #show answers
            initialize() #and restart program
        handleText(inputChar) #call text handler with entered text    
