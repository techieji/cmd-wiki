import render
import curses
from time import sleep
import wikipedia as wk
import sys

if len(sys.argv) == 1:
    title = input('Enter a search topic: ')
else:
    title = ' '.join(sys.argv[1:])

title = title.capitalize()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    text = wk.WikipediaPage(title=title).content
    while True:
        render.all_together_now(stdscr, title, text)
        stdscr.refresh()
        c = stdscr.getkey()
        if c == 'q':
            break
        elif c == 'KEY_DOWN':
            render.scroll += 1
        elif c == 'KEY_UP':
            if render.scroll > 0:
                render.scroll -= 1
        sleep(1/60)
        stdscr.erase()
    sleep(1)

curses.wrapper(main)
