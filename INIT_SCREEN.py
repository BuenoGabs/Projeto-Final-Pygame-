import pygame
import random
from os import path

from CONFIG import IMG_DIR , BLACK, FPS, GAME, QUIT, WIDTH


def init_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega o fundo da tela inicial
    tela = pygame.image.load(path.join(IMG_DIR, 'inicio.png')).convert()
    tela_rect = tela.get_rect()

    running = True
    while running:
        window.fill((0,0,0))
    
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(0, 400, WIDTH, 75)
        button_2 = pygame.Rect(0, 500, WIDTH, 75)

        if button_1.collidepoint((mx, my)):
            if click:
                init_screen(window)

        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                # sys.exit()

       
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    # sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # A cada loop, redesenha o fundo e os sprites
        window.fill(BLACK)
        window.blit(tela, tela_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return GAME

# #click = False
# def main_menu():
#     click = False
#     while True:
#         window.fill((0,0,0))
    
 
#         mx, my = pygame.mouse.get_pos()
 
#         button_1 = pygame.Rect(0, 400, WIDTH, 75)
#         button_2 = pygame.Rect(0, 500, WIDTH, 75)

#         if button_1.collidepoint((mx, my)):
#             if click:
#                 main_menu(window)

#         if button_2.collidepoint((mx, my)):
#             if click:
#                 pygame.quit()
#                 # sys.exit()

       
#         click = False

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 # sys.exit()

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.quit()
#                     # sys.exit()

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     click = True
        
#         window.fill(0,0,0)
#         window.blit(background, (0, 0))
#         pygame.draw.text('SHOTTO', font, (255, 255, 255), window, 600, 300)
#         pygame.draw.rect(window, (0, 0, 255), button_1)
#         pygame.draw.rect(window, (0, 0, 255), button_2)
#         pygame.draw.text('JOGAR', font, (255, 255, 255), window, 625, 420)       
#         pygame.draw.text('SAIR', font, (255, 255, 255), window, 640, 520)
#         pygame.display.update()
