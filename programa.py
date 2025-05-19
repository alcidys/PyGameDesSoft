import pygame
import sys
import random

pygame.init()

# Configurações
LARGURA_TELA, ALTURA_TELA = 800, 600
LARGURA_MUNDO = 90000
CHAO_Y = 500
ALTURA_CHAO = 100  # altura real da imagem do chão

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Plataforma")
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
try:
    personagem_img = pygame.image.load("assets/Herondina.png").convert_alpha()
    personagem_img = pygame.transform.scale(personagem_img, (50, 50))
except:
    personagem_img = pygame.Surface((50, 50))
    personagem_img.fill((0, 0, 255))

# Fonte
fonte = pygame.font.SysFont(None, 40)

# Carregamento das imagens de fundo
cenario0_img = pygame.transform.scale(pygame.image.load("assets/FUNDAO.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario1_img = pygame.transform.scale(pygame.image.load("assets/FUNDO 1.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario2_img = pygame.transform.scale(pygame.image.load("assets/FUNDO 2.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario3_img = pygame.transform.scale(pygame.image.load("assets/FUNDO 3.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario4_img = pygame.transform.scale(pygame.image.load("assets/FUNDO 4.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))

# Imagem do chão
chao_img = pygame.transform.scale(pygame.image.load("assets/CHÃO.png").convert_alpha(), (LARGURA_TELA, ALTURA_CHAO))

camadas = [
    {"img": cenario0_img, "offset": 0, "vel": 0.2},
    {"img": cenario1_img, "offset": 0, "vel": 0.4},
    {"img": cenario2_img, "offset": 0, "vel": 0.6},
    {"img": cenario3_img, "offset": 0, "vel": 0.8},
    {"img": cenario4_img, "offset": 0, "vel": 1.0},
]

# Obstáculos
obstaculos = []
espacamento_minimo = 50

for i in range(300):
    tentativas = 0
    colisao = True

    while colisao and tentativas < 100:
        x = random.randint(300, LARGURA_MUNDO - 300)
        largura = random.choice([50, 100, 150])
        altura = 20
        y = random.randint(300, CHAO_Y - 40)
        tipo = random.choice(["normal", "dano"])

        novo_rect = pygame.Rect(x, y, largura, altura)
        novo_rect_inflado = novo_rect.inflate(espacamento_minimo, espacamento_minimo)

        colisao = False
        for obs in obstaculos:
            if novo_rect_inflado.colliderect(obs["rect"]):
                colisao = True
                break
            if tipo == "dano":
                colisao = False

        tentativas += 1

    if not colisao:
        obstaculos.append({"rect": novo_rect, "tipo": tipo, "causou_dano": False})

# Loop principal
camera_x = 0
rodando = True
while rodando:
    dt = clock.tick(60)
    
    # Limpa a tela com preto
    tela.fill((0, 0, 0))

    # Atualiza os offsets das camadas (efeito paralaxe com aceleração)
    for camada in camadas:
        camada["offset"] -= camada["vel"]
        camada["vel"] += 0.0002  # aceleração contínua

    # Desenha as camadas de fundo com paralaxe
    for camada in camadas:
        largura_img = camada["img"].get_width()
        x = camada["offset"] % largura_img
        for i in range(-1, LARGURA_TELA // largura_img + 2):
            tela.blit(camada["img"], (x + i * largura_img, 0))

    # Desenhar o chão ao longo do mundo
    for x in range(0, LARGURA_MUNDO, LARGURA_TELA):
        tela.blit(chao_img, (x - camera_x, CHAO_Y))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Entrada
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

    # Colisão horizontal
    for obs in obstaculos:
        rect = obs["rect"]
        if obs["tipo"] == "normal" and jogador.colliderect(rect):
            if vel_x > 0:
                jogador.right = rect.left
            elif vel_x < 0:
                jogador.left = rect.right

    # Aplicar gravidade
    vel_y += gravidade
    jogador.y += vel_y
    no_chao = False

    # Colisão vertical
    for obs in obstaculos:
        rect = obs["rect"]
        if jogador.colliderect(rect):
            overlap_left = jogador.right - rect.left
            overlap_right = rect.right - jogador.left
            overlap_top = jogador.bottom - rect.top
            overlap_bottom = rect.bottom - jogador.top
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

            if min_overlap == overlap_top:
                jogador.bottom = rect.top
                vel_y = 0
                no_chao = True
            elif min_overlap == overlap_bottom:
                jogador.top = rect.bottom
                vel_y = 0
            elif min_overlap == overlap_left:
                jogador.right = rect.left
            elif min_overlap == overlap_right:
                jogador.left = rect.right

            if obs["tipo"] == "dano" and not obs["causou_dano"]:
                vidas -= 1
                obs["causou_dano"] = True
                if vidas <= 0:
                    rodando = False

    # Reset de dano
    for obs in obstaculos:
        if obs["tipo"] == "dano":
            if jogador.colliderect(obs["rect"]):
                if not obs["causou_dano"]:
                    vidas -= 1
                    obs["causou_dano"] = True
        else:
            obs["causou_dano"] = False

    # Colisão com chão
    if jogador.bottom >= CHAO_Y:
        jogador.bottom = CHAO_Y
        vel_y = 0
        no_chao = True

    # Câmera
    camera_x = jogador.x - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))

    # Desenhar personagem
    tela.blit(personagem_img, (jogador.x - camera_x, jogador.y))

    # Desenhar obstáculos
    for obs in obstaculos:
        rect = obs["rect"]
        if rect.right > camera_x and rect.left < camera_x + LARGURA_TELA:
            cor = VERMELHO if obs["tipo"] == "dano" else PRETO
            pygame.draw.rect(tela, cor, (rect.x - camera_x, rect.y, rect.width, rect.height))

    # UI
    pontuacao = jogador.x // 10
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

    for i in range(vidas):
        pygame.draw.rect(tela, VERMELHO, (10 + i * 30, 50, 20, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
