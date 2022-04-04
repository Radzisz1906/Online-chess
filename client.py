import socket
import pygame as p
import chess
import szachownica
from threading import Thread
import time

HOST = #IP_ADRESS
PORT = #port
ruch = ""
# print(board)

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
IMAGES = {}
MAX_FPS = 60
przeg = 0
wyg = 0


def load_Images():
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("red")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(
                screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(
                    IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


def moving(plansza):
    # print(plansza, "\n\n")
    dostepne_ruchy = str(list(plansza.legal_moves))
    ruchy = ""
    w = 0
    for i in range(len(dostepne_ruchy)):
        if dostepne_ruchy[i] == "(":
            w = 1
        if dostepne_ruchy[i] == ">" or dostepne_ruchy[i] == ")":
            w = 0
        if w == 1:
            ruchy += dostepne_ruchy[i]
    dostepne_ruchy = ""
    for i in ruchy:
        if i == "(":
            dostepne_ruchy += " "
        else:
            dostepne_ruchy += i
    dostepne_ruchy = "".join(c for c in dostepne_ruchy if c not in "'")
    dostepne_ruchy = dostepne_ruchy.split()
    # print("Dostepne ruchy: ", dostepne_ruchy)
    return dostepne_ruchy
    # ruch = input()
    # if ruch in dostepne_ruchy:
    #     move = chess.Move.from_uci(ruch)
    #     plansza.push(move)
    #     print(plansza)
    #     print("\n")
    #     return ruch
    # else:
    #     print("Zly ruch")
    #     moving(plansza)


plansza = chess.Board()

gs = szachownica.StanGry()

wys = 0


class klasa(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        global ruch
        global wys
        global gs
        global plansza
        global wyg
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                data = s.recv(1024)
                print(data.decode())
                msg = input()
                if msg == 1:
                    gs.ruch = 1
                if msg == 0:
                    gs.ruch = 0
                s.send(bytes(msg, "utf-8"))
                data = s.recv(1024)
                print(data.decode())
                if data.decode() != "0":
                    msg = input()
                    s.send(bytes(msg, "utf-8"))
                    data = s.recv(1024)
                    print(data.decode())
                    if data.decode() != "Zle id!":
                        data = s.recv(1024)
                        print(data.decode())
                    if data.decode() == "Gra":
                        gs.game = True
                        while True:

                            data = s.recv(1024)
                            print(data.decode())
                            gs.turn = True
                            data = s.recv(1024)
                            if data.decode() != "Nic" and data.decode() != "przegranko":
                                gs.rusz(data.decode())
                                move = chess.Move.from_uci(data.decode())
                                plansza.push(move)
                            elif data.decode() == "przegranko":
                                print("WYGRALES!!!")
                                wyg = 1
                                break
                            while True:
                                if wys == 1:
                                    break
                            if przeg == 1:
                                s.send(bytes("przegranko", "utf-8"))
                            else:
                                wys = 0
                                gs.turn = False
                                # gs.rusz(ruch)
                                print("RUCH: ", ruch)
                                move = chess.Move.from_uci(ruch)
                                print("RUCH: ", move)
                                plansza.push(move)
                                s.send(bytes(ruch, "utf-8"))
                                ruch = ""

                            # print(inputy)

            s.close()


def main():
    global wys
    global ruch
    global przeg
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    load_Images()
    running = True
    sqSelected = ()
    playerClicks = []
    obiekt = klasa()
    obiekt.start()
    while running == True:
        for e in p.event.get():
            if e.type == p.K_ESCAPE:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and gs.turn == True and gs.game == True:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                sqSelected = (row, col)
                playerClicks.append(sqSelected)
                if len(moving(plansza)) == 0 and wyg == 0:
                    print("PRZEGRALES")
                    przeg = 1
                    wys = 1
                    break
                else:
                    if len(playerClicks) == 2:
                        # print(playerClicks)

                        ruch += szachownica.col_rev(playerClicks[0][1])
                        ruch += szachownica.row_rev(playerClicks[0][0])
                        ruch += szachownica.col_rev(playerClicks[1][1])
                        ruch += szachownica.row_rev(playerClicks[1][0])
                        # print(ruch)
                        # print(moving(plansza))

                        if ruch in moving(plansza):
                            gs.rusz_rev(playerClicks)
                            wys = 1
                            playerClicks = []
                            sqSelected = ()
                            gs.ruch = False
                        else:
                            playerClicks = []
                            sqSelected = ()
                            ruch = ""
                    elif len(playerClicks) > 2:
                        playerClicks = []
                        sqSelected = ()

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
