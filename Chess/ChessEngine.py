#Esse arquivo é responsável por guardar todas as informações sobre o estado atual do
# jogo de xadrez e determinar os movimentos válidos no estado vigente. Também terá um move log

class GameState():
    def __init__(self):
        #Tabuleiro escrito como uma lista 2d 8x8 e cada elemento tem 2 caracteres
        #O primeiro caractere representa a cor da peça, 'b' ou 'w'
        #O segundo caractere representa o tipo da peça, 'K', 'Q', 'R', 'B', 'K' ou 'p'
        #"--" representa os espaços em branco sem peças
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'K': self.getKingMoves, 'Q': self.getQueenMoves
                              }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

#Pega um movimento como parametro e executa. (Não funcional para roque, promoção de peão e en passant)
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        '''
        Desfazer o ultimo lance
        '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

    '''
    Todos os lances durante um check
    '''
    def getValidMoves(self):
        #1 Gerar todos os lances possiveis
        moves = self.getAllPossibleMoves()
        #2 para cada lance, fazer outros lances
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            #3 gerar todos os lances do adversário:
            #4 ver se ele ataca o seu rei
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #5 Se atacar o rei será inválido
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        False
    '''
    Todos os lances fora de uma posição de check
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #Encontra a função correta se baseando no dicionário
        return moves

    '''
    Pega todos os lances para o peão localizado na localização dada (r,c) e adiciona na lista de moves
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": #Mover 1 quadrado
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #Avançar 2 quadrados
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >=0: #capturas à esquerda
                if self.board[r-1][c-1][0] == "b" :
                    moves.append(Move((r,c), (r-1, c-1), self.board))
            if c+1 <= 7: #capturas à direita
                if self.board[r-1][c+1][0] == "b" :
                    moves.append(Move((r,c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c-1 >=0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c-1), self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))


    '''
    Pega todos os lances para a torre localizada na localização dada (r,c) e adiciona na lista de moves
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0<= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #espaço vazio
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #peça inimiga
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #peça amiga
                        break
                else: #Fora do tabuleiro
                    break
    '''
        Pega todos os lances para o cavalo localizado na localização dada (r,c) e adiciona na lista de moves
        '''

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
    '''
        Pega todos os lances para o bispo localizado na localização dada (r,c) e adiciona na lista de moves
        '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #espaço vazio
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #peça inimiga
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #peça amiga
                        break
                else: #Fora do tabuleiro
                    break
    '''
        Pega todos os lances para a rainha localizada na localização dada (r,c) e adiciona na lista de moves
        '''

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    '''
        Pega todos os lances para o rei localizado na localização dada (r,c) e adiciona na lista de moves
        '''

    def getKingMoves(self, r, c, moves):
        kingDirections = ((1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0))
        allyPiece = 'w' if self.whiteToMove else 'b'
        for i in range (1,8):
            endRow = r + kingDirections[i][0]
            endCol = c + kingDirections[i][1]
            if 0<= endRow < 8 and 0<= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyPiece:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

class Move():
    ranksToRows = { "1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Override o metodo igual
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self,r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

