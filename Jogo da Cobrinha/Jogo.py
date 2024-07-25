import pygame as pg
from pygame.locals import *
from sys import exit
from random import randint

# inicializando o pygame
pg.init()

# configurações de tela
largura, altura = 1080, 640
pg.display.set_caption('Snake Game')
tela = pg.display.set_mode((largura, altura))

# configurações de velocidade
relogio = pg.time.Clock()
velocidade = 10

# configurações de texto
fonte = pg.font.SysFont('arial', 25, True, True)

# configurações de som
pg.mixer.music.set_volume(0.1)
musica_fundo = pg.mixer.music.load('backsound.mp3')
pg.mixer.music.play(-1)
som_moeda = pg.mixer.Sound('smw_coin.wav')

# configurações dos elementos
x_cobra, y_cobra = largura//2, altura//2
x_maca, y_maca = randint(25, 1055), randint(25, 615)

pontuacao, game_over = 0, False
lista_cobra, len_cobra = [], 5
x_controle, y_controle = 10, 0

# função de aumento do corpo da cobra
def aumenta_cobra(lista):
    for coord in lista_cobra:
        pg.draw.rect(tela, (0,255,0), (coord[0],coord[1],20,20))

# função para reiniciar o jogo
def reiniciar_jogo():
    global x_cobra, y_cobra, x_maca, y_maca, pontuacao, game_over, lista_cobra, len_cobra, x_controle, y_controle

    x_cobra, y_cobra = int(largura / 2), int(altura / 2)
    x_maca, y_maca = randint(25, 1055), randint(25, 615)

    pontuacao, game_over = 0, False
    lista_cobra, len_cobra = [], 5
    x_controle, y_controle = 10, 0

# loop do jogo
while True:

    # reiniciações do loop
    relogio.tick(30)
    tela.fill((255,255,255))
    pontos_txt = f'SCORE: {pontuacao}'
    texto_formatado = fonte.render(pontos_txt, True, (0,0,0))

    # loop para cada evento
    for event in pg.event.get():

        # sair do jogo
        if event.type == QUIT:
            pg.quit()
            exit()

        # teclas de movimento
        if event.type == KEYDOWN:
            if event.key == K_w and y_controle == 0:
                x_controle, y_controle = 0, -velocidade
            if event.key == K_a and x_controle == 0:
                x_controle, y_controle = -velocidade, 0
            if event.key == K_s and y_controle == 0:
                x_controle, y_controle = 0, velocidade
            if event.key == K_d and x_controle == 0:
                x_controle, y_controle = velocidade, 0

    # movimentação da cobra
    x_cobra += x_controle
    y_cobra += y_controle

    # desenho da cobra e da maçã na tela
    cobra = pg.draw.rect(tela, (0,255,0), (x_cobra,y_cobra,20,20))
    maca = pg.draw.circle(tela, (255,0,0), (x_maca,y_maca), 10)

    # colisão com a maçã
    if cobra.colliderect(maca):
        x_maca, y_maca = randint(25, 1055), randint(25, 615)
        som_moeda.play()
        pontuacao += 1
        len_cobra += 1

    # aumento do corpo da cobra
    lista_cabeca = [x_cobra, y_cobra]
    lista_cobra.append(lista_cabeca)

    # fim de jogo
    if lista_cobra.count(lista_cabeca) > 1:
        game_over_txt = fonte.render('GAME OVER', True, (0, 0, 0))
        pont_final_txt = fonte.render(f'SCORE: {pontuacao}', True, (0, 0, 0))
        mensagem_txt = fonte.render('Press SPACE to play again', True, (0,0,0))
        game_over = True

        # loop da tela de fim de jogo
        while game_over:

            # limpando a tela
            tela.fill((255, 255, 255))

            # loop para cada evento
            for event in pg.event.get():
                # sair do jogo
                if event.type == QUIT:
                    pg.quit()
                    exit()
                # reiniciar o jogo
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        reiniciar_jogo()

            # atualizando a tela
            tela.blit(game_over_txt, (largura//2 - 90, altura//2 - 60))
            tela.blit(pont_final_txt, (largura//2 - 80, altura//2 - 20))
            tela.blit(mensagem_txt, (largura//2 - 180, altura//2 + 220))
            pg.display.update()

    # teletransporte da cobra
    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra > altura:
        y_cobra = 0
    if y_cobra < 0:
        y_cobra = altura

    # limitação do corpo da cobra
    if len(lista_cobra) > len_cobra:
        del lista_cobra[0]
    aumenta_cobra(lista_cobra)

    # atualização da tela
    tela.blit(texto_formatado, (890,40))
    pg.display.update()