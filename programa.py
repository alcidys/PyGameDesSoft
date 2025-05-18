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
LARGURA_MUNDO = 90000
CHAO_Y = 500

# Cores
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
CINZA = (200, 200, 200)
PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
ROSA = (255, 105, 180)

# Jogador
jogador = pygame.Rect(100, CHAO_Y - 50, 50, 50)
vel_x = 0
vel_y = 0
gravidade = 1
pulo = -18
no_chao = True

# Vida
vida = 5
MAX_VIDA = 5

# Tipos de obstáculo
TIPOS_OBSTACULO = ["plataforma", "solido", "dano_bloco", "dano_plataforma"]
obstaculos = []

for _ in range(100):
    tipo = random.choice(TIPOS_OBSTACULO)
    x = random.randint(300, 89800)
    largura = random.choice([50, 100, 150])
    altura = 50

    if tipo in ["plataforma", "dano_plataforma"]:
        y = CHAO_Y - random.randint(100, 200)
    else:
        y = CHAO_Y - altura

    obstaculos.append({
        "rect": pygame.Rect(x, y, largura, altura),
        "tipo": tipo
    })

# Pontuação
pontuacao = 0
fonte = pygame.font.SysFont(None, 40)

# Função para desenhar barra de vida
def desenha_barra_vida(tela, vida):
    for i in range(MAX_VIDA):
        cor = (255, 0, 0) if i < vida else (100, 100, 100)
        pygame.draw.rect(tela, cor, (10 + i * 35, 50, 30, 30))

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

    # Colisões com obstáculos
    colidiu_com_sólido = False
    for obs in obstaculos:
        rect = obs["rect"]
        tipo = obs["tipo"]

        if jogador.colliderect(rect):
            # Plataforma
            if tipo in ["plataforma", "dano_plataforma"] and jogador.bottom <= rect.top + 10 and vel_y >= 0:
                jogador.bottom = rect.top
                vel_y = 0
                no_chao = True
                if tipo == "dano_plataforma":
                    vida -= 1
                continue

            # Sólido
            if tipo == "solido":
                if jogador.right > rect.left and jogador.left < rect.left:
                    jogador.right = rect.left
                elif jogador.left < rect.right and jogador.right > rect.right:
                    jogador.left = rect.right
                colidiu_com_sólido = True

            # Dano bloco
            if tipo == "dano_bloco":
                vida -= 1

    # Câmera
    camera_x = jogador.x - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))

    # Desenhar chão
    pygame.draw.rect(tela, VERDE, (0 - camera_x, CHAO_Y, LARGURA_MUNDO, ALTURA_TELA - CHAO_Y))

    # Desenhar jogador
    pygame.draw.rect(tela, AZUL, (jogador.x - camera_x, jogador.y, jogador.width, jogador.height))

    # Desenhar obstáculos
    for obs in obstaculos:
        rect = obs["rect"]
        tipo = obs["tipo"]
        cor = {
            "plataforma": PRETO,
            "solido": CINZA,
            "dano_bloco": VERMELHO,
            "dano_plataforma": ROSA
        }[tipo]
        pygame.draw.rect(tela, cor, (rect.x - camera_x, rect.y, rect.width, rect.height))

    # Mostrar pontuação
    pontuacao = jogador.x // 10
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

    # Mostrar barra de vida
    desenha_barra_vida(tela, vida)

    # Verifica fim de jogo
    if vida <= 0:
        texto_gameover = fonte.render("Game Over!", True, VERMELHO)
        tela.blit(texto_gameover, (LARGURA_TELA // 2 - 80, ALTURA_TELA // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        rodando = False

    pygame.display.flip()

pygame.quit()
