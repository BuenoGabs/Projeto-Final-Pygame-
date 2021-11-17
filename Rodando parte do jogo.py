# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random

pygame.init()

# ----- Gera tela principal
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shotto')

# ----- Inicia assets
Inimigo_WIDTH = 100
Inimigo_HEIGHT = 100
font = pygame.font.SysFont(None, 48)
background = pygame.image.load('starfield.png').convert()  #carrega as imagens de fundo 
enemy_img = pygame.image.load('ghost2.jpg').convert_alpha() #carrega as imagens do inimigo
inimigo_img_small = pygame.transform.scale(enemy_img, (Inimigo_WIDTH, Inimigo_HEIGHT))

class Enemy(pygame.sprite.Sprite):
    def  __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-Inimigo_WIDTH)
        self.rect.y = random.randint(-100, -Inimigo_HEIGHT)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy 

        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-Inimigo_WIDTH)
            self.rect.y = random.randint(-100, -Inimigo_HEIGHT)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)
        
#Definindo os novos tipos 
# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30

Inimigo1 = Enemy(enemy_img)
Inimigo2 = Enemy(enemy_img)

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
    Inimigo1.update()
    Inimigo2.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (0, 0))  # desenha a imagem de fundo e depois a imagem do meteoro
    window.blit(Inimigo1.image, Inimigo1.rect)
    window.blit(Inimigo2.image, Inimigo2.rect) # desenha a imagem de fundo e depois a imagem do inimigo
    
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
