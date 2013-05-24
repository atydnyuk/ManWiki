####################### 
   MANWIKI README
######################


Launching instructions:

1) Type make
2) ./mw [search term]


Files Included:

Makefile - really simple so far, compiles and generates binary

getPage.pl - this is the perl script that gets and parses the page

outfile - This is where the output of the perl script goes

mw.c - This holds the C code for the manwiki program

mw - the executable binary


Planned Additions:

#########NOTE#########
Since I hardcoded the text positions, the program will crash
when it tries to write to the screen if your terminal is too 
small. I just used fullscreen to set it up, so to prevent 
crashes, just fullscreen your terminal. I will fix the text
positioning to be relative to the menus and the size of the 
window later..


1) Include an option for picking the wiki you want to search
2) Include a config file for different random options like colors
3) Format the page better, and actually return the article text as opposed
   to everything on the sidebar, and all of the other extra info.
4) Some extra functionality in the text viewer (want to avoid having to use less)
5) Fix up the makefile to include dependencies, and some more options
6) Remove the need for an outfile, or delete it after program exits.
