import curses
from pyfiglet import Figlet
import itertools as it
import re

def log(*x):
    with open('log.txt', 'w') as f:
        print(*x, file=f, flush=True)

scroll = 0
percent = 0
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
    maxy, maxx = stdscr.getmaxyx()
    amt = int(percent * maxx)
    if amt > maxx:
        amt = maxx
    l1 = '─' * amt
    stdscr.addstr(y, 0, l1, curses.color_pair(1))
    l2 = '─' * int((1 - percent) * maxx)
    stdscr.addstr(y, amt, l2)

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
            word = ''
        else:
            word += x
    return l

def headerize(l):
    newl = []
    for x in l:
        if len(x.strip()) > 0 and x.strip()[0] == '=':
            newl.extend(Figlet(font='5x7').renderText(x).replace('#', '█').split('\n'))
            newl.append(x)
        else:
            newl.append(x)
    return newl

def load_text(stdscr, text, y=9):
    global wrapped_text
    global percent
    maxy, maxx = stdscr.getmaxyx()
    if wrapped_text is None:
        wrapped_text = wrap_text(text, maxx - 1)
    txt = wrapped_text[scroll: scroll + maxy - y - 1]
    percent = (scroll + maxy - y - 1)/len(wrapped_text)
    for i in range(len(txt)):
        stdscr.addstr(y + i, 0, txt[i].replace('\n', '').strip())

def all_together_now(stdscr, title, text):
    stdscr.addstr(0, 0, big_text(title, stdscr))
    rule(stdscr)
    load_text(stdscr, text)
