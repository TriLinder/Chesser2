from pygame.locals import *
from pathlib import Path
import pygame
import chess
import math
import time
import sys

board = chess.Board()
pygame.init()

#----------------------------------#
size = 3

black = (181, 136, 99)
white = (240, 217, 181)
#----------------------------------#

################################################################
#  LOAD ASSETS

print("Loading assets..")

def getFilename(piece) :
    if not piece == "blank" :
        if piece.isupper() :
            return Path("assets/images/pieces/white/%s.png" % (piece.lower()))
        else :
            return Path("assets/images/pieces/black/%s.png" % (piece.lower()))
    else :
        return Path("assets/images/blank.png")

B = pygame.image.load(getFilename("B"))
K = pygame.image.load(getFilename("K"))
N = pygame.image.load(getFilename("N"))
P = pygame.image.load(getFilename("P"))
Q = pygame.image.load(getFilename("Q"))
R = pygame.image.load(getFilename("R"))

b = pygame.image.load(getFilename("b"))
k = pygame.image.load(getFilename("k"))
n = pygame.image.load(getFilename("n"))
p = pygame.image.load(getFilename("p"))
q = pygame.image.load(getFilename("q"))
r = pygame.image.load(getFilename("r"))

print("Done.")
################################################################

def init() :
    pygame.display.init()

    monintor = pygame.display.Info()

    w = monintor.current_w
    h = monintor.current_h

    if w > h :
        w = int(w / size)
        h = w
    else :
        h = int(h / size)
        w = h

    icon = pygame.image.load(Path("assets/images/icon-32x32.png"))

    pygame.display.set_icon(icon)
    pygame.display.set_caption("Chesser 2")

    return pygame.display.set_mode((h,w), RESIZABLE)

def renderChessboard(screen) :
    monintor = pygame.display.Info()

    w = monintor.current_w
    h = monintor.current_h

    if w > h :
        w = int(w / size)
        h = w
    else :
        h = int(h / size)
        w = h

    cellSize = math.ceil(w / 2.6666)

    isWhite = False

    for x in range(0, 8 + 1) :
        for y in range(0, 8 + 1) :
            isWhite = not isWhite
            if isWhite :
                pygame.draw.rect(screen, white, [cellSize*x,cellSize*y,cellSize,cellSize])
            else :
                pygame.draw.rect(screen, black, [cellSize*x,cellSize*y,cellSize,cellSize])

def renderPiece(screen, piece, x, y) :
    w, h = pygame.display.get_surface().get_size()
    cellSize = round((w / 2.6666) / size)

    if not piece.lower() in ["b", "k", "n", "p", "q", "r"] :
        return "NOT A VALID PIECE"

    exec('screen.blit(pygame.transform.scale(%s, (int(w / 8), int(h / 8))), ((x) * cellSize, (y) * cellSize))' % (piece)) #This is horrible, I know, but it should just do the trick.

def renderPieces(screen, FEN) : #Another horrible *piece* of code, but once again: it works.
    renderBoard = chess.Board()
    renderBoard.set_fen(FEN)

    lines = str(renderBoard).replace(" ", "").split("\n")
    
    x = 0
    y = 0

    for line in lines :
        for piece in line :
            if not piece == "." :
                renderPiece(screen, piece, x, y)
            x += 1

        y += 1
        x = 0

def frame(screen, FEN) :
    w, h = pygame.display.get_surface().get_size()

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            w, h = pygame.display.get_surface().get_size()
            cellSize = round((w / 2.6666) / size)
            click_x = math.ceil(pos[0] / cellSize) -1
            click_y = math.ceil(pos[1] / cellSize) -1

            if not click_x in range(0,8) or not click_y in range(0,8) : #01234567
                break

            return ["click", click_x, click_y]

    renderChessboard(screen)
    renderPieces(screen, FEN)

    if not w == h :
        print("Resizing to 1:1")
        pygame.display.set_mode((h,h), RESIZABLE)

    pygame.display.update()

if __name__ == "__main__" :
    FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    screen = init()

    while True :
        frame(screen, FEN)