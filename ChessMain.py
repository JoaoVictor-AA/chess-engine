#Esse é o arquivo main driver. Ela vai capturar os inputs e mostrar o GameState atual
import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 #Dimensão no xadrez é 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #para animações futuras
IMAGES = {}

'''
Inicialização de uma variável global de imagens. Será chamado uma única vez no main
'''

def loadImages():
    pieces = ["wp", "wR", "wB", "wQ", "wK", "wN", "bp", "bR", "bB", "bK", "bQ", "bN"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note que é possível acessar uma imagem por 'IMAGES['wp']'

'''
Esse será o main driver do código. Irá receber os inputs e atualizar a parte gráfica.
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages() #Uma única vez
    running = True
    sqSelected = () #manter o histórico de clicks, inicialmente nenhum elemento no tuple (row, col)
    playerClicks = [] #manter o histórico de clicks duplo tuple [(6, 4), (4,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #Posição (x,y) do mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsável por todos os gráficos em um jogo rodando
'''
def drawGameState(screen, gs):
    drawBoard(screen) #Desenha os quadrados do tabuleiro
    #Mostrar o highlight ou sugestões de lances (depois)
    drawPieces(screen, gs.board) #Desenha as peças no topo dos quadrados

'''
Desenha os quadrados do tabuleiro
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



'''
Desenhar as peças no tabuleiro usando o atual GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
