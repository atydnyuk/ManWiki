#include<ncurses.h>
#include<stdlib.h>
#include<stdio.h>
#include<string.h>
#include<unistd.h>
#include<fcntl.h>
#include<menu.h>
#include<form.h>

#define MAX_SIZE 1024


void display_entry(char *arg1);
void display_single_entry(char *arg1);
void display_menu();
void getFile(char* arg1,char *outname);
void print_menu(WINDOW *menu_win,int highlight,char **choices, int n_choices);
void print_prompt(WINDOW *menu_win);
void print_about(WINDOW *menu_win);
void print_usage();

char *string_input; 

int main(int argc, char **argv) {
  if (argc==2) {
	display_single_entry(argv[1]);
  } else if (argc==1) { 
	display_menu();
  } else {
	print_usage();
	return 1;
  }
  return 0;
}

/*You want to view an entry, so the perl script
 *is run to grab the entry, and then you read the 
 *entry from the outfile using less*/
void display_single_entry(char *arg1) {
  char *buffer = malloc(MAX_SIZE);
  char *outname = "outfile";
  int i, fd;
  getFile(arg1, outname);
  fd = open(outname, O_RDONLY);
  i = read(fd,buffer, MAX_SIZE-1);
  if (i == -1) {
	perror("Read call failed");
  }
  i = system("less outfile");
  if (i == -1) {
	perror("less call failed");
  }
  free(buffer);
}

void display_entry(char *arg1) {
  char *buffer = malloc(MAX_SIZE);
  char *outname = "outfile";
  int i, fd;
  getFile(arg1, outname);
  fd = open(outname, O_RDONLY);
  i = read(fd,buffer, MAX_SIZE-1);
  if (i == -1) {
	perror("Read call failed");
  }
  i = system("less outfile");
  if (i == -1) {
	perror("less call failed");
  }
  free(buffer);
  display_menu();
}

void display_menu() {
  WINDOW *menu_win;
  int highlight = 1;
  int c;
  char *choices[] = {"Lookup Term","Random Page","Configuration","About","Exit"};
  int n_choices = sizeof(choices)/sizeof(char *);
 
  initscr(); /*initiate screen*/
  clear(); /*clear screen*/
  raw();
  noecho(); /*dont print characters you type*/
  cbreak();
  start_color();
  curs_set(0); /*dont show cursor*/
  menu_win = newwin(0, 0, 0, 0);
  keypad(menu_win, TRUE);
  
  refresh();
  
  print_menu(menu_win, highlight, choices, n_choices);

  /*you print the menu, and then catch the keypresses
   *to navigate around it*/
  while(1) {
	c = wgetch(menu_win);
	switch(c) {
	case KEY_UP:
	  if(highlight == 1)
	    highlight = n_choices;
	  else
	    --highlight;
	  break;
	case KEY_DOWN:
	  if(highlight == n_choices)
	    highlight = 1;
	  else 
	    ++highlight;
	  break;
	case 10:
	  if (highlight==1) {
		/*if you want to search, a
		 *prompt comes up and shows the entry*/
		print_prompt(menu_win);
		clrtoeol();
		refresh();
		endwin();
		return;
	  }
	  if (highlight==4) {
		/*about*/
		print_about(menu_win);
	  }
	  if (highlight==n_choices) {
		/*exit*/
		//clrtoeol();
		wrefresh(menu_win);
		delwin(menu_win);
		free(string_input);
		clear();
		endwin();	      
		return;
	  }
	  else {
		refresh();
		break;
	  }
	  break;
	default: 
	  refresh();
	  break;
	}	
	print_menu(menu_win, highlight,choices,n_choices);
  }
  clrtoeol();
  refresh();
  endwin();
  return;
}


void getFile(char* arg1,char *outname) {
  int i;
  char *command = malloc(strlen("./getPage.pl ")+
						 strlen(arg1)+
						 strlen(" >")+
						 strlen(outname)+3);
  
  strcpy(command, "./getPage.pl ");
  strcat(command, arg1);
  strcat(command, " >");
  strcat(command, outname);
  
  i = system(command);
  if (i==-1) {
	perror("System call failed");
  }
  free(command);
}

void print_menu(WINDOW *menu_win,int highlight,char **choices, int n_choices) {
  int x, y, i;
  init_pair(1, COLOR_BLUE, COLOR_BLACK);
  x = COLS/2;
  y = LINES/2;
  box(menu_win, 0, 0);
  for(i = 0; i < n_choices; ++i)
    {
      wattron(menu_win,COLOR_PAIR(1)|A_BOLD);
      if(highlight == i + 1) {
		wattron(menu_win, A_REVERSE);
		mvwprintw(menu_win, y, x, "%s", choices[i]);
		wattroff(menu_win, A_REVERSE); 
	  } else {
		mvwprintw(menu_win, y, x, "%s", choices[i]);
	  }
      ++y;
      wattroff(menu_win,COLOR_PAIR(1)|A_BOLD);
    }
  refresh();
}

void print_prompt(WINDOW *menu_win) {
  string_input = malloc(sizeof(char) * 256);
  wattron(menu_win,COLOR_PAIR(1));
  mvwprintw(menu_win, 40, 10, "%s", "Term you would like to search for: ");
  refresh();
  echo();
  mvwgetnstr(menu_win,40,45,string_input,255);
  refresh();
  wattroff(menu_win,COLOR_PAIR(1)|A_BOLD);
  display_entry(string_input);
  /*this erases...*/
  mvwprintw(menu_win, 40, 10, "%s", "                                                                                  ");
  refresh();
}

void print_about(WINDOW *menu_win)
{
  wattron(menu_win,COLOR_PAIR(1));
  mvwprintw(menu_win, 30, 40, "%s", "Manwiki was developed by Andrey Tydnyuk, Peter Appleby, Dan Pomeroy and Jeung Won Kim");
  wattroff(menu_win,COLOR_PAIR(1));
  refresh();
  wgetch(menu_win);
  /*this erases...*/
  mvwprintw(menu_win, 30, 40, "%s", "                                                                                       ");
  refresh();
}


void print_usage()
{
  printf("Usage of manwiki:\n");
  printf("      You need either one or no arguments.\n");
  printf("      -mw [search term]\n"); 
}
