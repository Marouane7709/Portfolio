class GameBoard:
    def __init__(self):
        """Initialize the Checkers board with an 8x8 grid."""
        self.BoardState = self.CreateBoard()
    
    def CreateBoard(self):
        """Creates an 8x8 board and places pieces in the correct starting positions."""
        Board = [[' ' for _ in range(8)] for _ in range(8)]
        
        # Place white pieces (top side, player-controlled)
        for Row in range(3):
            for Col in range(8):
                if (Row + Col) % 2 == 1:
                    Board[Row][Col] = 'W'  # White piece
        
        # Place black pieces (bottom side, AI-controlled)
        for Row in range(5, 8):
            for Col in range(8):
                if (Row + Col) % 2 == 1:
                    Board[Row][Col] = 'B'  # Black piece
        
        return Board

    def DisplayBoard(self):
        """Displays the board in a readable format."""
        print("  A B C D E F G H")
        print(" +----------------")
        for Index, Row in enumerate(self.BoardState):
            print(f"{Index+1}|", end=" ")
            print(" ".join(Row))
        print()

    def GetValidMoves(self, X, Y):
        """Returns a list of valid moves for a piece at (X, Y), including jumps."""
        Piece = self.BoardState[X][Y]
        if Piece == ' ':
            return []  # No piece to move

        # Determine movement directions
        if Piece == 'W':
            Directions = [(1, -1), (1, 1)]  # White moves downward
        elif Piece == 'B':
            Directions = [(-1, -1), (-1, 1)]  # Black moves upward
        elif Piece in ('WK', 'BK'):  
            Directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]  # Kings move in all four directions
    
        ValidMoves = []
        JumpMoves = []

        # Check regular moves
        for DX, DY in Directions:
            NX, NY = X + DX, Y + DY
            if 0 <= NX < 8 and 0 <= NY < 8 and self.BoardState[NX][NY] == ' ':
                ValidMoves.append((NX, NY))

        # Check for jumps (captures)
        for DX, DY in Directions:
            NX, NY = X + DX, Y + DY
            JX, JY = X + 2 * DX, Y + 2 * DY
            if 0 <= JX < 8 and 0 <= JY < 8 and 0 <= NX < 8 and 0 <= NY < 8:
                if self.BoardState[NX][NY] not in (' ', Piece) and self.BoardState[JX][JY] == ' ':
                    JumpMoves.append((JX, JY))

        # If a jump is available, the player MUST take it
        return JumpMoves if JumpMoves else ValidMoves

    def MovePiece(self, StartX, StartY, TargetX, TargetY):
        """Moves a piece from (StartX, StartY) to (TargetX, TargetY) if the move is valid, including captures."""
        ValidMoves = self.GetValidMoves(StartX, StartY)
        if (TargetX, TargetY) in ValidMoves:
            self.BoardState[TargetX][TargetY] = self.BoardState[StartX][StartY]
            self.BoardState[StartX][StartY] = ' '
            
            # If the move was a jump (capture), remove the captured piece
            if abs(TargetX - StartX) == 2:
                CapturedX, CapturedY = (StartX + TargetX) // 2, (StartY + TargetY) // 2
                self.BoardState[CapturedX][CapturedY] = ' '  # Remove captured piece

                # Allow multiple jumps for kings
                if self.BoardState[TargetX][TargetY] in ('WK', 'BK'):
                    AdditionalJumps = self.GetValidMoves(TargetX, TargetY)
                    if any(abs(JX - TargetX) == 2 for JX, JY in AdditionalJumps):
                        return "JumpContinued"

            # Check for king promotion
            if TargetX == 0 and self.BoardState[TargetX][TargetY] == 'B':
                self.BoardState[TargetX][TargetY] = 'BK'  # Black piece becomes king
            elif TargetX == 7 and self.BoardState[TargetX][TargetY] == 'W':
                self.BoardState[TargetX][TargetY] = 'WK'  # White piece becomes king

            return True
        return False

    def HasValidMoves(self, Player):
        """Check if the given player has any valid moves left."""
        for X in range(8):
            for Y in range(8):
                if self.BoardState[X][Y] in (Player, Player + 'K') and self.GetValidMoves(X, Y):
                    return True
        return False

    def IsGameOver(self):
        """Check if the game is over (one player has no valid moves left)."""
        return not (self.HasValidMoves('W') and self.HasValidMoves('B'))
