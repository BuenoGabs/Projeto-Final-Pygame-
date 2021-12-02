import random
import pygame
from CONFIG import WIDTH, HEIGHT, Inimigo_WIDTH, Inimigo_HEIGHT, protag_WHIDTH, protag_HEIGHT
from DADOS import protag_img, PEW_SOUND, enemy_img, bullet_img, EXPLOSION_ANIM


class Protag(pygame.sprite.Sprite):
    def __init__(self, groups, dados):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = dados[protag_img]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.groups = groups
        self.dados = dados
        self.bullet_img = bullet_img
        self.sentido_x = True
        #self.shoot_delay = 150

        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 100
    
    def update(self):
        # Atualização da posição do protagonista
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.speedx > 0:
            self.sentido_x = True
        if self.speedx < 0:
            self.sentido_x = False

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
        
        new_bullet = Bullet(self.bullet_img, pos_bullet, self.rect.centerx, self.sentido_x)
        self.groups['all_sprites'].add(new_bullet)
        self.groups['all_bullets'].add(new_bullet)
        self.dados[PEW_SOUND].play()

        


class Enemy(pygame.sprite.Sprite):
    def  __init__(self, dados):
        pygame.sprite.Sprite.__init__(self)

        self.image = dados[enemy_img]
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

class Boss(Enemy):
    def  __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-Inimigo_WIDTH)
        self.rect.y = random.randint(-100, -Inimigo_HEIGHT)
        self.speedx = random.randint(9, 16) * random.randint(-1, 1)
        self.speedy = random.randint(9, 16) 

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy 


        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-Inimigo_WIDTH)
            self.rect.y = random.randint(-100, -Inimigo_HEIGHT)
            self.speedx = random.randint(9, 16) * random.randint(-1, 1)
            self.speedy = random.randint(9, 16) 


# Classe dos tiros
class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, dados, bottom, centerx, sentido_x = True):
        # Construtor da classe mãe (Sprite). 
        pygame.sprite.Sprite.__init__(self)

        self.image = dados[bullet_img]
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        if sentido_x:
            self.speedx = 100 # Velocidade fixa para o lado
        else:
            self.speedx = -100


    def update(self):
        # A bala só se move no eixo x
        self.rect.x += self.speedx
         

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.bottom < 0:
            self.kill()

# Classe explosão
class Explosion(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, center, dados):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = dados[EXPLOSION_ANIM]

        # Inicia o processo de animação colocando a primeira imagem na tela.
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.explosion_anim[self.frame]  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.center = center  # Posiciona o centro da imagem

        # Guarda o tick da primeira imagem, ou seja, o momento em que a imagem foi mostrada
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 50

    def update(self):
        # Verifica o tick atual.
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1

            # Verifica se já chegou no final da animação.
            if self.frame == len(self.explosion_anim):
                # Se sim, tchau explosão!
                self.kill()
            else:
                # Se ainda não chegou ao fim da explosão, troca de imagem.
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
