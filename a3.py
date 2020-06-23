import sys
import random
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

class MCNode:
    """Monte carlo node"""
    def __init__(self, move, parent, player, state=None):
        self.move = move
        self.parent = parent
        self.state = state
        self.player = player
        if parent != None:
            copyState = list(map(list, parent.state))
            row, col = move
            copyState[row][col] = player * -1
            self.state = copyState
        self.children = []
        self.lose = 0
        self.winOrDraw = 0
        
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
        
    def monteCarloTreeSearch(self, N=5000):
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

        def gameResult(board):
            """Return 0 if draw or not complete game, 1 if opponent wins and -1 if AI wins"""
            numRow = len(board)
            numCol = len(board[0])
            for player in [self.AI,self.human]:
                for row in range(numRow):
                    for col in range(numCol):
                        if board[row][col] == player:
                            if (hasKMoves(3, (row, col), (1,0), player, board) or
                                hasKMoves(3, (row, col), (0,1), player, board) or
                                hasKMoves(3, (row, col), (1,1), player, board) or
                                hasKMoves(3, (row, col), (1,-1), player, board)):
                                return player
            return None
                                
        def quickCheckWinner(board, move):
            """Return 0 if draw, 1 if opponents wins and -1 if AI wins"""
            row, col = move
            player = board[row][col]
            if (hasKMoves(3, move, (1,0), player, board) or
                hasKMoves(3, move, (0,1), player, board) or
                hasKMoves(3, move, (1,1), player, board) or
                hasKMoves(3, move, (1,-1), player, board)):
                return player
            return None
                
        def isGameTerminated(board):
            for row in range(3):
                for col in range(3):
                    if board[row][col] == self.empty:
                        return False
            return True
        
        def expand(node):
            children = []
            player = node.player * -1
            for row in range(3):
                for col in range(3):
                    if node.state[row][col] == self.empty:
                        child = MCNode(move=(row, col),player=player,parent=node)
                        children.append(child)
            return children

    
        def select(node):
            return random.choice(node.children)

        def simulate(node):
            nextNode = node
            winner = None
            while True:
                winner = quickCheckWinner(nextNode.state, nextNode.move)
                if winner != None:
                    queue = expand(nextNode)
                    tmp = 1
                    while queue != []:
                        tmp += len(queue)
                        newQueue = []
                        for child in queue:
                            newQueue += expand(child)
                        queue = newQueue
                        
                    if winner == self.human:
                        node.lose += tmp
                        break
                    elif winner == self.AI:
                        node.winOrDraw += tmp
                        break
                if isGameTerminated(nextNode.state):
                    break
                children = expand(nextNode)
                nextNode = random.choice(children)

            if winner == None:
                node.winOrDraw += 1

        def heu1(minLose):
            def maxWinOrDraw(e):
                if e.lose == minLose:
                    return e.winOrDraw
                return -1
            return maxWinOrDraw

        def heu2(e):
            return e.lose
        
        def heu3(e):
            if e.lose == 0:
                return e.winOrDraw
            return e.winOrDraw / e.lose
        
        recentOpponentMove = self.opponentMoves[-1]
        copyBoard = list(map(list, self.board))
        root = MCNode(move=recentOpponentMove, player=self.AI, state=copyBoard, parent=None)
        root.children = expand(root)
        for _ in range(N):
            child = select(root)
            #winner = quickCheckWinner(child.state, child.move)
            #if winner != None:
            #    queue = expand(child)
            #    tmp = 1
            #    while queue != []:
            #        tmp += len(queue)
            #        newQueue = []
            #        for node in queue:
            #            newQueue += expand(node)
            #        queue = newQueue
            #        
            #    if winner == self.human:
            #        child.lose += tmp
            #        continue
            #    elif winner == self.AI:
            #        child.winOrDraw += tmp
            #        continue
            simulate(child)
        minLose = min(root.children, key=heu2).lose
        for child in root.children:
            print(child.lose, child.winOrDraw)
        bestChild = max(root.children, key=heu3)
        return bestChild.move

        
    
def play_a_new_game():
    #game = TicTacToe()
    human1 = HumanPlayer("human1", "X")
    AI = AIPlayer("AI", "O")
    game = TicTacToe(human1, AI)
    game.run()
    #pass

if __name__ == "__main__":
    play_a_new_game()
