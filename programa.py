import pygame
import sys
import random

pygame.init()

# Tela e mundo
LARGURA_TELA, ALTURA_TELA = 800, 600
LARGURA_MUNDO = 90000
CHAO_Y = 500
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo Blocos Sólidos")
clock = pygame.time.Clock()

# Cores
VERDE = (0, 255, 0)
CINZA = (200, 200, 200)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Jogador
jogador = pygame.Rect(100, CHAO_Y - 50, 50, 50)
vel_x = 0
vel_y = 0
gravidade = 1
pulo = -18
no_chao = True
vidas = 5

# Imagem do personagem
personagem_img = pygame.image.load("assets/Herondina.png").convert_alpha()
personagem_img = pygame.transform.scale(personagem_img, (50, 50))

# Fonte
fonte = pygame.font.SysFont(None, 40)

# Obstáculos
obstaculos = []
for i in range(300):
    x = random.randint(300, LARGURA_MUNDO - 300)
    largura = random.choice([50, 100, 150])
    altura = 20  # espessura fixa para blocos flutuantes
    y = random.randint(300, CHAO_Y - 40)

    tipo = random.choice(["normal", "dano"])
    rect = pygame.Rect(x, y, largura, altura)
    obstaculos.append({"rect": rect, "tipo": tipo, "causou_dano": False})

# Loop principal
camera_x = 0
rodando = True
while rodando:
    dt = clock.tick(60)
    tela.fill(CINZA)

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
    for obs in obstaculos:
        rect = obs["rect"]
        if obs["tipo"] == "normal":
            if jogador.colliderect(rect):
                if vel_x > 0:
                    jogador.right = rect.left
                elif vel_x < 0:
                    jogador.left = rect.right

    # Gravidade
    vel_y += gravidade
    jogador.y += vel_y
    no_chao = False

    for obs in obstaculos:
        rect = obs["rect"]

        # Colisão apenas com blocos normais
        if obs["tipo"] == "normal":
            if jogador.colliderect(rect):
                if vel_y > 0 and jogador.bottom <= rect.top + vel_y:
                    jogador.bottom = rect.top
                    vel_y = 0
                    no_chao = True
                elif vel_y < 0 and jogador.top >= rect.bottom - vel_y:
                    jogador.top = rect.bottom
                    vel_y = 0

        # Dano com blocos vermelhos, mas sem bloqueio de movimento
        elif obs["tipo"] == "dano":
            if jogador.colliderect(rect) and not obs["causou_dano"]:
                vidas -= 1
                obs["causou_dano"] = True
                if vidas <= 0:
                    print("Game Over")
                    rodando = False

    # Colisão com o chão
    if jogador.bottom >= CHAO_Y:
        jogador.bottom = CHAO_Y
        vel_y = 0
        no_chao = True

    # Câmera
    camera_x = jogador.x - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))

    # Desenho do chão
    pygame.draw.rect(tela, VERDE, (0 - camera_x, CHAO_Y, LARGURA_MUNDO, ALTURA_TELA - CHAO_Y))

    # Desenho do jogador
    tela.blit(personagem_img, (jogador.x - camera_x, jogador.y))

    # Obstáculos
    for obs in obstaculos:
        cor = VERMELHO if obs["tipo"] == "dano" else PRETO
        rect = obs["rect"]
        pygame.draw.rect(tela, cor, (rect.x - camera_x, rect.y, rect.width, rect.height))

    # Pontuação
    pontuacao = jogador.x // 10
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

    # Vidas
    for i in range(vidas):
        pygame.draw.rect(tela, VERMELHO, (10 + i * 30, 50, 20, 20))

    pygame.display.flip()

pygame.quit()
