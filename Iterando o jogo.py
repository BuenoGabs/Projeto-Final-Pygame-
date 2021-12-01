# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import time
# from CONFIG import BLACK

from pygame.sprite import Group 

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
WIDTH = 1400
HEIGHT = 750
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shotto')

# ----- Inicia assets
Inimigo_WIDTH = 100
Inimigo_HEIGHT = 100
protag_WHIDTH = 80
protag_HEIGHT = 80
dados = {}
dados['background'] = pygame.image.load('img/space.png').convert()
dados['enemy_img'] =  pygame.image.load('img/ghost_pac_r.png').convert_alpha()
dados['inimigo_img_small'] = pygame.transform.scale(dados['enemy_img'], (Inimigo_WIDTH, Inimigo_HEIGHT))
dados['protag_img'] = pygame.image.load('img/megamen.png').convert_alpha()
dados['protag_img'] = pygame.transform.scale(dados['protag_img'], (protag_WHIDTH, protag_HEIGHT))
dados['bullet_img'] = pygame.image.load('img/laserRed16.png').convert_alpha()
dados['img_humberto'] = pygame.image.load('img/humberto2.png').convert_alpha()
explosion_anim = []
for i in range(9):
    # Os arquivos de animação são numerados de 00 a 08
    filename = 'img/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename).convert()
    img = pygame.transform.scale(img, (32, 32))
    explosion_anim.append(img)
dados["explosion_anim"] = explosion_anim
dados["score_font"] = pygame.font.Font('font/SuperMario256.ttf', 28)

font = pygame.font.SysFont(None, 70)
background = pygame.image.load('img/space.png').convert()  #carrega as imagens de fundo 
enemy_img = pygame.image.load('img/ghost_pac_r.png').convert_alpha() #carrega as imagens do inimigo
inimigo_img_small = pygame.transform.scale(enemy_img, (Inimigo_WIDTH, Inimigo_HEIGHT))
protag_img = pygame.image.load('img/megamen.png').convert_alpha()
protag_img = pygame.transform.scale(protag_img, (protag_WHIDTH, protag_HEIGHT))
protag_img_mirror = pygame.transform.flip(protag_img, True, False)
bullet_img = pygame.image.load('img/laserRed16.png').convert_alpha()
bullet_img_mirror = pygame.transform.flip(bullet_img, True, False)

img_humberto = dados['img_humberto']

# Sons do game
pygame.mixer.music.load('sons/Backgroundmusic.mp3')
pygame.mixer.music.set_volume(0.4)
dados['boom_sound'] = pygame.mixer.Sound('sons/expl3.wav')
dados['destroy_sound'] = pygame.mixer.Sound('sons/expl6.wav')
dados['pew_sound'] = pygame.mixer.Sound('sons/pew.wav')
dados['oc'] = pygame.mixer.Sound('sons/oc.mp3')


#----- MAIN MENU
click = False
def main_menu():
    click = False
    while True:
        window.fill((0,0,0))
    
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(0, 400, WIDTH, 75)
        button_2 = pygame.Rect(0, 500, WIDTH, 75)

        if button_1.collidepoint((mx, my)):
            if click:
                main_menu(window)

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
        
        window.fill(0,0,0)
        window.blit(background, (0, 0))
        pygame.draw.text('SHOTTO', font, (255, 255, 255), window, 600, 300)
        pygame.draw.rect(window, (0, 0, 255), button_1)
        pygame.draw.rect(window, (0, 0, 255), button_2)
        pygame.draw.text('JOGAR', font, (255, 255, 255), window, 625, 420)       
        pygame.draw.text('SAIR', font, (255, 255, 255), window, 640, 520)
        pygame.display.update()


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
        self.pew_sound = pew_sound
        self.sentido_x = True

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
        self.all_sprites.add(new_bullet)
        self.all_bullets.add(new_bullet)
        dados['pew_sound'].play()

        


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
    def __init__(self, img, bottom, centerx, sentido_x = True):
        # Construtor da classe mãe (Sprite). 
        pygame.sprite.Sprite.__init__(self)

        self.image = img
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
    def __init__(self, center, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Armazena a animação de explosão
        self.explosion_anim = assets['explosion_anim']

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



# ----- Inicia estruturas de dados
game = True
clock = pygame.time.Clock()
FPS = 30

all_boss = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_enemy = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()

# Criando o jogador
player = Protag(protag_img, all_sprites, all_bullets, bullet_img, dados) 
all_sprites.add(player)
bullet = Bullet(bullet_img, HEIGHT - 10, WIDTH / 2)

tem_boss = False

# Criando os inimigos
for i in range(5):
    Inimigo = Enemy(enemy_img)
    all_sprites.add(Inimigo)
    all_enemy.add(Inimigo)

score = 0
keys = {}
vidas = 5


# ===== Loop principal =====
pygame.mixer.music.play(loops=-1)
while game:
    cont_boss = score // 100

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
    for inimigo in hits:
        if inimigo not in all_boss:
            dados['destroy_sound'].play()
            I = Enemy(enemy_img)
            all_sprites.add(I)
            all_enemy.add(I)

            explosao = Explosion(inimigo.rect.center, dados)
            all_sprites.add(explosao)
            
            #agréssimo de pontos 
            score += 100
        else:
            dados['destroy_sound'].play()
            B = Boss(img_humberto)
            all_sprites.add(B)
            all_boss.add(B)
            explosao = Explosion(inimigo.rect.center, dados)
            all_sprites.add(explosao)
            score += 1000

    if  len(all_boss) < cont_boss: #score >= 100 and tem_boss == False:
    #3tem_boss = True
            boss = Boss(img_humberto)
            all_sprites.add(boss)
            all_enemy.add(boss)
            all_boss.add(boss)
  

    # Verifica se houve colisão 
    hits = pygame.sprite.spritecollide(player, all_enemy, True)
    if len(hits) > 0:
        # TOCA O SOM DA COLISÃO
        dados['boom_sound'].play()
        dados['oc'].play()
        pygame.mixer.music.stop()
        time.sleep(1)

        game = False

    
    

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(dados['background'], (0, 0))
    # Desenhando inimigos
    all_sprites.draw(window)

    text_surface = dados['score_font'].render("{:08d}".format(score), True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH / 10,  10)
    window.blit(text_surface, text_rect)

    pygame.display.update()  # Mostra o novo frame para o jogador

while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 50)
    game_over_screen = game_over_font.render('Game Over', True, (255,255,255))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (WIDTH  / 2,  HEIGHT / 2)
    window.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

