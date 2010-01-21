'''
Created on Jan 20, 2010
'''

import curses

def drawScreen():
    """Draw screen components"""
    screen.border(0)
    screen.addstr(2, 2, "hello!")
    

if __name__ == '__main__':
    screen = curses.initscr()
    screen.clear()
    
    drawScreen()
    x = screen.getch()
    curses.endwin()
