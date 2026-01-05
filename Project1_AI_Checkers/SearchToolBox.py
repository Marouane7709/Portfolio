import time

class SearchToolBox:
    def __init__(self, TimeLimit=4, DepthLimit=5):
        """Initializes the search toolbox with constraints on search time and depth."""
        self.StatesExpanded = 0  # Tracks the number of expanded states in search
        self.PrunedBranches = 0  # Tracks the number of pruned branches in Alpha-Beta pruning
        self.TimeLimit = min(max(TimeLimit, 1), 4)  # Time limit between 1 and 4 seconds
        self.DepthLimit = min(max(DepthLimit, 3), 5)  # Depth limit between 3 and 5 plies
        self.StartTime = None  # Stores start time of the search
        self.BranchingFactor = 0  # Average branching factor in search

    def Minimax(self, BoardState, Depth, MaximizingPlayer):
        """Implements the Minimax algorithm to find the best move."""
        if self.StartTime is None:
            self.StartTime = time.time()
        if time.time() - self.StartTime > self.TimeLimit:
            return None  # Stop searching if time limit is exceeded

        self.StatesExpanded += 1  # Count expanded states
        if Depth == 0 or self.IsGameOver(BoardState):
            return self.Heuristic(BoardState)  # Evaluate board if depth is 0 or game is over

        MovesList = self.GetAllMoves(BoardState, 'B' if MaximizingPlayer else 'W')
        self.BranchingFactor = len(MovesList)

        if MaximizingPlayer:
            MaxEvaluation = -float('inf')
            for Move in MovesList:
                NewBoardState = self.MakeMove(BoardState, Move)
                Evaluation = self.Minimax(NewBoardState, Depth - 1, False)
                if Evaluation is None:
                    return None
                MaxEvaluation = max(MaxEvaluation, Evaluation)
            return MaxEvaluation
        else:
            MinEvaluation = float('inf')
            for Move in MovesList:
                NewBoardState = self.MakeMove(BoardState, Move)
                Evaluation = self.Minimax(NewBoardState, Depth - 1, True)
                if Evaluation is None:
                    return None
                MinEvaluation = min(MinEvaluation, Evaluation)
            return MinEvaluation

    def AlphaBeta(self, BoardState, Depth, Alpha, Beta, MaximizingPlayer):
        """Implements Alpha-Beta pruning to optimize the Minimax algorithm."""
        if self.StartTime is None:
            self.StartTime = time.time()
        if time.time() - self.StartTime > self.TimeLimit:
            return None  # Stop searching if time limit is exceeded

        self.StatesExpanded += 1  # Count expanded states
        if Depth == 0 or self.IsGameOver(BoardState):
            return self.Heuristic(BoardState)  # Evaluate board if depth is 0 or game is over

        MovesList = self.GetAllMoves(BoardState, 'B' if MaximizingPlayer else 'W')
        self.BranchingFactor = len(MovesList)

        if MaximizingPlayer:
            MaxEvaluation = -float('inf')
            for Move in MovesList:
                NewBoardState = self.MakeMove(BoardState, Move)
                Evaluation = self.AlphaBeta(NewBoardState, Depth - 1, Alpha, Beta, False)
                if Evaluation is None:
                    return None
                MaxEvaluation = max(MaxEvaluation, Evaluation)
                Alpha = max(Alpha, Evaluation)
                if Beta <= Alpha:
                    self.PrunedBranches += 1  # Count pruned branches
                    break  # Prune unnecessary search branches
            return MaxEvaluation
        else:
            MinEvaluation = float('inf')
            for Move in MovesList:
                NewBoardState = self.MakeMove(BoardState, Move)
                Evaluation = self.AlphaBeta(NewBoardState, Depth - 1, Alpha, Beta, True)
                if Evaluation is None:
                    return None
                MinEvaluation = min(MinEvaluation, Evaluation)
                Beta = min(Beta, Evaluation)
                if Beta <= Alpha:
                    self.PrunedBranches += 1  # Count pruned branches
                    break  # Prune unnecessary search branches
            return MinEvaluation

    def Heuristic(self, BoardState):
        """Evaluates the board by counting the difference between black and white pieces."""
        WhitePieces = sum(row.count('W') for row in BoardState)
        BlackPieces = sum(row.count('B') for row in BoardState)
        return BlackPieces - WhitePieces

    def GetAllMoves(self, BoardState, Player):
        """Returns all valid moves for the given player, including capturing moves."""
        MovesList = []
        for X in range(8):
            for Y in range(8):
                Piece = BoardState[X][Y]
                if Piece == ' ' or (Player == 'W' and Piece not in ('W', 'WK')) or (Player == 'B' and Piece not in ('B', 'BK')):
                    continue  # Skip empty squares and opponent's pieces

                Directions = [(1, -1), (1, 1)] if Piece == 'W' else [(-1, -1), (-1, 1)]
                if Piece in ('WK', 'BK'):
                    Directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Kings move in all directions

                for DX, DY in Directions:
                    NX, NY = X + DX, Y + DY
                    if 0 <= NX < 8 and 0 <= NY < 8 and BoardState[NX][NY] == ' ':
                        MovesList.append((X, Y, NX, NY))

                    JX, JY = X + 2 * DX, Y + 2 * DY
                    if 0 <= JX < 8 and 0 <= JY < 8 and 0 <= NX < 8 and 0 <= NY < 8:
                        if BoardState[NX][NY] not in (' ', Piece) and BoardState[JX][JY] == ' ':
                            MovesList.append((X, Y, JX, JY))  # Include jumps
        return MovesList

    def MakeMove(self, BoardState, Move):
        """Executes a move and returns the new board state."""
        StartingMoveLocationX, StartingMoveLocationY, TargetingMoveLocationX, TargetingMoveLocationY = Move
        NewBoardState = [row[:] for row in BoardState]  # Copy board

        NewBoardState[TargetingMoveLocationX][TargetingMoveLocationY] = NewBoardState[StartingMoveLocationX][StartingMoveLocationY]  # Move piece
        NewBoardState[StartingMoveLocationX][StartingMoveLocationY] = ' '  # Empty previous position

        if abs(TargetingMoveLocationX - StartingMoveLocationX) == 2:  # If it's a jump move, remove the captured piece
            CapturedX, CapturedY = (StartingMoveLocationX + TargetingMoveLocationX) // 2, (StartingMoveLocationY + TargetingMoveLocationY) // 2
            NewBoardState[CapturedX][CapturedY] = ' '

        return NewBoardState

    def IsGameOver(self, BoardState):
        """Determines if the game is over (one side has no pieces left)."""
        WhitePieces = sum(row.count('W') for row in BoardState)
        BlackPieces = sum(row.count('B') for row in BoardState)
        return WhitePieces == 0 or BlackPieces == 0
