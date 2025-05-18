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
ROSA = (255, 100, 180)
LARANJA = (255, 165, 0)

# Jogador
jogador = pygame.Rect(100, CHAO_Y - 50, 50, 50)
vel_x = 0
vel_y = 0
gravidade = 1
pulo = -18
no_chao = True
vidas = 5

personagem_img = pygame.image.load("assets/Herondina.png").convert_alpha()
personagem_img = pygame.transform.scale(personagem_img, (75, 75))

# Fonte
fonte = pygame.font.SysFont(None, 40)

# Obstáculos com tipos
obstaculos = []
obstaculos_dano_consecutivos = 0
metade_mundo = LARGURA_MUNDO // 2

for i in range(300):
    x = random.randint(300, LARGURA_MUNDO - 300)
    largura = random.choice([50, 100, 150])
    altura = random.randint(40, 100)

    if x < metade_mundo:
        if obstaculos_dano_consecutivos >= 2:
            tipo = random.choice(["plataforma", "solido"])
            obstaculos_dano_consecutivos = 0
        else:
            tipo = random.choice(["plataforma", "solido", "dano_bloco", "dano_plataforma"])
            if tipo in ["dano_bloco", "dano_plataforma"]:
                obstaculos_dano_consecutivos += 1
            else:
                obstaculos_dano_consecutivos = 0
    else:
        tipo = random.choice(["plataforma", "solido", "dano_bloco", "dano_plataforma"])

    if tipo in ["plataforma", "dano_plataforma"]:
        y = CHAO_Y - random.randint(100, 250)
    else:
        y = CHAO_Y - altura

    rect = pygame.Rect(x, y, largura, altura)
    obstaculos.append({"rect": rect, "tipo": tipo, "causou_dano": False})

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
        rect = obs["rect"]
        tipo = obs["tipo"]

        if jogador.colliderect(rect):
            if tipo in ["plataforma", "dano_plataforma"]:
                if vel_y > 0 and jogador.bottom <= rect.top + 20:
                    jogador.bottom = rect.top
                    vel_y = 0
                    no_chao = True
            elif tipo == "solido":
                if vel_y > 0 and jogador.bottom <= rect.top + 20:
                    jogador.bottom = rect.top
                    vel_y = 0
                    no_chao = True
                elif vel_y < 0 and jogador.top >= rect.bottom - 20:
                    jogador.top = rect.bottom
                    vel_y = 0
                elif jogador.right > rect.left and jogador.left < rect.left:
                    jogador.right = rect.left
                elif jogador.left < rect.right and jogador.right > rect.right:
                    jogador.left = rect.right
            elif tipo in ["dano_bloco", "dano_plataforma"]:
                if not obs["causou_dano"]:
                    vidas -= 1
                    obs["causou_dano"] = True
                    if vidas <= 0:
                        print("Game Over")
                        rodando = False

    # Câmera
    camera_x = jogador.x - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))

    # Desenhar chão
    pygame.draw.rect(tela, VERDE, (0 - camera_x, CHAO_Y, LARGURA_MUNDO, ALTURA_TELA - CHAO_Y))

    # Desenhar jogador (imagem)
    tela.blit(personagem_img, (jogador.x - camera_x, jogador.y))

    # Desenhar obstáculos
    for obs in obstaculos:
        cor = VERMELHO
        if obs["tipo"] == "plataforma":
            cor = PRETO
        elif obs["tipo"] == "solido":
            cor = PRETO
        elif obs["tipo"] == "dano_bloco":
            cor = VERMELHO
        elif obs["tipo"] == "dano_plataforma":
            cor = VERMELHO

        rect = obs["rect"]
        pygame.draw.rect(tela, cor, (rect.x - camera_x, rect.y, rect.width, rect.height))

    # Mostrar pontuação
    pontuacao = jogador.x // 10
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

    # Mostrar barra de vida
    for i in range(vidas):
        pygame.draw.rect(tela, VERMELHO, (10 + i * 30, 50, 20, 20))

    pygame.display.flip()

pygame.quit()
