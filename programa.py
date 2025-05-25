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

def load_spritesheet(path, frame_count, scale=2):
    sheet = pygame.image.load(path).convert_alpha()
    frame_width = sheet.get_width() // frame_count
    frame_height = sheet.get_height()
    frames = []
    for i in range(frame_count):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)
    return frames


tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Plataforma")
clock = pygame.time.Clock()

# Cores
VERDE = (0, 255, 0)
CINZA = (200, 200, 200)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Jogador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animations = {
            'idle': load_spritesheet("assets/Soldier_1/Idle.png", 7),
            'run': load_spritesheet("assets/Soldier_1/Run.png", 8),
            'hurt': load_spritesheet("assets/Soldier_1/Hurt.png", 3),
            'dead': load_spritesheet("assets/Soldier_1/Dead.png", 4),
            'shot': load_spritesheet("assets/Soldier_1/Shot_2.png", 4)
        }
        self.state = 'idle'
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.vel_y = 0
        self.flipped = False
        self.animation_timer = 0
        self.animation_delay = 100
        self.speed = 7
        self.no_chao = False

    def update(self, keys, dt, chao_y, obstaculos):
        self.state = 'idle'
        dx = 0

        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.state = 'run'
            self.flipped = False
        elif keys[pygame.K_LEFT]:
            dx = -self.speed
            self.state = 'run'
            self.flipped = True

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.no_chao:
            self.vel_y = -18
            self.no_chao = False

        # Movimento horizontal
        self.rect.x += dx
        for obs in obstaculos:
            rect = obs["rect"]
            if rect.colliderect(self.rect):
                if dx > 0:
                    self.rect.right = rect.left
                elif dx < 0:
                    self.rect.left = rect.right

        # Gravidade e movimento vertical
        self.vel_y += 1
        self.rect.y += self.vel_y
        self.no_chao = False

        for obs in obstaculos:
            rect = obs["rect"]
            if self.rect.colliderect(rect):
                if self.rect.bottom <= rect.top + 20:
                    self.rect.bottom = rect.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.rect.top >= rect.bottom - 20:
                    self.rect.top = rect.bottom
                    self.vel_y = 0

        if self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y
            self.vel_y = 0
            self.no_chao = True

        # Animação
        self.animation_timer += dt
        if self.animation_timer >= self.animation_delay:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.state]):
                self.frame_index = 0 if self.state != 'dead' else len(self.animations['dead']) - 1
            self.animation_timer = 0

        frame = self.animations[self.state][self.frame_index]
        self.image = pygame.transform.flip(frame, self.flipped, False)
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom

player = Player(100, CHAO_Y)
vel_x = 0
vel_y = 0
gravidade = 1
pulo = -18
no_chao = True
vidas = 5
vidas_extra_por_cristais = 0
cristais_coletados = 0
grupo_jogador = pygame.sprite.Group(player)


# Fonte
fonte = pygame.font.SysFont(None, 40)

# Personagens
personagens_disponiveis = [
    pygame.transform.scale(pygame.image.load("assets/Herondina.png").convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/Mariana.png").convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load("assets/Soldier_1/Attack.png").convert_alpha(), (50, 50)),
]

cristal = [
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_02_blue.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_03_violet.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_01_green.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_04_blue.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_03_violet.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_02_blue.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_03_violet.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_01_green.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_04_blue.png').convert_alpha(), (50, 50)),
    pygame.transform.scale(pygame.image.load('assets/Cristais/crystal_03_violet.png').convert_alpha(), (50, 50)),
]
personagem_escolhido = None


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

tela_selecao_personagem()

cenario0_img = pygame.transform.scale(pygame.image.load("assets/FUNDAO.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario1_img = pygame.transform.scale(pygame.image.load("assets/FUNDO 1.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario2_img = pygame.transform.scale(pygame.image.load("assets/FUNDO 2.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario3_img = pygame.transform.scale(pygame.image.load("assets/FUNDO 3.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario4_img = pygame.transform.scale(pygame.image.load("assets/FUNDO 4.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))

chao_img = pygame.transform.scale(pygame.image.load("assets/CHÃO.png").convert_alpha(), (LARGURA_TELA, ALTURA_CHAO))

camadas = [
    {"img": cenario0_img, "offset": 0, "vel": 0.2},
    {"img": cenario1_img, "offset": 0, "vel": 0.4},
    {"img": cenario2_img, "offset": 0, "vel": 0.6},
    {"img": cenario3_img, "offset": 0, "vel": 0.8},
    {"img": cenario4_img, "offset": 0, "vel": 1.0},
]

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
            if novo_rect.colliderect(obs["rect"]):
                sucesso = False
                break
        if tipo == "dano":
            sucesso = True
        tentativas += 1
    if sucesso:
        cristal_id = randint(0, 4) if tipo == "normal" else None
        obstaculos.append({"rect": novo_rect, "tipo": tipo, "causou_dano": False, "cristal": cristal_id, "coletado": False})

camera_x = 0
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

    keys = pygame.key.get_pressed()
    player.update(keys, dt, CHAO_Y, obstaculos)


    player.rect.x += vel_x

    for obs in obstaculos:
        rect = obs["rect"]
        if obs["tipo"] == "normal" and player.rect.colliderect(rect):
            if vel_x > 0:
                player.rect.right = rect.left
            elif vel_x < 0:
                player.rect.left = rect.right


    no_chao = False

    for obs in obstaculos:
        rect = obs["rect"]
        if player.rect.colliderect(rect):
            # Tratamento de colisão vertical
            if player.rect.bottom <= rect.top + 20:
                player.rect.bottom = rect.top
                vel_y = 0
                no_chao = True
            elif player.rect.top >= rect.bottom - 20:
                player.rect.top = rect.bottom
                vel_y = 0

            # Dano ocorre só uma vez por contato
            if obs["tipo"] == "dano":
                if not obs["causou_dano"]:
                    vidas -= 1
                    obs["causou_dano"] = True
                    if vidas <= 0:
                        rodando = False
        else:
            # Reseta para poder causar dano novamente na próxima colisão
            if obs["tipo"] == "dano":
                obs["causou_dano"] = False



    camera_x = player.rect.x - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))

    if personagem_escolhido:
        for sprite in grupo_jogador:
            sprite.rect.x -= camera_x  # aplicar câmera

        grupo_jogador.draw(tela)

        for sprite in grupo_jogador:
            sprite.rect.x += camera_x  # desfaz o ajuste da câmera


    for obs in obstaculos:
        rect = obs["rect"]
        if rect.right > camera_x and rect.left < camera_x + LARGURA_TELA:
            cor = VERMELHO if obs["tipo"] == "dano" else PRETO
            pygame.draw.rect(tela, cor, (rect.x - camera_x, rect.y, rect.width, rect.height))

            if obs["tipo"] == "normal" and obs["cristal"] is not None and not obs["coletado"]:
                cristal_rect = pygame.Rect(rect.x + rect.width // 2 - 25, rect.y - 50, 50, 50)
                tela.blit(cristal[obs["cristal"]], (cristal_rect.x - camera_x, cristal_rect.y))
                if player.rect.colliderect(cristal_rect):
                    obs["coletado"] = True
                    cristais_coletados += 1
                vidas_esperadas = cristais_coletados // 10
                if vidas_esperadas > vidas_extra_por_cristais:
                    vidas += vidas_esperadas - vidas_extra_por_cristais
                    vidas_extra_por_cristais = vidas_esperadas


    pontuacao = player.rect.x // 10
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))
    texto_cristais = fonte.render(f"Cristais: {cristais_coletados}", True, (0, 100, 255))
    tela.blit(texto_cristais, (10, 80))

    for i in range(vidas):
        pygame.draw.rect(tela, VERMELHO, (10 + i * 30, 50, 20, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
