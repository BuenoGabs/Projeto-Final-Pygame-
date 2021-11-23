# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import time 

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
WIDTH = 1400
HEIGHT = 750
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shotto')

# ----- Inicia assets
Inimigo_WIDTH = 1
Inimigo_HEIGHT = 1
protag_WHIDTH = 80
protag_HEIGHT = 80
font = pygame.font.SysFont(None, 70)
background = pygame.image.load('imagens Pygame/space.png').convert()  #carrega as imagens de fundo 
enemy_img = pygame.image.load('imagens Pygame/ghost2.jpg').convert_alpha() #carrega as imagens do inimigo
inimigo_img_small = pygame.transform.scale(enemy_img, (Inimigo_WIDTH, Inimigo_HEIGHT))
protag_img = pygame.image.load('imagens Pygame/megamen.png').convert_alpha()
protag_img = pygame.transform.scale(protag_img, (protag_WHIDTH, protag_HEIGHT))
protag_img_mirror = pygame.transform.flip(protag_img, True, False)
bullet_img = pygame.image.load('imagens Pygame/laserRed16.png').convert_alpha()
bullet_img_mirror = pygame.transform.flip(bullet_img, True, False)

# Carrega os sons do jogo
pygame.mixer.music.load('Backgroundmusic.mp3')
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound('expl3.wav')
destroy_sound = pygame.mixer.Sound('expl6.wav')
pew_sound = pygame.mixer.Sound('pew.wav')


class Protag(pygame.sprite.Sprite):
    def __init__(self, img, all_sprites, all_bullets, bullet_img, pew_sound):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.all_sprites = all_sprites
        self.all_bullets = all_bullets
        self.bullet_img = bullet_img
        self.pew_sound =pew_sound

    
    def update(self):
        # Atualização da posição da protagonista
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        #Contorno periodico
        if self.rect.right > WIDTH:
            self.rect.left = 0
            
            
        if self.rect.left < 0:
            self.rect.right = WIDTH

        if self.rect.bottom > HEIGHT:
            self.rect.top = 0
        
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT
        
      
    
    def shoot(self):
        pos_bullet = self.rect.top + 50
        new_bullet = Bullet(self.bullet_img, pos_bullet, self.rect.centerx)
        self.all_sprites.add(new_bullet)
        self.all_bullets.add(new_bullet)
        self.pew_sound.play()

        


class Enemy(pygame.sprite.Sprite):
    def  __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-Inimigo_WIDTH)
        self.rect.y = random.randint(-100, -Inimigo_HEIGHT)
        self.speedx = random.randint(-5, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy 

        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-Inimigo_WIDTH)
            self.rect.y = random.randint(-100, -Inimigo_HEIGHT)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)

# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedy = 100 # Velocidade fixa para o lado


    def update(self):
        # A bala só se move no eixo x
        self.rect.x += self.speedy
         

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()


# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30

all_sprites = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
# Criando o jogador
player = Protag(protag_img, all_sprites, all_bullets, bullet_img, pew_sound)
all_sprites.add(player)
bullet = Bullet(bullet_img, HEIGHT - 10, WIDTH / 2)  
# Criando os inimigos
for i in range(8):
    Inimigo = Enemy(enemy_img)
    all_sprites.add(Inimigo)
    all_enemy.add(Inimigo)

# ===== Loop principal =====
pygame.mixer.music.play(loops=-1)
while game:
    clock.tick(FPS)

    direita = True
    esquerda = True
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False
        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:

                player.image = protag_img_mirror
                bullet_img = bullet_img_mirror
                player.speedx -= 8
                    
            if event.key == pygame.K_RIGHT:
                player.speedx += 8
                player.image = protag_img
                bullet_img = bullet_img_mirror
        
            if event.key == pygame.K_UP:
                player.speedy -= 8
            if event.key == pygame.K_DOWN:
                player.speedy += 8
            if event.key == pygame.K_SPACE:
                
                player.shoot()
                bullet_img = bullet_img_mirror
        
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx += 8
            if event.key == pygame.K_RIGHT:
                player.speedx -= 8
            if event.key == pygame.K_UP:
                player.speedy += 8
            if event.key == pygame.K_DOWN:
                player.speedy -= 8
        
    
    # ----- Atualiza estado do jogo
    # Atualizando a posição dos inimigos

    all_sprites.update()

    hits = pygame.sprite.groupcollide(all_enemy, all_bullets, True, True)
    for Inimigos in hits:
        I = Enemy(enemy_img)
        all_sprites.add(I)
        all_enemy.add(I)

    # Verifica se houve colisão entre nave e meteoro
    hits = pygame.sprite.spritecollide(player, all_enemy, True)
    if len(hits) > 0:
        # TOCA O SOM DA COLISÃO
        boom_sound.play()
        time.sleep(1)

        game = False

    
    

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(background, (0, 0))
    # Desenhando inimigos
    all_sprites.draw(window)
 

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
 