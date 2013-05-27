all:
	gcc -g -o mw -W -Wall -Wextra -O2 -lmenu -lform -lpanel -lncurses -lcurl mw.c
clean:
	rm *.out
	rm *.o