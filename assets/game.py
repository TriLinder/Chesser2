import render
import menu
import time
import chess
import sys

maxFPS = 15

#FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#FEN = "8/8/K7/7r/6r1/8/8/2k5 w - - 0 1" #Checkmate test
#FEN = "8/8/k7/7R/6R1/8/8/K7 w - - 0 1" #Checkmate test2
FEN = menu.getFEN()

if FEN == None :
    sys.exit()

gameType = menu.getGameType()

if gameType == None :
    sys.exit()

screen = render.init()

def getPiece(FEN, x, y) :
    board = chess.Board()
    board.set_fen(FEN)

    return str(board).replace(" ", "").split("\n")[y][x]

def getPossibleMoves(FEN) : #Translates possible moves to board coords
    alphabet = "a,b,c,d,e,f,g,h".split(",")

    board = chess.Board()
    board.set_fen(FEN)

    translatedMoves = []

    for move in board.legal_moves :
        move = str(move)

        startState = [(alphabet.index(move[0])), 8-(int(move[1]))]
        endState = [(alphabet.index(move[2])), 8-(int(move[3]))]

        translatedMove = [startState, endState]
        translatedMoves.append(translatedMove)
    
    return translatedMoves

def coordsToStandart(coords) :
    alphabet = "a,b,c,d,e,f,g,h".split(",")

    return alphabet[coords[0]] + str(8-coords[1])

def makeMove(FEN, move) :
    board = chess.Board()
    board.set_fen(FEN)
    board.push(chess.Move.from_uci(move))

    return [str(board.fen()), board.outcome()]

def whosTurn(FEN) :
    board = chess.Board()
    board.set_fen(FEN)

    return board.turn == chess.WHITE

selectedX = -1
selectedY = -1

possibleEndstates = []

if not gameType :
    isWhite = True
    canPlayOther = True

outcome = None

render.redrawScreen(screen, FEN, [selectedX, selectedY], possibleEndstates)

while True :
    event = render.frame(screen, FEN, [selectedX, selectedY], possibleEndstates, outcome)
    
    if event[0] == "none" :
        pass
    elif event[0] == "click" :
        if [event[1], event[2]] in possibleEndstates :
            movingToX = event[1]
            movingToY = event[2]

            move = coordsToStandart([selectedX, selectedY]) + coordsToStandart([movingToX, movingToY])
            FEN = makeMove(FEN, move)

            outcome = FEN[1]
            FEN = FEN[0]

            selectedX = -1
            selectedY = -1
            possibleEndstates = []

        else :
            selectedX = event[1]
            selectedY = event[2]

            possiblePiece = getPiece(FEN, selectedX, selectedY)

            if possiblePiece == "." :
                selectedX = -1
                selectedY = -1
            
            possibleMoves = getPossibleMoves(FEN)

            possibleEndstates = []

            for move in possibleMoves :
                startState = move[0]
                endState = move[1]

                if startState == [selectedX, selectedY] :
                    possibleEndstates.append(endState)

        render.redrawScreen(screen, FEN, [selectedX, selectedY], possibleEndstates)

    elif event[0] == "quit" :
        sys.exit()

    time.sleep(1/maxFPS)