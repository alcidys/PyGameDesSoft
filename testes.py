import pygame
import sys
import random
from random import randint
pygame.init()
pygame.mixer.init()

# Configurações
LARGURA_TELA, ALTURA_TELA = 800, 600
LARGURA_MUNDO = 90000
CHAO_Y = 500
ALTURA_CHAO = 100
musica = pygame.mixer.Sound('assets/Random/jungle-explorer-video-game-theme-141773.ogg')
pulinho = pygame.mixer.Sound('assets/Random/video-game-jump-soundeffect-37532.ogg')
pega = pygame.mixer.Sound('assets/Random/snd_fragment_retrievewav-14728.ogg')

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
pulo = -20
no_chao = True
vidas = 5
vidas_extra_por_cristais = 0
djumps_por_cristais = 0
cristais_coletados = 0
djumps = cristais_coletados

# Fonte
fonte = pygame.font.SysFont(None, 40)

# Classe para personagem animado apenas com a animação de correr
class PersonagemAnimado:
    def __init__(self, pos_x, pos_y, spritesheet, n_frames):
        self.x = pos_x
        self.y = pos_y
        self.n_frames = n_frames

        # Carregar a spritesheet de corrida
        sprite_sheet = pygame.image.load(spritesheet).convert_alpha()
        largura_sheet, altura_sheet = sprite_sheet.get_size()
        largura_frame = largura_sheet // n_frames

        # Dividir a spritesheet em frames individuais
        self.frames = []
        for i in range(n_frames):
            frame = sprite_sheet.subsurface((i * largura_frame, 0, largura_frame, altura_sheet))
            self.frames.append(frame)

        # Estado inicial
        self.frame_index = 0
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.intervalo_frame = 100  # milissegundos entre frames

        self.largura = largura_frame
        self.altura = altura_sheet

    def atualizar_animacao(self):
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultimo_frame > self.intervalo_frame:
            self.frame_index = (self.frame_index + 1) % self.n_frames
            self.tempo_ultimo_frame = tempo_atual

    def desenhar(self, surface, camera_x=0, x_jogador=None, y_jogador=None):
        # Se passar a posição do jogador, desenha nela para seguir o jogador
        frame = self.frames[self.frame_index]
        if x_jogador is not None and y_jogador is not None:
            surface.blit(frame, (x_jogador - camera_x, y_jogador - self.altura))
        else:
            surface.blit(frame, (self.x - camera_x, self.y))

# Criando personagens animados
personagem1 = PersonagemAnimado(
    pos_x=0, pos_y=CHAO_Y - 50,
    spritesheet='assets/Samurai_Archer/Run.png',
    n_frames=8
)

personagem2 = PersonagemAnimado(
    pos_x=0, pos_y=CHAO_Y - 50,
    spritesheet='assets/Knight_2/Run.png',
    n_frames=7
)

personagens_disponiveis = [personagem1, personagem2]

cupuacu = PersonagemAnimado(
    pos_x = random.randint(1000, LARGURA_MUNDO - 100),
    pos_y = CHAO_Y - 100,
    spritesheet='assets/Random/Animacao Cupuacu.png',
    n_frames=7
)

cupuacu_rect = pygame.Rect(cupuacu.x, cupuacu.y, cupuacu.largura, cupuacu.altura)

# obstasculos
obstaculo_contato = pygame.transform.scale(pygame.image.load('assets/Random/OBSTACULO.png').convert_alpha(), (100, 20))
obstaculo_dano = pygame.transform.scale(pygame.image.load('assets/Random/OBSTACULO DANO.png').convert_alpha(), (100, 20))

#carrega os cristais que serao gerados
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

# Função para criar a tela de seleção
def tela_selecao_personagem():
    global personagem_escolhido

    # Carrega e ajusta a imagem de fundo
    imagem_fundo = pygame.image.load("assets/Telas/inicio.jpeg")
    imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))

    selecionando = True

    botoes = []
    textos_botoes = [" ", " ", "Informações"]
    mapa_escolhas = [1, 0, None]  # None para o botão de informações

    for i in range(len(textos_botoes)):
        if i < 2:
            # Botões de seleção lado a lado
            x = LARGURA_TELA // 2 - 250 + i * 300
            y = ALTURA_TELA // 2 + 115
        else:
            # Botão de informações abaixo dos outros
            x = LARGURA_TELA // 2 - 125  # Centralizado
            y = ALTURA_TELA // 2 + 200

        largura = 250
        altura = 50
        botoes.append(pygame.Rect(x, y, largura, altura))

    while selecionando:
        tela.blit(imagem_fundo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i, botao in enumerate(botoes):
                    if botao.collidepoint(mx, my):
                        if textos_botoes[i] == "Informações":
                            tela_informacoes()  # Chama a tela de informações
                        else:
                            personagem_escolhido = personagens_disponiveis[mapa_escolhas[i]]
                            selecionando = False

        pygame.display.flip()
        clock.tick(60)

# Função para exibir a tela de informações
def tela_informacoes():
    informacoes_img = pygame.image.load("assets/Telas/como jogar.jpeg")
    informacoes_img = pygame.transform.scale(informacoes_img, (LARGURA_TELA, ALTURA_TELA))

    mostrando = True
    while mostrando:
        tela.blit(informacoes_img, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_x:
                    mostrando = False  # Volta para a tela de seleção

        pygame.display.flip()
        clock.tick(60)



imagem_contexto = pygame.image.load("assets/Telas/contexto.jpeg")
imagem_contexto = pygame.transform.scale(imagem_contexto, (LARGURA_TELA, ALTURA_TELA))
def tela_contexto():
    imagem_contexto = pygame.image.load("assets/Telas/contexto.jpeg")
    imagem_contexto = pygame.transform.scale(imagem_contexto, (LARGURA_TELA, ALTURA_TELA))
    
    mostrando = True
    while mostrando:
        tela.blit(imagem_contexto, (0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                mostrando = False  # Sai da tela de contexto ao pressionar qualquer tecla
        
        pygame.display.flip()
        clock.tick(60)

imagem_vitoria = pygame.image.load("assets/Telas/venceu.jpeg")
imagem_vitoria = pygame.transform.scale(imagem_vitoria, (LARGURA_TELA, ALTURA_TELA))
def tela_vitoria():
    imagem_vitoria = pygame.image.load("assets/Telas/venceu.jpeg")
    imagem_vitoria = pygame.transform.scale(imagem_vitoria, (LARGURA_TELA, ALTURA_TELA))
    
    mostrando = True
    while mostrando:
        tela.blit(imagem_vitoria, (0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

imagem_derrota = pygame.image.load("assets/Telas/fim de jogo.jpeg")
imagem_derrota = pygame.transform.scale(imagem_derrota, (LARGURA_TELA, ALTURA_TELA))
def tela_derrota():
    imagem_derrota = pygame.image.load("assets/Telas/fim de jogo.jpeg")
    imagem_derrota = pygame.transform.scale(imagem_derrota, (LARGURA_TELA, ALTURA_TELA))
    
    mostrando = True
    while mostrando:
        tela.blit(imagem_derrota, (0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        clock.tick(60)


#carrega os sprites do plano de fundo e do chão
cenario0_img = pygame.transform.scale(pygame.image.load("assets/Random/FUNDAO.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario1_img = pygame.transform.scale(pygame.image.load("assets/Random/FUNDO 1.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario2_img = pygame.transform.scale(pygame.image.load("assets/Random/FUNDO 2.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario3_img = pygame.transform.scale(pygame.image.load("assets/Random/FUNDO 3.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
cenario4_img = pygame.transform.scale(pygame.image.load("assets/Random/FUNDO 4.png").convert_alpha(), (LARGURA_TELA, ALTURA_TELA))
chao_img = pygame.transform.scale(pygame.image.load("assets/Random/CHÃO.png").convert_alpha(), (LARGURA_TELA, ALTURA_CHAO))
#separa os sprites do cenario para animação do background
camadas = [
    {"img": cenario0_img, "offset": 0, "vel": 0.2},
    {"img": cenario1_img, "offset": 0, "vel": 0.4},
    {"img": cenario2_img, "offset": 0, "vel": 0.6},
    {"img": cenario3_img, "offset": 0, "vel": 0.8},
    {"img": cenario4_img, "offset": 0, "vel": 1.0},
]
#cria os obstaculos
obstaculos = []
ultimos_tipos = []  # Controla os últimos dois tipos ("normal" ou "dano")

for i in range(300):
    tentativas = 0
    sucesso = False

    while not sucesso and tentativas < 100:
        x = random.randint(300, LARGURA_MUNDO - 300)
        largura = random.choice([100])
        altura = 20
        y = random.randint(300, CHAO_Y - 40)

        # Evita 3 "dano" seguidos
        if ultimos_tipos[-2:] == ["dano", "dano"]:
            tipo = "normal"
        else:
            tipo = random.choice(["normal", "dano"])

        # Novo retângulo com margem de 20 px
        novo_rect = pygame.Rect(x - 20, y - 20, largura + 40, altura + 40)

        # Verifica se há sobreposição (com margem)
        sucesso = all(not novo_rect.colliderect(
            obs["rect"].inflate(40, 40)) for obs in obstaculos)

        tentativas += 1

    if sucesso:
        # Rect original (sem margem extra)
        final_rect = pygame.Rect(x, y, largura, altura)
        cristal_id = random.randint(0, 4) if tipo == "normal" else None

        obstaculos.append({
            "rect": final_rect,
            "tipo": tipo,
            "causou_dano": False,
            "cristal": cristal_id,
            "coletado": False
        })

        # Atualiza o histórico de tipos
        ultimos_tipos.append(tipo)

def espera_tecla():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False
        pygame.time.wait(10)

#set da camera e condição para rodar o jogo
camera_x = 0
rodando = True

#roda a musica
musica.set_volume(1)
musica.play()

# Executa tela de seleção
tela_selecao_personagem()

#loop principal que roda o jogo
tela_contexto()
while rodando:
    # set no clock para 60FPS
    dt = clock.tick(60)
    tela.fill((0, 0, 0))

    # leitura de comando e consequências
    teclas = pygame.key.get_pressed()
    vel_x = 0
    if teclas[pygame.K_LEFT]:
        vel_x = -7
    if teclas[pygame.K_RIGHT]:
        vel_x = 7

    # movimenta o personagem
    jogador.x += vel_x

    # cria o fundo com paralaxe (movimenta apenas se personagem se mover)
    if vel_x != 0:
        for camada in camadas:
            camada["offset"] -= vel_x * camada["vel"]
            # você pode deixar esse incremento se quiser aceleração com o tempo
            # camada["vel"] += 0.0002

    # desenha as camadas de fundo
    for camada in camadas:
        largura_img = camada["img"].get_width()
        x = camada["offset"] % largura_img
        for i in range(-1, LARGURA_TELA // largura_img + 2):
            tela.blit(camada["img"], (x + i * largura_img, 0))

    # desenha o chão
    for x in range(0, LARGURA_MUNDO, LARGURA_TELA):
        tela.blit(chao_img, (x - camera_x, CHAO_Y))

    # eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or evento.type == pygame.K_BACKSPACE:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if (evento.key == pygame.K_SPACE or evento.key == pygame.K_UP):
                if no_chao == True:
                    vel_y = pulo
                elif djumps > 0:
                    vel_y = pulo
                    pulinho.play()
                    djumps -= 1
                    cristais_coletados -= 1
                no_chao = False

    # define o tipo do cristal gerado
    for obs in obstaculos:
        rect = obs["rect"]
        if obs["tipo"] == "normal" and jogador.colliderect(rect):
            if vel_x > 0:
                jogador.right = rect.left
            elif vel_x < 0:
                jogador.left = rect.right

    # Gravidade e verificação se o jogador pode pular ou não
    vel_y += gravidade
    jogador.y += vel_y
    no_chao = False

    # tratamento de colisão
    for obs in obstaculos:
        rect = obs["rect"]
        if jogador.colliderect(rect):
            # Tratamento de colisão vertical
            if jogador.bottom <= rect.top + 20:
                jogador.bottom = rect.top
                vel_y = 0
                no_chao = True
            elif jogador.top >= rect.bottom - 20:
                jogador.top = rect.bottom
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

    if jogador.bottom >= CHAO_Y:
        jogador.bottom = CHAO_Y
        vel_y = 0
        no_chao = True

    camera_x = jogador.x - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))

    # anima e desenha o personagem escolhido
    if personagem_escolhido:
        personagem_escolhido.atualizar_animacao()
        personagem_escolhido.desenhar(
            tela,
            camera_x=camera_x,
            x_jogador=jogador.x,
            y_jogador=jogador.bottom
        )

    # Atualiza animação do cupuacu
        cupuacu.atualizar_animacao()

        # Atualiza rect do cupuacu
        cupuacu_rect.topleft = (cupuacu.x, cupuacu.y)

        # Desenha o cupuacu (ajustando posição com a câmera)
        cupuacu.desenhar(tela, camera_x=camera_x, x_jogador=cupuacu.x, y_jogador=cupuacu.y + cupuacu.altura)

        # Verifica colisão entre jogador e cupuacu para capturar
        if jogador.colliderect(cupuacu_rect):
            rodando = False  # termina o jogo quando capturado

    # gera os obstáculos conforme a posição do jogador
    
    for obs in obstaculos:
        rect = obs["rect"]
        if rect.right > camera_x and rect.left < camera_x + LARGURA_TELA:
            imagem_obstaculo = obstaculo_dano if obs["tipo"] == "dano" else obstaculo_contato
            tela.blit(imagem_obstaculo, (rect.x - camera_x, rect.y))

            if obs["tipo"] == "normal" and obs["cristal"] is not None and not obs["coletado"]:
                cristal_rect = pygame.Rect(rect.x + rect.width // 2 - 25, rect.y - 50, 50, 50)
                tela.blit(cristal[obs["cristal"]], (cristal_rect.x - camera_x, cristal_rect.y))
                if jogador.colliderect(cristal_rect):
                    obs["coletado"] = True
                    cristais_coletados += 1
                    pega.play()
                vidas_esperadas = cristais_coletados // 10
                if vidas_esperadas > vidas_extra_por_cristais:
                    vidas += vidas_esperadas - vidas_extra_por_cristais
                    vidas_extra_por_cristais = vidas_esperadas
                djumps_esperados = cristais_coletados // 1
                if djumps_esperados > djumps_por_cristais:
                    djumps += djumps_esperados - djumps_por_cristais
                    djumps_por_cristais = djumps_esperados

    # desenha o HUD na tela
    pontuacao = jogador.x // 10
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))
    texto_cristais = fonte.render(f"Cristais: {cristais_coletados}", True, (0, 100, 255))
    tela.blit(texto_cristais, (10, 80))
    for i in range(vidas):
        pygame.draw.rect(tela, VERMELHO, (10 + i * 30, 50, 20, 20))
    
    # define a tela de ganho ou de perda:

    if jogador.colliderect(cupuacu_rect):
        tela_vitoria()
        espera_tecla()
        tela_selecao_personagem()
        break  # ou return, se o loop estiver dentro de uma função
    elif vidas <= 0:
        tela_derrota()
        espera_tecla()
        tela_selecao_personagem()
        break  # ou return

    pygame.display.flip()

#encerra o jogo
pygame.quit()
sys.exit()