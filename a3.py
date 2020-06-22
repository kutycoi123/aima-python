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

    def isWinner(self, currentPos, player):
        i, j = currentPos
        if self.board[i][j] != player.symbol:
            return False
        # Check vertical
        cnt = 0
        up, down = (j, j + 1)
        while up >= 0 or down < self.size:
            brk = True
            if up >= 0 and self.board[up][j] == player.symbol:
                cnt += 1
                up -= 1
                brk = False
            if down < self.size and self.board[down][j] == player.symbol:
                cnt += 1
                down += 1
                brk = False
            if brk:
                break
        if cnt >= self.adjMoveToWin:
            return True
        # Check horizontal
        cnt = 0
        left, right = (i, i + 1)
        while left >= 0 or right < self.size:
            brk = True
            if left >= 0 and self.board[i][left] == player.symbol:
                cnt += 1
                left -= 1
                brk = False
            if right < self.size and self.board[i][right] == player.symbol:
                cnt += 1
                right += 1
                brk = False
            if brk:
                break
        if cnt >= self.adjMoveToWin:
            return True

        # Check left diagonal
        cnt = 0
        leftUpRow, leftUpCol = (i, j)
        rightDownRow, rightDownCol= (i+1, j+1)
        while (leftUpRow >= 0 and leftUpCol >= 0) or (rightDownRow < self.size and rightDownCol < self.size):
            brk = True
            if leftUpRow >= 0 and leftUpCol >= 0 and self.board[leftUpRow][leftUpCol] == player.symbol:
                cnt += 1
                leftUpRow -= 1
                leftUpCol -= 1
                brk = False
            if rightDownCol < self.size and rightDownRow < self.size and self.board[rightDownRow][rightDownCol] == player.symbol:
                cnt += 1
                rightDownRow += 1
                rightDownCol += 1
                brk = False
            if brk:
                break
        if cnt >= self.adjMoveToWin:
            return True
        
        # Check right diagonal
        cnt = 0
        leftDownRow, leftDownCol = (i, j)
        rightUpRow, rightUpCol= (i-1, j+1)
        while (leftDownRow < self.size and leftDownCol >= 0 ) or (rightUpRow >= 0 and rightUpCol < self.size):
            brk = True
            if leftDownRow < self.size and leftDownCol >= 0 and self.board[leftDownRow][leftDownCol] == player.symbol:
                cnt += 1
                leftDownRow += 1
                leftDownCol -= 1
                brk = False
            if rightUpCol < self.size and rightUpRow >= 0 and self.board[rightUpRow][rightUpCol] == player.symbol:
                cnt += 1
                rightUpRow -= 1
                rightUpCol += 1
                brk = False
            if brk:
                break
        if cnt >= self.adjMoveToWin:
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
