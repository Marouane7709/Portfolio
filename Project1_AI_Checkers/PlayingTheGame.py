from SearchToolBox import SearchToolBox
import time

def GetHumanMove(GUI):
    """Gets human player's move through GUI clicks."""
    print("Your turn! Select a piece and its destination on the GUI.")

    GUI.Clicks.clear()
    while len(GUI.Clicks) < 2:
        GUI.Screen.update()

    StartingMoveLocationX, StartingMoveLocationY = GUI.Clicks[0]
    TargetingMoveLocationX, TargetingMoveLocationY = GUI.Clicks[1]

    GUI.Clicks.clear()
    return StartingMoveLocationX, StartingMoveLocationY, TargetingMoveLocationX, TargetingMoveLocationY

def GameLoop(Board, GUI):
    """Interactive game loop integrating GUI and automatic bot moves with detailed analytics."""
    SearchToolbox = SearchToolBox()
    IsHumanTurn = True
    SearchDepth = 3

    while not Board.IsGameOver():
        GUI.Refresh()

        if IsHumanTurn:
            print("Your turn!")
            MoveSuccessful = False
            while not MoveSuccessful:
                X1, Y1, X2, Y2 = GetHumanMove(GUI)
                if Board.BoardState[X1][Y1].startswith('W'):
                    MoveSuccessful = Board.MovePiece(X1, Y1, X2, Y2)
                    if not MoveSuccessful:
                        print("Invalid move. Try again.")
                else:
                    GUI.Refresh()
                if not MoveSuccessful:
                    print("Invalid move, please select again.")
                GUI.Clicks.clear()

        else:
            print("Bot's turn!")
            SearchToolbox = SearchToolBox()
            SearchDepth = 3

            # Minimax
            BestMoveMinimax = None
            BestValueMinimax = -float('inf')
            SearchToolbox.StartTime = time.time()
            for Move in SearchToolbox.GetAllMoves(Board.BoardState, 'B'):
                NewBoard = SearchToolbox.MakeMove(Board.BoardState, Move)
                MoveValue = SearchToolbox.Minimax(NewBoard, SearchDepth, False)
                if MoveValue is None:
                    continue
                if MoveValue > BestValueMinimax:
                    BestValueMinimax = MoveValue
                    BestMoveMinimax = Move
            MinimaxTime = time.time() - SearchToolbox.StartTime
            StatesExpandedMinimax = SearchToolbox.StatesExpanded
            SearchToolbox.StatesExpanded = 0

            # Alpha-Beta
            BestMoveAB = None
            BestValueAB = -float('inf')
            Alpha, Beta = -float('inf'), float('inf')
            SearchToolbox.StartTime = time.time()
            for Move in SearchToolbox.GetAllMoves(Board.BoardState, 'B'):
                NewBoard = SearchToolbox.MakeMove(Board.BoardState, Move)
                MoveValue = SearchToolbox.AlphaBeta(NewBoard, SearchDepth, Alpha, Beta, False)
                if MoveValue is None:
                    continue
                if MoveValue > BestValueAB:
                    BestValueAB = MoveValue
                    BestMoveAB = Move
                Alpha = max(Alpha, BestValueAB)
            AlphaBetaTime = time.time() - SearchToolbox.StartTime
            StatesExpandedAB = SearchToolbox.StatesExpanded
            PrunedBranchesAB = SearchToolbox.PrunedBranches
            SearchToolbox.StatesExpanded = 0
            SearchToolbox.PrunedBranches = 0

            # Alpha-Beta Ordered
            BestMoveABOrdered = None
            BestValueABOrdered = -float('inf')
            Alpha, Beta = -float('inf'), float('inf')
            SearchToolbox.StartTime = time.time()
            Moves = SearchToolbox.GetAllMoves(Board.BoardState, 'B')

            # Separate capturing moves from regular moves
            CapturingMoves = [Move for Move in Moves if abs(Move[0] - Move[2]) == 2]  # Capturing moves have a distance of 2
            NonCapturingMoves = [Move for Move in Moves if Move not in CapturingMoves]

            # Prioritize captures if available
            OrderedMoves = CapturingMoves if CapturingMoves else NonCapturingMoves

            # Use heuristic ordering for better decision-making
            OrderedMoves = sorted(OrderedMoves, key=lambda M: SearchToolbox.Heuristic(SearchToolbox.MakeMove(Board.BoardState, M)), reverse=True)

            for Move in OrderedMoves:
                NewBoard = SearchToolbox.MakeMove(Board.BoardState, Move)
                MoveValue = SearchToolbox.AlphaBeta(NewBoard, SearchDepth, Alpha, Beta, False)
                if MoveValue is None:
                    continue
                if MoveValue > BestValueABOrdered:
                    BestValueABOrdered = MoveValue
                    BestMoveABOrdered = Move
                Alpha = max(Alpha, BestValueABOrdered)
            ABOrderedTime = time.time() - SearchToolbox.StartTime
            StatesExpandedABOrdered = SearchToolbox.StatesExpanded
            PrunedBranchesABOrdered = SearchToolbox.PrunedBranches
            SearchToolbox.StatesExpanded = 0
            SearchToolbox.PrunedBranches = 0

            if BestMoveABOrdered:
                Board.MovePiece(*BestMoveABOrdered)
                print(f"Bot moved (Alpha-Beta Ordered) from {(BestMoveABOrdered[0], BestMoveABOrdered[1])} to {(BestMoveABOrdered[2], BestMoveABOrdered[3])}")
                GUI.Refresh()

            # Display analytics clearly
            print("\nAlgorithm Comparison:")
            print("+----------------------+------------------+----------------+-----------------+-----------------+")
            print("| Algorithm            | Best Move        | States Expanded| Pruned Branches | Time Taken (s)  |")
            print("+----------------------+------------------+----------------+-----------------+-----------------+")
            print(f"| Minimax              | {BestMoveMinimax}        | {StatesExpandedMinimax:<14}| {'N/A':<15}| {MinimaxTime:<15.4f}|")
            print(f"| Alpha-Beta           | {BestMoveAB}        | {StatesExpandedAB:<14}| {PrunedBranchesAB:<15}| {AlphaBetaTime:<15.4f}|")
            print(f"| Alpha-Beta Ordered   | {BestMoveABOrdered}        | {StatesExpandedABOrdered:<14}| {PrunedBranchesABOrdered:<15}| {ABOrderedTime:<15.4f}|")
            print("+----------------------+------------------+----------------+-----------------+-----------------+\n")

        # Switch turns
        IsHumanTurn = not IsHumanTurn

    GUI.Refresh()
    print("Game Over!")
    if Board.HasValidMoves('W'):
        print("You win!")
    else:
        print("Bot wins!")
