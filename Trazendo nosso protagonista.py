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
Inimigo_WIDTH = 20
Inimigo_HEIGHT = 10
protag_WHIDTH = 80
protag_HEIGHT = 80
font = pygame.font.SysFont(None, 70)
background = pygame.image.load('starfield.png').convert()  #carrega as imagens de fundo 
enemy_img = pygame.image.load('ghost2.jpg').convert_alpha() #carrega as imagens do inimigo
inimigo_img_small = pygame.transform.scale(enemy_img, (Inimigo_WIDTH, Inimigo_HEIGHT))
protag_img = pygame.image.load('rambo.png').convert_alpha()
protag_img = pygame.transform.scale(protag_img, (protag_WHIDTH, protag_HEIGHT))

class Protag(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
    
    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx

        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


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
all_sprites = pygame.sprite.Group()
# Criando o jogador
player =    Protag(protag_img)
all_sprites.add(player)
# Criando os Inimigos
for i in range(8):
    Inimigo = Enemy(enemy_img)
    all_sprites.add(Inimigo)

# ===== Loop principal =====
while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Atualiza estado do jogo
    # Atualizando a posição dos Inimigos
    all_sprites.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (0, 0))
    # Desenhando Inimigos
    all_sprites.draw(window)

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

