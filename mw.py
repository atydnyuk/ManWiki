#!/usr/bin/env python 

## Credit where credit is due:

################
# The menu code:
################
# Topmenu and the submenus are based of the example 
# found at this location 
# http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/
# The rest of the work was done by Matthew Bennett and he 
# requests you keep these two mentions when you reuse the code :-)
# Basic code refactoring by Andrew Scheller

import curses 
import sys
import urllib
import lxml.etree
import urllib
import wiki_utils
import utils
import re 
import os
import signal

exitmenu = False
screen = None

def main():
    signal.signal(signal.SIGWINCH, handle)
    if len(sys.argv) == 2:
        display_single_entry(sys.argv[1])
    elif len(sys.argv) == 1:
        processmenu(menu_data)
        curses.endwin()
    else:
        print_usage()
        
menu_data = {
    'title': "Main Menu", 
    'subtitle': "The Main Nav Menu for the program",
    'options': [
        { 'title': "Lookup Term", 'command': '' },
        { 'title': "About", 'command': '' },
        ]
    }

def handle(*args):
    global exitmenu
    curses.flash()
    curses.refresh()
    exitmenu = True
    size = screen.getmaxyx()
    #sys.stderr.write("Now %u x %u\n" % (size[1],size[0]))
    processmenu(menu_data)
    
    
# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent, n, h):
    global screen
    if parent is None:
        lastoption = "Exit"
    else:
        lastoption = "Return to %s menu" % parent['title']

    optioncount = len(menu['options']) # how many options in this menu
        
    pos=0 
    oldpos=None # used to prevent the screen being redrawn every time
    x = None 
    
    # Loop until return key is pressed
    while x !=ord('\n'):
        if pos != oldpos:
            oldpos = pos
            screen.clear() 
            screen.border(0)
            screen.refresh()
            screen.addstr(2,2, menu['title'], curses.A_STANDOUT) 
            screen.addstr(4,2, menu['subtitle'], curses.A_BOLD) 

      # Display all the menu items, showing the 'pos' item highlighted
        for index in range(optioncount):
            textstyle = n
            if pos==index:
                textstyle = h
            screen.addstr(5+index,4, 
                          "%d - %s" % 
                          (index+1, menu['options'][index]['title']), 
                          textstyle)
      # Now display Exit/Return at bottom of menu
        textstyle = n
        if pos==optioncount:
            textstyle = h
        screen.addstr(5+optioncount,4, 
                      "%d - %s" % (optioncount+1, lastoption), 
                      textstyle)
        screen.refresh()
      # finished updating screen

        x = screen.getch() # Gets user input

    # What is user input?
        if x >= ord('1') and x <= ord(str(optioncount+1)):
            pos = x - ord('0') - 1 
        elif x == 258: # down arrow
            if pos < optioncount:
                pos += 1
            else: pos = 0
        elif x == 259: # up arrow
            if pos > 0:
                pos += -1
            else: pos = optioncount
        elif x != ord('\n'):
            curses.flash()
            
    # return index of the selected item
    return pos

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
    global exitmenu
    global screen
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    screen.keypad(1) 
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE) 
    h = curses.color_pair(1) 
    n = curses.A_NORMAL 
    optioncount = len(menu['options'])
    while not exitmenu: #Loop until the user exits the menu
        getin = runmenu(menu, parent, n, h)
        if getin == optioncount:
            exitmenu = True
        elif getin == 0:
            #this is the search
            print_prompt()
        else:
            print_about()

def print_about():
    global screen
    screen.addstr(10,2, "Creator: Andrey Tydnyuk", curses.A_STANDOUT) 
    screen.refresh()
    screen.getch(10,20)
    screen.addstr(10,2, "                       ", 
                  curses.A_STANDOUT) 
    screen.refresh()
    
def print_prompt():
    global screen
    screen.addstr(10,2, "Search for term: ", curses.A_STANDOUT) 
    screen.refresh()
    curses.echo()
    search_term = screen.getstr(10,20)
    display_entry(search_term)
    screen.addstr(10,2, "                       ", 
                  curses.A_STANDOUT) 
    screen.refresh()
    curses.noecho()

def display_single_entry(title):
    global exitmenu
    wikipedia_utils = utils.swimport("wikipedia_utils")
    val = wikipedia_utils.GetWikipediaPage(title)
    if val == None:
        #we didnt get anything
        result = "We could not find anything under that key word"
    else:    
        res = wikipedia_utils.ParseTemplates(val["text"])
        result = res["flattext"]    
            
    print result
    sys.stdout.flush()
    exitmenu = True

def display_entry(title):
    global screen
    if (len(title)==0):
        return
    screen.addstr(20,10,"Loading.",curses.A_STANDOUT)
    screen.refresh()
    wikipedia_utils = utils.swimport("wikipedia_utils")
    screen.addstr(20,10,"Loading..",curses.A_STANDOUT)
    screen.refresh()
    val = wikipedia_utils.GetWikipediaPage(title)
    screen.addstr(20,10,"Loading...",curses.A_STANDOUT)
    screen.refresh()
    if val == None:
        #we didnt get anything
        result = "We could not find anything under that key word"
    else:    
        res = wikipedia_utils.ParseTemplates(val["text"])
        result = res["flattext"]    
    re.sub('<[^<]+?>', '', result)
    screen.erase()
    screen.refresh()
    screen.addstr(0,0,result[:1500].encode('utf-8').decode('ascii','ignore').replace('\n\n','\n'),curses.A_STANDOUT) 
    screen.refresh()
    screen.getch(0,0)

def print_usage():
    print "Usage of ManWiki:"
    print "      ./mw [search term]"

if __name__=="__main__":
    main()
