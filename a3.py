import sys
import random
import math
import numpy as np
class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [["*","*","*"], ["*","*","*"], ["*","*","*"]]
        self.size = 3
        self.ply1 = player1
        self.ply2 = player2
        self.nPossibleMoves = 9
        self.adjMoveToWin = 3 # adjacent move to win
        self.winner = None

    def updateBoard(self, player, move):
        i, j = move
        self.board[i][j] = player.symbol
        
    def getPossibleMoves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '*': # Might want to remove this hard-code
                    moves.append((i, j))
        return moves
    
    def get(self, row, col):
        if row >= 0 and row < self.size and col >= 0 and col < self.size:
            return self.board[row][col]
        return None
    
    def hasConsecutiveKMoves(self, k, startPos, delta, player):
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
    
    def isWinner(self, curPos, player):
        k = self.adjMoveToWin
        if (self.hasConsecutiveKMoves(k, curPos, (1,0), player) or
            self.hasConsecutiveKMoves(k, curPos, (0,1), player) or
            self.hasConsecutiveKMoves(k, curPos, (1,1), player) or
            self.hasConsecutiveKMoves(k, curPos, (1,-1), player)):
            return True
        return False

    def printBoard(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j], end=' ')
            print()
        
    def playerMove(self, ply):
        possibleMoves = self.getPossibleMoves()
        while self.nPossibleMoves > 0:
            plyMove = ply.nextMove(possibleMoves)
            if plyMove not in possibleMoves:
                print("Invalid move. Please choose another move!!!")
                continue
            self.updateBoard(ply, plyMove)
            self.nPossibleMoves -= 1
            return plyMove 
        
    def run(self):
        self.printBoard()
        while True:
            print("Player {name} turn".format(name = self.ply1.name))
            ply1Move = self.playerMove(self.ply1)
            self.printBoard()
            isOver = self.nPossibleMoves == 0
            if self.isWinner(ply1Move, self.ply1):
                self.winner = self.ply1
                isOver = True
            if isOver:
                break
            self.ply2.acknowledge(ply1Move)
            print("Player {name} turn".format(name = self.ply2.name))
            ply2Move = self.playerMove(self.ply2)
            self.printBoard()
            if self.isWinner(ply2Move, self.ply2):
                self.winner = self.ply2
                isOver = True
            if isOver:
                break
            self.ply1.acknowledge(ply2Move)
        if not self.winner:
            print("Draw!!!")
        else:
            print("Player {name} wins".format(name = self.winner.name))

class TictactoePlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def nextMove(self, possibleMoves):
        pass
    def acknowledge(self, move):
        pass

class HumanPlayer(TictactoePlayer):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
    def nextMove(self, possibleMoves):
        row = int(input("Choose a row: "))
        col = int(input("Choose a col: "))
        return (row, col)
INF = float('inf')
class MCNode:
    """Monte carlo node"""
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
        self.children = []
        self.numOfVisited = 0
        self.numOfWins = 0

    def bestChild(self):
        def ucb(n, C=1.4):
            return np.inf if n.numOfVisited == 0 else n.numOfWins / n.numOfVisited + C * np.sqrt(np.log(n.parent.numOfVisited) / n.numOfVisited)
        def uct(node, C_PARAM=1.4):
            if node.numOfVisited == 0 or node.parent.numOfVisited == 0:
                return INF
            return node.numOfWins / node.numOfVisited + C_PARAM * (math.sqrt(math.log(node.parent.numOfVisited)) / node.numOfVisited)
        return max(self.children, key=ucb)
        
class AIPlayer(TictactoePlayer):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
        self.board = [[0,0,0], [0,0,0], [0,0,0]]
        self.opponentMoves = []
        self.AI = -1
        self.human = 1
        self.empty = 0
        
    def nextMove(self, possibleMoves):
        move = self.monteCarloTreeSearch()
        row, col = move
        self.board[row][col] = self.AI
        return move
    
    def acknowledge(self, move):
        self.opponentMoves.append(move)
        i,j = move
        self.board[i][j] = self.human
        
    def monteCarloTreeSearch(self, N=2000):
        
        def ucb(n, C=1.4):
            if n.numOfVisited == 0:
                return np.inf
            else:
                return n.numOfWins / n.numOfVisited + C * np.sqrt(np.log(n.parent.numOfVisited) / n.numOfVisited)
        def hasKMoves(k, startPos, delta, player, board):
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
                                                                                                 
        def select(n):
            """select a leaf node in the tree"""
            if n.children != []:
                return select(max(n.children, key=ucb))
            else:
                return n
        def selectLeafNode(node):
            # Find leaf node
            leaf = node
            while leaf.children != []:
                leaf = leaf.bestChild()
            return leaf
        def expand(node):
            player = node.player * -1
            if node.children == [] and quickCheckWinner(node.state, node.move) == 0:
                for row in range(3):
                    for col in range(3):
                        if node.state[row][col] == self.empty:
                            child = MCNode(move=(row, col), player=player, parent=node)
                            node.children.append(child)
            return select(node)
        def quickCheckWinner(board, move):
            """Return 0 if draw, 1 if human wins and -1 if AI wins"""
            row, col = move
            player = board[row][col]
            if (hasKMoves(3, move, (1,0), player, board) or
                hasKMoves(3, move, (0,1), player, board) or
                hasKMoves(3, move, (1,1), player, board) or
                hasKMoves(3, move, (1,-1), player, board)):
                return player
            return 0
        
        def simulate(node):
            currNode = MCNode(move=node.move, player=node.player, parent=node.parent, state=node.state)
            currPlayer = node.player
            rolloutResult = 0 # draw
            while True:
                winner = quickCheckWinner(currNode.state, currNode.move)
                expand(currNode)
                if winner != 0 or len(currNode.children) == 0:
                    if winner == currPlayer:
                        rolloutResult = -1 # Opponent loses
                    else:
                        rolloutResult = 1 # Opponent wins
                    break
                randNode = random.choice(currNode.children)
                currNode = MCNode(move=randNode.move, player=randNode.player, parent=randNode.parent, state=randNode.state)
            return rolloutResult # draw

        def backprop(node, rolloutResult):
            currNode = node
            while currNode:
                currNode.numOfVisited += 1
                if rolloutResult > 0:
                    currNode.numOfWins += rolloutResult
                currNode = currNode.parent
                rolloutResult *= -1 # One wins, the other loses and vice versa
        def _backprop(n, utility):
            """passing the utility back to all parent nodes"""
            if utility > 0:
                n.numOfWins += utility
                # if utility == 0:
                #     n.U += 0.5
            n.numOfVisited += 1
            if n.parent:
                _backprop(n.parent, -utility)
        def bestChildPolicy(child):
            return child.numOfVisited
        
        recentOpponentMove = self.opponentMoves[-1]
        copyBoard = list(map(list, self.board))
        root = MCNode(move=recentOpponentMove, player=self.AI, state=copyBoard, parent=None)
        #bestLeaf = select(root)
        for _ in range(N):
            bestLeaf = select(root)
            #print(bestLeaf.state, end=' ')
            rolloutNode = expand(bestLeaf)
            #print(rolloutNode.state)
            #print(rolloutNode.state, end=' ')
            #expand(bestLeaf)
            #rolloutNode = bestLeaf
            #if rolloutNode.children != []:
            #    rolloutNode = selectLeaf(bestLeaf)
            res = simulate(rolloutNode)
            #print(res)
            _backprop(rolloutNode, res)

        for child in root.children:
            print(child.numOfVisited, child.numOfWins)
        bestChild = max(root.children, key=bestChildPolicy)
        return bestChild.move
        #return (0,0)

        
            
def play_a_new_game():
    #game = TicTacToe()
    human1 = HumanPlayer("human1", "X")
    AI = AIPlayer("AI", "O")
    game = TicTacToe(human1, AI)
    game.run()
    #pass

if __name__ == "__main__":
    play_a_new_game()
