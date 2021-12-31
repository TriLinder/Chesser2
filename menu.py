import PySimpleGUI as sg

def getFEN() :
    layout = [  [sg.Text('Input a starting FEN String')],
            [sg.InputText(default_text="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")],
            [sg.Button('Ok')] ]

    window = sg.Window('Choose a FEN String', layout, no_titlebar=True, grab_anywhere=True, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            break
        window.close()
        return values[0]

def getGameType() :
    layout = [[sg.Button("2 Players, local multiplayer"), sg.Button("Player vs Computer")]]

    window = sg.Window('Choose game type', layout, no_titlebar=True, grab_anywhere=True, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            break
        window.close()
        return event == "Player vs Computer"
    
def getColor() :
    layout = [[sg.Button("Play as white"), sg.Button("Play as black")]]

    window = sg.Window('Choose your color', layout, no_titlebar=True, grab_anywhere=True, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            break
        window.close()
        return event == "Play as white"