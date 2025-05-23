import pygame
import sys
import random
from random import randint

pygame.init()

# Configurações
LARGURA_TELA, ALTURA_TELA = 800, 600
LARGURA_MUNDO = 90000
CHAO_Y = 500
ALTURA_CHAO = 100

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

# Classe de Personagem Animado
class PersonagemAnimado(pygame.sprite.Sprite):
    def __init__(self, caminho_spritesheet, num_frames, frame_height, escala=2):
        super().__init__()
        self.frames = []
        self.index = 0
        self.timer = 0
        self.escala = escala

        spritesheet = pygame.image.load(caminho_spritesheet).convert_alpha()
        frame_width = spritesheet.get_width() // num_frames

        for i in range(num_frames):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (frame_width * escala, frame_height * escala))
            self.frames.append(frame)

        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.timer += 1
        if self.timer >= 7:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.timer = 0
        self.rect.midbottom = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Personagens
cavaleiro = PersonagemAnimado("assets/Knight_2/Run.png", 7, 128, 2)
samurai = PersonagemAnimado("assets/Samurai_Archer/Run.png", 8, 128, 2)

personagens_disponiveis = [cavaleiro, samurai]
personagem_escolhido = None

# Cristais
cristal = [
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_02_blue.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_03_violet.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_01_green.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_04_blue.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_03_violet.png').convert_alpha(), (50, 50)),
]

def tela_selecao_personagem():
    global personagem_escolhido
    selecionando = True

    botoes = [
        {"pos": (200, 300, 50, 50), "cor": (255, 0, 0), "personagem": personagens_disponiveis[1]},
        {"pos": (350, 300, 50, 50), "cor": (255, 255, 0), "personagem": personagens_disponiveis[0]},
    ]

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
                for botao in botoes:
                    rect = pygame.Rect(botao["pos"])
                    if rect.collidepoint(mx, my):
                        personagem_escolhido = botao["personagem"]
                        selecionando = False

        personagens_disponiveis[0].update(350, 200)
        personagens_disponiveis[1].update(200, 200)
        personagens_disponiveis[0].draw(tela)
        personagens_disponiveis[1].draw(tela)

        for botao in botoes:
            pygame.draw.rect(tela, botao["cor"], botao["pos"])

        pygame.display.flip()
        clock.tick(60)

cenario_imgs = [
    pygame.transform.scale(pygame.image.load(f"assets/FUNDO {i}.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
    for i in range(1, 5)
]
cenario0_img = pygame.transform.scale(pygame.image.load("assets/FUNDAO.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
chao_img = pygame.transform.scale(pygame.image.load("assets/CHÃO.png").convert_alpha(), (LARGURA_TELA, ALTURA_CHAO))

camadas = [{"img": cenario0_img, "offset": 0, "vel": 0.2}]
camadas += [{"img": cenario_imgs[i], "offset": 0, "vel": 0.4 + 0.2 * i} for i in range(4)]

obstaculos = []
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
        sucesso = True
        for obs in obstaculos:
            if abs(novo_rect.centerx - obs["rect"].centerx) < (largura // 2 + obs["rect"].width // 2 + 30) and abs(novo_rect.centery - obs["rect"].centery) < 40:
                sucesso = False
                break
        if tipo == "dano":
            sucesso = True
        tentativas += 1
    if sucesso:
        cristal_id = randint(0, 4) if tipo == "normal" else None
        obstaculos.append({"rect": novo_rect, "tipo": tipo, "causou_dano": False, "cristal": cristal_id, "coletado": False})

camera_x = 0
tela_selecao_personagem()
rodando = True

while rodando:
    dt = clock.tick(60)
    tela.fill((0, 0, 0))

    for camada in camadas:
        camada["offset"] -= camada["vel"]
        camada["vel"] += 0.0002

    for camada in camadas:
        largura_img = camada["img"].get_width()
        x = camada["offset"] % largura_img
        for i in range(-1, LARGURA_TELA // largura_img + 2):
            tela.blit(camada["img"], (x + i * largura_img, 0))

    for x in range(0, LARGURA_MUNDO, LARGURA_TELA):
        tela.blit(chao_img, (x - camera_x, CHAO_Y))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

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

    for obs in obstaculos:
        rect = obs["rect"]
        if obs["tipo"] == "normal" and jogador.colliderect(rect):
            if vel_x > 0:
                jogador.right = rect.left
            elif vel_x < 0:
                jogador.left = rect.right

    vel_y += gravidade
    jogador.y += vel_y
    no_chao = False

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

    for obs in obstaculos:
        if obs["tipo"] == "dano" and jogador.colliderect(obs["rect"]):
            if not obs["causou_dano"]:
                vidas -= 1
                obs["causou_dano"] = True
        else:
            obs["causou_dano"] = False

    if jogador.bottom >= CHAO_Y:
        jogador.bottom = CHAO_Y
        vel_y = 0
        no_chao = True

    camera_x = jogador.x - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))

    if personagem_escolhido:
        personagem_escolhido.update(jogador.x - camera_x, jogador.y)
        personagem_escolhido.draw(tela)

    for obs in obstaculos:
        rect = obs["rect"]
        if rect.right > camera_x and rect.left < camera_x + LARGURA_TELA:
            cor = VERMELHO if obs["tipo"] == "dano" else PRETO
            pygame.draw.rect(tela, cor, (rect.x - camera_x, rect.y, rect.width, rect.height))
            if cor == PRETO and obs["cristal"] is not None and not obs["coletado"]:
                tela.blit(cristal[obs["cristal"]], (rect.x - camera_x + rect.width // 2 - 25, rect.y - 50))

    for obs in obstaculos:
        if obs["tipo"] == "normal" and not obs["coletado"] and obs["cristal"] is not None:
            cristal_rect = pygame.Rect(obs["rect"].x + obs["rect"].width // 2 - 25, obs["rect"].y - 50, 50, 50)
            if jogador.colliderect(cristal_rect):
                obs["coletado"] = True
                cristais_coletados += 1

    pontuacao = jogador.x // 10
    tela.blit(fonte.render(f"Pontuação: {pontuacao}", True, PRETO), (10, 10))
    tela.blit(fonte.render(f"Cristais: {cristais_coletados}", True, (0, 100, 255)), (10, 80))
    for i in range(vidas):
        pygame.draw.rect(tela, VERMELHO, (10 + i * 30, 50, 20, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
