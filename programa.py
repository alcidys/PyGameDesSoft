#programa que roda o jogo
import pygame
import random
import sys

# Inicialização
pygame.init()
LARGURA, ALTURA = 1200, 1000
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Temple Run Simplificado")
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

# Jogador
jogador = pygame.Rect(375, 500, 50, 50)
vel_x = 7
vel_y = 0
gravidade = 1
no_chao = True

# Obstáculos
obstaculos = []
tempo_criacao = 0
intervalo_obstaculo = 1500  # milissegundos

# Pontuação
pontuacao = 0
fonte = pygame.font.SysFont(None, 40)

# Função para criar obstáculos
def criar_obstaculo():
    x = random.randint(0, LARGURA - 50)
    return pygame.Rect(x, -50, 50, 50)

# Loop principal
rodando = True
while rodando:
    dt = clock.tick(60)
    tela.fill(BRANCO)
    tempo_criacao += dt
    pontuacao += dt // 10  

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Teclas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and jogador.left > 0:
        jogador.x -= vel_x
    if teclas[pygame.K_RIGHT] and jogador.right < LARGURA:
        jogador.x += vel_x
    if teclas[pygame.K_SPACE] and no_chao:
        vel_y = -18
        no_chao = False

    # Gravidade e pulo
    vel_y += gravidade
    jogador.y += vel_y
    if jogador.y >= 500:
        jogador.y = 500
        vel_y = 0
        no_chao = True

    # Criar obstáculos
    if tempo_criacao > intervalo_obstaculo:
        obstaculos.append(criar_obstaculo())
        tempo_criacao = 0

    # Atualizar obstáculos
    for obs in list(obstaculos):
        obs.y += 7
        if obs.top > ALTURA:
            obstaculos.remove(obs)
        if jogador.colliderect(obs):
            print("Pontuação:", pontuacao)
            pygame.quit()
            sys.exit()

    # Desenhar jogador e obstáculos
    pygame.draw.rect(tela, AZUL, jogador)
    for obs in obstaculos:
        pygame.draw.rect(tela, VERMELHO, obs)

    # Mostrar pontuação
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

    pygame.display.flip()

pygame.quit()
