#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import curses 
from curses import panel
import sys



def main():
    if len(sys.argv) == 2:
        display_single_entry(sys.argv[1])
    elif len(sys.argv) == 1:
        display_menu()
    else:
        print_usage()
        

def display_single_entry(argument):
    print argument

def display_menu():
    screen = curses.initscr()
    curses.start_color()
    curses.noecho() 
    curses.curs_set(0) 
    screen.keypad(1) 
    
    highlight = 0
    choices = {"Lookup Term", "About","Exit"}
    num_choices = 3
    print_menu(screen,highlight,choices,num_choices)

    while True: 
        event = screen.getch() 
        if event == ord("q"): 
            break 
        elif event == curses.KEY_UP:
            if (highlight==0):
                highlight = num_choices-1
            else:
                highlight -= 1
        elif event == curses.KEY_DOWN:
            if (highlight==num_choices-1):
                highlight = 0
            else:
                highlight += 1
        else:
            screen.addstr(str(event))
        screen.refresh()
        print_menu(screen,highlight,choices,num_choices)
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

def mkpanel(color, rows, cols, tly, tlx):
    win = curses.newwin(rows, cols, tly, tlx)
    pan = panel.new_panel(win)
    if curses.has_colors():
        if color == curses.COLOR_BLUE:
            fg = curses.COLOR_WHITE
        else:
            fg = curses.COLOR_BLACK
        bg = color
        curses.init_pair(color, fg, bg)
        win.bkgdset(ord(' '), curses.color_pair(color))
    else:
        win.bkgdset(ord(' '), curses.A_BOLD)

    return pan

def print_menu(screen, highlight, choices, num_choices):
    i=0
    x = 0
    y = 0
    dy = 30
    p1 = mkpanel(curses.COLOR_RED,
                 curses.LINES,
                 curses.COLS,
                 0,
                 0)
    p1.set_userptr("p1")
    #fill_panel(p1)
    for choice in choices:
        if (i!=highlight):
            #p1.move(y,0)
            screen.addstr(y,x,choice)
        else:
            #p1.move(y,0)
            #p1.attron(curses.A_BOLD)
            screen.addstr(y,x,choice,curses.A_BOLD)
            #p1.attroff(curses.A_BOLD)
        i+=1
        y+=dy
    
def print_usage():
    print "Usage of ManWiki:"
    print "      ./mw [search term]"

if __name__=="__main__":
    main()
