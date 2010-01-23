'''
Created on Jan 20, 2010
'''

import curses
import console

(width, height) = console.getTerminalSize()
middleX = width/2
middleY = height/2
padHeight = 10
padWidth = 70
screen = curses.initscr()
curses.start_color()

pad = curses.newpad(padHeight,padWidth)

def drawScreen():
    """Draw screen components"""
    screen.addstr(2, middleX, "iKnow", curses.A_BOLD)
    screen.refresh()   
    pad.border(0)
    pad.addstr(0,0,"Ask me a Question!")
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    pad.addstr(4,0, "RED ALERT!", curses.color_pair(1) )
    pad.refresh(0,0, 5,5, padHeight+5,padWidth+5)
    screen.refresh()
    

#screen = screen.subwin(23, 79, 0, 0)
screen.box()
screen.clear()
curses.noecho()
screen.border(0)
padXpos = 0
padYpos=0

drawScreen()

while(True):
    x = screen.getch()
    if x == 27:
        break
    pad.addch(padXpos,padYpos,x) 
    #pad.addstr(2,2, "asdf" + str(x) )
    #print "Asdf" + str(x)


curses.endwin()
