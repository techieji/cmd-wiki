import curses
from pyfiglet import Figlet
import itertools as it
import re

def log(*x):
    with open('log.txt', 'w') as f:
        print(*x, file=f, flush=True)

scroll = 0
title = None
wrapped_text = None

def big_text(text, stdscr=None):
    global title
    font = "5x7"
    if stdscr is not None:
        _, x = stdscr.getmaxyx()
        if 5 * len(text) > x:
            font = "3x5"
    if title is None:
        title = Figlet(font=font).renderText(text).replace('#', '█')
    return title

def rule(stdscr, y=8):
    l = '─' * (stdscr.getmaxyx()[1] - 1)
    stdscr.addstr(y, 0, l)

def wrap_text(_text, maxx=100):
    text = _text + '\n'
    l = ['']
    col = 0
    word = ''
    for x in text:
        if x == '\n':
            l[-1] += ' ' + word
            word = ''
            col = 0
            l.append('')
        elif x == ' ':
            if 1 + len(word) + col > maxx:
                l.append(word)
                col = len(word)
            else:
                l[-1] += ' ' + word
                col += 1 + len(word)
        else:
            word += x
    return l

def _wrap_text(text, maxx=100):
    l = ['']
    col = 0
    word = ''
    for x in text:
        if x == '\n':
            l.append('')
            l.append('')
            col = 0
        elif x == ' ':
            if len(word) + col > maxx:
                l.append(word)
                # log(col, word, maxx)
                word = ''
                col = len(word)
            else:
                l[-1] += word
                col += len(word)
        elif col > maxx:
            l.append('')
            col = 0
        word += x
    return l

def load_text(stdscr, text, y=9):
    global wrapped_text
    maxy, maxx = stdscr.getmaxyx()
    if wrapped_text is None:
        wrapped_text = wrap_text(text, maxx - 1)
    txt = wrapped_text[scroll: scroll + maxy - y - 1]
    for i in range(len(txt)):
        stdscr.addstr(y + i, 0, txt[i].replace('\n', '').strip())

def all_together_now(stdscr, title, text):
    stdscr.addstr(0, 0, big_text(title, stdscr))
    rule(stdscr)
    load_text(stdscr, text)
