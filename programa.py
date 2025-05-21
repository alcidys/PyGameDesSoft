import pygame
import sys
import random
from random import randint

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
cristais_coletados = 0

# Fonte
fonte = pygame.font.SysFont(None, 40)

# Opções de personagens
personagens_disponiveis = [
    pygame.transform.scale(pygame.image.load("assets/Herondina.png").convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/Mariana.png").convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/Jarina.png").convert_alpha(), (50, 50)),
]

cristal = [
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_02_blue.png').convert_alpha(), (50,50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_03_violet.png').convert_alpha(), (50,50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_01_green.png').convert_alpha(), (50,50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_04_blue.png').convert_alpha(), (50,50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_03_violet.png').convert_alpha(), (50,50)),
]
personagem_escolhido = None

# Função para exibir a tela de seleção de personagem
def tela_selecao_personagem():
    global personagem_escolhido

    selecionando = True
    while selecionando:
        tela.fill((30, 30, 30))
        titulo = fonte.render("Escolha seu personagem", True, (255, 255, 255))
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 50))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i in range(3):
                    rect = pygame.Rect(200 + i * 150, 200, 50, 50)
                    if rect.collidepoint(mx, my):
                        personagem_escolhido = personagens_disponiveis[i]
                        selecionando = False

        for i, img in enumerate(personagens_disponiveis):
            x = 200 + i * 150
            tela.blit(img, (x, 200))
            pygame.draw.rect(tela, (255, 255, 255), (x, 200, 50, 50), 2)

        pygame.display.flip()
        clock.tick(60)

# Chama a tela de seleção antes de começar
tela_selecao_personagem()

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
    sucesso = False

    while not sucesso and tentativas < 100:
        x = random.randint(300, LARGURA_MUNDO - 300)
        largura = random.choice([50, 100, 150])
        altura = 20
        y = random.randint(300, CHAO_Y - 40)
        tipo = random.choice(["normal", "dano"])

        novo_rect = pygame.Rect(x, y, largura, altura)
        distancia_minima = 30
        sucesso = True

        for obs in obstaculos:
            distancia_horizontal = abs(novo_rect.centerx - obs["rect"].centerx)
            distancia_vertical = abs(novo_rect.centery - obs["rect"].centery)
            if distancia_horizontal < (largura // 2 + obs["rect"].width // 2 + distancia_minima) and \
               distancia_vertical < 40:
                sucesso = False
                break

        if tipo == "dano":
            sucesso = True

        tentativas += 1

    if sucesso:
        cristal_id = randint(0, 4) if tipo == "normal" else None
        obstaculos.append({"rect": novo_rect,"tipo": tipo,"causou_dano": False,"cristal": cristal_id, "coletado": False})


# Loop principal
camera_x = 0
rodando = True
while rodando:
    dt = clock.tick(60)
    tela.fill((0, 0, 0))

    # Atualiza offsets (paralaxe)
    for camada in camadas:
        camada["offset"] -= camada["vel"]
        camada["vel"] += 0.0002

    # Desenha fundos com paralaxe
    for camada in camadas:
        largura_img = camada["img"].get_width()
        x = camada["offset"] % largura_img
        for i in range(-1, LARGURA_TELA // largura_img + 2):
            tela.blit(camada["img"], (x + i * largura_img, 0))

    # Chão
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

    jogador.x += vel_x

    # Colisão horizontal
    for obs in obstaculos:
        rect = obs["rect"]
        if obs["tipo"] == "normal" and jogador.colliderect(rect):
            if vel_x > 0:
                jogador.right = rect.left
            elif vel_x < 0:
                jogador.left = rect.right

    # Gravidade
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

    if jogador.bottom >= CHAO_Y:
        jogador.bottom = CHAO_Y
        vel_y = 0
        no_chao = True

    # Câmera
    camera_x = jogador.x - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))

    # Personagem
    if personagem_escolhido:
        tela.blit(personagem_escolhido, (jogador.x - camera_x, jogador.y))

    amarelo = (0,255,255)
    # Obstáculos
    for obs in obstaculos:
        rect = obs["rect"]
        if rect.right > camera_x and rect.left < camera_x + LARGURA_TELA:
            cor = VERMELHO if obs["tipo"] == "dano" else PRETO
            pygame.draw.rect(tela, cor, (rect.x - camera_x, rect.y, rect.width, rect.height))
            # Coleta de cristais
            for obs in obstaculos:
                if obs["tipo"] == "normal" and not obs["coletado"] and obs["cristal"] is not None:
                    cristal_id = pygame.Rect(obs["rect"].x + obs["rect"].width // 2 - 25, obs["rect"].y - 50, 50, 50)
                if jogador.colliderect(cristal_id):
                    obs["coletado"] = True
                    cristais_coletados += 1
            if cor == PRETO and obs["cristal"] is not None and not obs["coletado"]:
                tela.blit(cristal[obs["cristal"]],(rect.x - camera_x + rect.width // 2 - 25, rect.y - 50))


    # UI
    pontuacao = jogador.x // 10
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))
    texto_cristais = fonte.render(f"Cristais: {cristais_coletados}", True, (0, 100, 255))
    tela.blit(texto_cristais, (10, 80))


    for i in range(vidas):
        pygame.draw.rect(tela, VERMELHO, (10 + i * 30, 50, 20, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
