import pygame
import os

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo com Animação")
clock = pygame.time.Clock()

# Carregar imagens de animação
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

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animations = {
            'idle': load_spritesheet("assets/Soldier_1/Idle.png", 7),   # Corrigido: 7 quadros
            'run': load_spritesheet("assets/Soldier_1/Run.png", 8),
            'hurt': load_spritesheet("assets/Soldier_1/Hurt.png", 3),
            'dead': load_spritesheet("assets/Soldier_1/Dead.png", 4),
            'shot': load_spritesheet("assets/Soldier_1/Shot_2.png", 4)
        }
        self.state = 'idle'
        self.frame_index = 0
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(midbottom=(x, y))  # posicionar pelo "pé" do personagem
        self.speed = 5
        self.animation_timer = 0
        self.animation_delay = 100  # milissegundos
        self.flipped = False

    def update(self, keys, dt):
        prev_state = self.state
        self.state = 'idle'

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.state = 'run'
            self.flipped = False
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.state = 'run'
            self.flipped = True
        elif keys[pygame.K_h]:
            self.state = 'hurt'
        elif keys[pygame.K_d]:
            self.state = 'dead'
        elif keys[pygame.K_s]:
            self.state = 'shot'

        # Se mudou de estado, reseta o índice
        if self.state != prev_state:
            self.frame_index = 0
            self.animation_timer = 0

        # Atualiza animação
        self.animation_timer += dt
        if self.animation_timer >= self.animation_delay:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.state]):
                self.frame_index = 0 if self.state != 'dead' else len(self.animations['dead']) - 1
            self.animation_timer = 0

        frame = self.animations[self.state][self.frame_index]
        self.image = pygame.transform.flip(frame, self.flipped, False)
        # Manter a base dos pés ao trocar a imagem
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom

# Grupo de sprites
player = Player(100, 400)  # Corrigido: posição Y mais alta
all_sprites = pygame.sprite.Group(player)

# Loop principal
running = True
while running:
    dt = clock.tick(60)
    screen.fill((30, 30, 30))  # fundo escuro

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    all_sprites.update(keys, dt)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()