# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 480
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shotto')

# ----- Inicia assets
Inimigo_WIDTH = 50
Inimigo_HEIGHT = 38
font = pygame.font.SysFont(None, 48)
background = pygame.image.load('background.jpg').convert()  #carrega as imagens de fundo 
enemy_img = pygame.image.load('rambo.png').convert_alpha() #carrega as imagens do inimigo
inimigo_img_small = pygame.transform.scale(enemy_img, (Inimigo_WIDTH, Inimigo_HEIGHT))

# ----- Inicia estruturas de dados
game = True
enemy_x = 200 # inicializa as variáveis que armazenam a posição do inimigo
# y negativo significa que está acima do topo da janela. O inimigo começa fora da janela
enemy_y = -Inimigo_HEIGHT
enemy_speedx = 3
enemy_speedy = 4 # inicializa as variáveis que armazenam a velocidade dos inimigos
inimigo_x = random.randint(0, WIDTH-Inimigo_WIDTH) #- o valor de x pode estar entre 0 e a largura da janela menos a largura da imagem do inimigo. Lembre-se que x é a esquerda do retângulo que define a imagem;
inimigo_y = random.randint(-100, -Inimigo_HEIGHT) #valores negativos significam que o inimigo está acima da janela. Vamos sortear valores de maneira que ele sempre comece o movimento de fora da janela, ou seja, o mais baixo possível é -Enemy_HEIGHT
inimigo_speedx = random.randint(-3, -3) #- se os valores da componente x da velocidade forem muito altos o inimigo vai se mover para um dos lados sem descer muito;
inimigo_speedy = random.randint(2,9) # - velocidades positivas em y significam que o inimigo vai se mover para baixo.
#variável para ajustar a velocidade
clock = pygame.time.Clock()
FPS = 30

# ===== Loop principal =====
while game:
    clock.tick(FPS)
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    # Atualizando a posição do meteoro
    inimigo_x += inimigo_speedx # atualiza a posição do inimigo;
    enemy_y += inimigo_speedy # atualiza a posição do inimigo;
    # Se o meteoro passar do final da tela, volta para cima
    if enemy_y > HEIGHT or enemy_x + Inimigo_WIDTH < 0 or enemy_x > WIDTH: # verifica se o inimigo saiu da tela. Nesse caso, faz ele voltar para a posição inicial.
        enemy_x = 200
        enemy_y = -Inimigo_HEIGHT # verifica se o meteoro saiu da tela. Nesse caso, faz ele voltar para a posição inicial.

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (0, 0))  # desenha a imagem de fundo e depois a imagem do meteoro
    window.blit(inimigo_img_small, (enemy_x, enemy_y)) # desenha a imagem de fundo e depois a imagem do inimigo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
