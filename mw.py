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
from curses import panel
import sys
import urllib
from lxml import html


def main():
    if len(sys.argv) == 2:
        display_single_entry(sys.argv[1])
    elif len(sys.argv) == 1:
        processmenu(menu_data)
        curses.endwin()
    else:
        print_usage()
        

def display_single_entry(argument):
    print argument

menu_data = {
    'title': "Main Menu", 
    'subtitle': "The Main Nav Menu for the program",
    'options': [
        { 'title': "Lookup Term", 'command': '' },
        { 'title': "About", 'command': '' },
        ]
    }

# This function displays the appropriate menu and returns the option selected
def runmenu(screen, menu, parent, n, h):
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
      screen.addstr(2,2, menu['title'], curses.A_STANDOUT) 
      screen.addstr(4,2, menu['subtitle'], curses.A_BOLD) 

      # Display all the menu items, showing the 'pos' item highlighted
      for index in range(optioncount):
        textstyle = n
        if pos==index:
          textstyle = h
        screen.addstr(5+index,4, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)
      # Now display Exit/Return at bottom of menu
      textstyle = n
      if pos==optioncount:
        textstyle = h
      screen.addstr(5+optioncount,4, "%d - %s" % (optioncount+1, lastoption), textstyle)
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
    exitmenu = False
    while not exitmenu: #Loop until the user exits the menu
        getin = runmenu(screen, menu, parent, n, h)
        if getin == optioncount:
            exitmenu = True
        elif getin == 0:
            #this is the search
            print_prompt(screen)
        else:
            print_about(screen)

def print_about(screen):
    screen.addstr(10,2, "Creator: Andrey Tydnyuk", curses.A_STANDOUT) 
    screen.refresh()
    search_term = screen.getch(10,20)
    screen.addstr(10,2, "                                     ", 
                  curses.A_STANDOUT) 
    screen.refresh()
    
def print_prompt(screen):
    screen.addstr(10,2, "Search for term: ", curses.A_STANDOUT) 
    screen.refresh()
    curses.echo()
    search_term = screen.getstr(10,20)
    display_entry(screen,search_term)
    screen.addstr(10,2, "                                     ", 
                  curses.A_STANDOUT) 
    screen.refresh()

def display_entry(screen,term):
    url = "http://en.wikipedia.org/wiki/"+term
    page = html.fromstring(urllib.urlopen(url).read())
    screen.clear()
    screen.addstr(10,10,html.tostring(page)[0:30])
    
def print_usage():
    print "Usage of ManWiki:"
    print "      ./mw [search term]"

if __name__=="__main__":
    main()
