import turtle

class CheckersGUI:
    def __init__(self, GameBoard):
        """Initializes the GUI for the Checkers game."""
        self.GameBoard = GameBoard
        self.Screen = turtle.Screen()
        self.Screen.setup(600, 600)
        self.Screen.title("Interactive Checkers Game")
        self.Screen.tracer(0)

        self.Turtle = turtle.Turtle()
        self.Turtle.speed(0)
        self.Turtle.hideturtle()
        self.Turtle.penup()  # Ensure no unwanted lines are drawn

        self.SquareSize = 60
        self.Clicks = []

        self.Screen.onclick(self.HandleClick)
        self.DrawBoard()

    def DrawBoard(self):
        """Draws the checkerboard grid."""
        self.Turtle.penup()
        Colors = ["#D18B47", "#FFCE9E"]

        for Row in range(8):
            for Col in range(8):
                X = -240 + Col * self.SquareSize
                Y = 240 - Row * self.SquareSize
                self.Turtle.goto(X, Y)
                self.Turtle.fillcolor(Colors[(Row + Col) % 2])
                self.Turtle.begin_fill()
                for _ in range(4):
                    self.Turtle.forward(self.SquareSize)
                    self.Turtle.right(90)
                self.Turtle.end_fill()

        self.DrawPieces()

    def DrawPieces(self):
        """Draws the checkers pieces on the board."""
        self.Turtle.penup()
        PieceRadius = 20
        for Row in range(8):
            for Col in range(8):
                Piece = self.GameBoard.BoardState[Row][Col]
                if Piece != ' ':
                    X = -210 + Col * self.SquareSize
                    Y = 210 - Row * self.SquareSize
                    self.Turtle.goto(X, Y - PieceRadius)
                    self.Turtle.pendown()
                    if Piece in ('WK', 'BK'):
                        self.Turtle.color("gold", "white" if Piece.startswith('W') else "black")
                    else:
                        self.Turtle.color("black", "white" if Piece.startswith('W') else "black")
                    self.Turtle.begin_fill()
                    self.Turtle.circle(PieceRadius)
                    self.Turtle.end_fill()
                    self.Turtle.penup()
                    
                    # Mark kings with a crown
                    if Piece in ('WK', 'BK'):
                        self.Turtle.color("gold")
                        self.Turtle.goto(X, Y - PieceRadius / 2)
                        self.Turtle.write("K", align="center", font=("Arial", 16, "bold"))

    def HandleClick(self, X, Y):
        """Handles user clicks on the board to select pieces and moves."""
        Col = int((X + 240) // self.SquareSize)
        Row = int((240 - Y) // self.SquareSize)

        if 0 <= Row < 8 and 0 <= Col < 8:
            self.Clicks.append((Row, Col))
            print(f"Clicked square: (Row: {Row}, Col: {Col})")

    def Refresh(self):
        """Clears and redraws the board to reflect changes."""
        self.Turtle.clear()
        self.DrawBoard()