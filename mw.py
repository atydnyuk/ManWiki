#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import curses 
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
    curses.noecho() 
    curses.curs_set(0) 
    screen.keypad(1) 
    
    screen.addstr("This is a Sample Curses Script\n\n") 
    while True: 
        event = screen.getch() 
        if event == ord("q"): break 
        
    curses.endwin()
    
def print_usage():
    print "Usage of ManWiki:"
    print "      ./mw [search term]"

if __name__=="__main__":
    main()
