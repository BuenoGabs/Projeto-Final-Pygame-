# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
from CONFIG import WIDTH, HEIGHT, INIT, GAME, QUIT
from INIT_SCREEN import init_screen
from GAME_SCREEN import game_screen


pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shotto')

state = INIT
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        state = game_screen(window)
    else:
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

