import pygame
import sys
import random

# Inicialização
pygame.init()
LARGURA_TELA, ALTURA_TELA = 800, 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Pygame Alcidys e Nicolas")
clock = pygame.time.Clock()

# Mundo
LARGURA_MUNDO = 90000  # Mundo maior que a tela
CHAO_Y = 500

# Cores
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
CINZA = (200, 200, 200)
PRETO = (0, 0, 0)

# Jogador
jogador = pygame.Rect(100, CHAO_Y - 50, 50, 50)
vel_x = 0
vel_y = 0
gravidade = 1
pulo = -18
no_chao = True

# Obstáculos
obstaculos = []
for i in range(100):  # aumenta a frequência
    x = random.randint(300, 89800)  # dentro do mundo (evita início muito próximo)
    largura = random.choice([50, 100, 150])
    altura = random.randint(40, 100)
    y = CHAO_Y - random.randint(40, 120)
    obstaculos.append(pygame.Rect(x, y, largura, altura))

# Pontuação
pontuacao = 0
fonte = pygame.font.SysFont(None, 40)

# Loop principal
camera_x = 0
rodando = True
while rodando:
    dt = clock.tick(60)
    tela.fill(CINZA)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Entrada do jogador
    teclas = pygame.key.get_pressed()
    vel_x = 0
    if teclas[pygame.K_LEFT]:
        vel_x = -7
    if teclas[pygame.K_RIGHT]:
        vel_x = 7
    if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP]) and no_chao:
        vel_y = pulo
        no_chao = False


    # Movimento horizontal
    jogador.x += vel_x

    # Gravidade
    vel_y += gravidade
    jogador.y += vel_y

    # Colisão com o chão
    if jogador.bottom >= CHAO_Y:
        jogador.bottom = CHAO_Y
        vel_y = 0
        no_chao = True

    # Colisão com obstáculos
    for obs in obstaculos:
        if jogador.colliderect(obs):
            if vel_y > 0 and jogador.bottom <= obs.top + 20:
                jogador.bottom = obs.top
                vel_y = 0
                no_chao = True

    # Câmera segue o jogador
    camera_x = jogador.x - LARGURA_TELA // 2
    if camera_x < 0:
        camera_x = 0
    if camera_x > LARGURA_MUNDO - LARGURA_TELA:
        camera_x = LARGURA_MUNDO - LARGURA_TELA

    # Desenhar chão
    pygame.draw.rect(tela, VERDE, (0 - camera_x, CHAO_Y, LARGURA_MUNDO, ALTURA_TELA - CHAO_Y))

    # Desenhar jogador
    pygame.draw.rect(tela, AZUL, (jogador.x - camera_x, jogador.y, jogador.width, jogador.height))

    # Desenhar obstáculos
    for obs in obstaculos:
        pygame.draw.rect(tela, VERMELHO, (obs.x - camera_x, obs.y, obs.width, obs.height))

    # Mostrar pontuação (exemplo: baseada em posição x)
    pontuacao = jogador.x // 10
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

    pygame.display.flip()

pygame.quit()
