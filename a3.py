import sys
import random
import math
class TicTacToe:
    """ TicTacToe class represents a tictactoe game that allows 2 players to play """
    def __init__(self, player1, player2):
        self.board = [["*","*","*"], ["*","*","*"], ["*","*","*"]]
        self.size = 3
        self.ply1 = player1
        self.ply2 = player2
        self.nPossibleMoves = 9
        self.adjMoveToWin = 3 # adjacent move to win
        self.winner = None

    def updateBoard(self, player, move):
        """ Update the board cell based on player move """
        i, j = move
        self.board[i][j] = player.symbol
        
    def getPossibleMoves(self):
        """ Return all possible moves on board """
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '*': # Might want to remove this hard-code
                    moves.append((i, j))
        return moves
    
    def get(self, row, col):
        """ Return the board cell (row, col)"""
        if row >= 0 and row < self.size and col >= 0 and col < self.size:
            return self.board[row][col]
        return None
    
    def hasConsecutiveKMoves(self, k, startPos, delta, player):
        """ Check if from startPos there are k consecutive moves of the same player"""
        row, col = startPos
        deltaRow, deltaCol = delta
        cnt = 0
        while self.get(row, col) == player.symbol:
            cnt += 1
            row, col = row + deltaRow, col + deltaCol
        row, col = startPos
        while self.get(row, col) == player.symbol:
            cnt += 1
            row, col = row - deltaRow, col - deltaCol
        cnt -= 1
        return cnt >= k
    
    def isWinner(self, move, player):
        """ Check if player's move can help them win"""
        k = self.adjMoveToWin
        if (self.hasConsecutiveKMoves(k, move, (1,0), player) or
            self.hasConsecutiveKMoves(k, move, (0,1), player) or
            self.hasConsecutiveKMoves(k, move, (1,1), player) or
            self.hasConsecutiveKMoves(k, move, (1,-1), player)):
            return True
        return False

    def printBoard(self):
        """ Print the board on screen """
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j], end=' ')
            print()
        
    def playerMove(self, ply):
        """ Get player's next move"""
        possibleMoves = self.getPossibleMoves() # Get all possible moves
        while self.nPossibleMoves > 0:
            plyMove = ply.nextMove(possibleMoves) # Let player make a move
            # Validate move
            if plyMove not in possibleMoves: # invalid move
                print("Invalid move. Please choose another move!!!")
                continue
            self.updateBoard(ply, plyMove) # Valid move, let's update the board
            self.nPossibleMoves -= 1 
            return plyMove 
    def boardMoveInstruction(self):
        print("Below is the movement number of each cell")
        for i in range(3):
            for j in range(3):
                print(3*i+j + 1, end=' ')
            print()
    def run(self):
        """ Run the game """
        self.boardMoveInstruction()
        print("************** Let's start *************")
        self.printBoard()
        while True:
            print("Player {name} turn".format(name = self.ply1.name))
            ply1Move = self.playerMove(self.ply1) # Let player1 move
            self.printBoard()
            # Check if game is over: either there is no other empty cell or one player has won
            isOver = self.nPossibleMoves == 0
            if self.isWinner(ply1Move, self.ply1):
                self.winner = self.ply1
                isOver = True
            if isOver:
                break
            
            self.ply2.acknowledge(ply1Move) # Acknowledge player2 about player1's move
            print("Player {name} turn".format(name = self.ply2.name))
            ply2Move = self.playerMove(self.ply2) # Let player2 move
            self.printBoard()
            # Check if game is over: either there is no other empty cell or player2 already won
            if self.isWinner(ply2Move, self.ply2):
                self.winner = self.ply2
                isOver = True
            if isOver:
                break
            self.ply1.acknowledge(ply2Move) # Acknowledge player1 about player2's move
        if not self.winner:
            print("Game over: Draw!!!")
        else:
            print("Game over: Player {name} has won".format(name = self.winner.name))

class TictactoePlayer:
    """ Interface for tictactoe player """
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol #the symbol displayed on board, normally just 'X' or 'O'

    def nextMove(self, possibleMoves):
        pass
    def acknowledge(self, move):
        pass

class HumanPlayer(TictactoePlayer):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
    def nextMove(self, possibleMoves):
        move = int(input("Choose a move number (1~9):"))
        return ((move-1)//3, (move-1)%3)
    
class TreeNode:
    """Node for monte carlo tree search"""
    def __init__(self, move, parent, player, state=None):
        self.move = move
        self.parent = parent
        self.state = state
        self.player = player
        if parent != None and state == None:
            copyState = list(map(list, parent.state))
            row, col = move
            copyState[row][col] = player * -1
            self.state = copyState
        self.AI = -1
        self.human = 1
        self.empty = 0
        self.children = []
        self.numOfVisited = 0
        self.numOfWins = 0
        
    def __hasKMoves(self, k, startPos, delta, player, board):
        """ Check if there is k consecutive moves of the same player starting from startPos """
        numRow = len(board)
        numCol = len(board[0])
        row, col = startPos
        deltaRow, deltaCol = delta
        cnt = 0
        while row >= 0 and row < numRow and col >= 0 and col < numCol and board[row][col] == player:
            cnt += 1
            row, col = row + deltaRow, col + deltaCol
        row, col = startPos
        while row >= 0 and row < numRow and col >= 0 and col < numCol and board[row][col] == player:
            cnt += 1
            row, col = row - deltaRow, col - deltaCol
        cnt -= 1
        return cnt >= k
    
    def __quickCheckWinner(self):
        """ Return 0 if draw, 1 if human wins and -1 if AI wins """
        move = self.move
        board = self.state
        if move:
            row, col = move
            player = self.state[row][col]
            if (self.__hasKMoves(3, move, (1,0), player, board) or
                self.__hasKMoves(3, move, (0,1), player, board) or
                self.__hasKMoves(3, move, (1,1), player, board) or
                self.__hasKMoves(3, move, (1,-1), player, board)):
                return player
        return 0

    def bestMove(self):
        """ Return the best move based on heuristic """
        def heuristic(node):
            if node.numOfVisited == 0 or node.parent.numOfVisited == 0:
                return float('inf')
            return node.numOfWins / node.numOfVisited + 1.4 * (math.sqrt(math.log(node.parent.numOfVisited)) / node.numOfVisited)
        return max(self.children, key=heuristic)
    
    def selectNextLegalMove(self):
        """ Return current node/move if it doesn't have children/next move, otherwise return a good legal move for rollout """
        # Find leaf node
        state = self
        if state.children != []:
            return state.bestMove()
        return state
    
    def expand(self):
        """ Expand children of a node/state if it doesn't have """
        player = self.player * -1
        if not self.children and self.__quickCheckWinner() == 0:
            for row in range(3):
                for col in range(3):
                    if self.state[row][col] == self.empty:
                        child = TreeNode(move=(row, col), player=player, parent=self)
                        self.children.append(child)
    def rollout(self):
        """ Perform random rollout/playout to see if this node can lead to a win/draw/lose and return the result """
        node = self
        currNode = TreeNode(move=node.move, player=node.player, parent=node.parent, state=node.state)
        currPlayer = node.player
        rolloutResult = 0 # draw
        while True:
            winner = currNode.__quickCheckWinner()
            if winner != 0:
                if winner == currPlayer:
                    rolloutResult = -1 # Opponent loses
                else:
                    rolloutResult = 1 # Opponent wins
                break
            currNode.expand()
            if not currNode.children:
                break
            currNode = random.choice(currNode.children) # Random rollout
        return rolloutResult # draw
        
    def bubbleUpResult(self, rolloutResult):
        """ Bubble the rollout result from the current node up to the root, something similar to bubble up operation in heap """
        currNode = self
        while currNode:
            currNode.numOfVisited += 1
            if rolloutResult > 0: # If player wins, then increase number of wins
                currNode.numOfWins += rolloutResult
            currNode = currNode.parent
            rolloutResult *= -1 # One wins, the other loses and vice versa
        
class AIPlayer(TictactoePlayer):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
        self.board = [[0,0,0], [0,0,0], [0,0,0]]
        self.opponentMoves = []
        self.AI = -1
        self.human = 1
        self.empty = 0
        
    def nextMove(self, possibleMoves):
        """ Return next move for AI player """
        move = self.searchGoodMove()
        row, col = move
        self.board[row][col] = self.AI
        return move
    
    def acknowledge(self, move):
        """ This method is triggered when the opponent did a move so that AI can record that move
            and decide which move it should take
        """
        self.opponentMoves.append(move)
        i,j = move
        self.board[i][j] = self.human
        
    def searchGoodMove(self, N=3000):
        """ Perform random rollouts to find a good move that potentially lead to a draw or win """
        def bestMovePolicy(node):
            return node.numOfVisited
        random.seed()
        recentOpponentMove = self.opponentMoves[-1] if self.opponentMoves else None
        copyBoard = list(map(list, self.board))
        # Generate root node
        root = TreeNode(move=recentOpponentMove, player=self.AI, state=copyBoard, parent=None)
        root.expand() # Expand children for root
        # Perform N rollouts
        for _ in range(N):
            legalMove = root.selectNextLegalMove() # Select best child according to win/lose/draw stats
            legalMove.expand() # Expand children for best child 
            rolloutState = legalMove 
            if rolloutState.children != []:
                rolloutState = rolloutState.selectNextLegalMove() # Start from the state where AI is about to take move
            rolloutRes = rolloutState.rollout() # perform random rollout/playout
            rolloutState.bubbleUpResult(rolloutRes) 

        bestMove = max(root.children, key=bestMovePolicy)
        return bestMove.move

        
            
def play_a_new_game():
    """ Run the tictactoe game with human and AI """
    print("======================= TicTacToe game =====================")
    
    humanFirst = int(input("Please choose to go first or second (0 for first, 1 for second):"))
    game = None
    if humanFirst == 0:
        human = HumanPlayer("human", "X")
        AI = AIPlayer("AI", "O")
        game = TicTacToe(human, AI)
    elif humanFirst == 1:
        human = HumanPlayer("human", "O")
        AI = AIPlayer("AI", "X")
        game = TicTacToe(AI, human)
    else:
        raise Exception("You have to choose either go first(0) or second(1)")
    game.run()

if __name__ == "__main__":
    play_a_new_game()
