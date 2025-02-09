import time
import random
import curses
from curses import wrapper

def new_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to Words Per Minute!")
    stdscr.addstr(1, 0, "Press any key to start the game")
    stdscr.refresh()
    stdscr.getkey()

def inicia_texto(stdscr, target, atual, score, tempo_usado):
    stdscr.addstr(target)
    
    for i, char in enumerate(atual):
        correto = target[i]
        cor = curses.color_pair(1)
        if char == correto:
            cor = curses.color_pair(2)
            #Falta formula para calcular o Score com base nas certas e errads
        stdscr.addstr(0, i, char, cor)
        stdscr.addstr(1, 0, "Score: " + str(score))
        stdscr.addstr(2, 0, "Tempo: " + str(round(tempo_usado)) + " sec.")

def load_texto():
    with open("sample.txt", "r") as f:
        lines = f.readlines()
        print(lines)
        return random.choice(lines)

def game_on(stdscr):
    target = load_texto()
    atual = []
    final_score = 0
    tempo = time.time()
    stdscr.nodelay(True)

    while True:
        tempo_usado = max(time.time() - tempo, 1)
        final_score = len(atual)
        stdscr.clear()
        inicia_texto(stdscr, target, atual, final_score, tempo_usado)
        stdscr.refresh()

        if "".join(atual) == target:
            stdscr.nodelay(False)
            break
        if len(atual)>=len(target):
            stdscr.nodelay(False)
            break
        try:
            tecla = stdscr.getkey()
            #if len(tecla) == 1:
            #    atual.append(tecla)
        except:
            continue
                
        if len(tecla)==1 and ord(tecla)==27:
            break

        if tecla in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(atual) > 0:
                atual.pop()
        elif tecla in ("KEY_ENTER", "\n", "\r", "\x0D"):
            continue
        elif len(atual) < len(target):
            atual.append(tecla)
        else: #len(atual)>=len(target) :
            stdscr.nodelay(False)
            break

def main(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    new_screen(stdscr)
    while True:
        game_on(stdscr)
        #stdscr.clear()
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(3, 0, "Game Over!")
        stdscr.addstr(4, 0, "Press any key to play again.")
        tecla = stdscr.getkey()
        if ord(tecla)==27:
            break

wrapper(main)