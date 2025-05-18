#programa que roda o jogo
import pygame
import random
import sys

# Inicialização
pygame.init()
tela = pygame.display.set_mode((1200, 1000))
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

pygame.quit()
