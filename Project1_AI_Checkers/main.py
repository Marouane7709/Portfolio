from PlayingTheGame import GameLoop
from CheckersGUI import CheckersGUI
from GameBoard import GameBoard
import turtle

def Main():
    """Initializes and starts the checkers game."""
    Board = GameBoard()
    GUI = CheckersGUI(Board)
    GameLoop(Board, GUI)
    turtle.done()

if __name__ == "__main__":
    Main()