import sys

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

class AIPlayer(TictactoePlayer):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
        self.board = [[-1,-1,-1], [-1,-1,-1], [-1,-1,-1]]
    def nextMove(self, possibleMoves):
        pass
    def acknowledge(self, move):
        i,j = move
        self.board[i][j] = 0
        
    
def play_a_new_game():
    #game = TicTacToe()
    human1 = HumanPlayer("human1", "X")
    human2 = HumanPlayer("human2", "O")
    game = TicTacToe(human1, human2)
    game.run()
    #pass

if __name__ == "__main__":
    play_a_new_game()
