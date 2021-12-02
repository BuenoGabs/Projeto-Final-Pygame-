import pygame
from CONFIG import WIDTH, HEIGHT, Inimigo_WIDTH, Inimigo_HEIGHT, protag_WHIDTH, protag_HEIGHT
from DADOS import load_dados, protag_img, PEW_SOUND, enemy_img, bullet_img, EXPLOSION_ANIM
from JOGO_Principal import *
from SPRITES import *


def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    dados = load_dados()

    # Criando um grupo de meteoros
    all_sprites = pygame.sprite.Group()
    all_enemy = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_enemy'] = all_enemy
    groups['all_bullets'] = all_bullets
    groups['all_boss'] = all_boss 

    # Criando o jogador
    player = Protag(groups, dados)
    all_sprites.add(player)
    # Criando os meteoros
    for i in range(8):
        enemy_img = Enemy(dados)
        all_sprites.add(enemy_img)
        all_enemy.add(enemy_img)

    DONE = 0
    PLAYING = 1
    state = PLAYING

    score = 0

    # ===== Loop principal =====
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        cont_boss = score // 100

    clock.tick(FPS)

    direita = True
    esquerda = True
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            state = DONE
        # Verifica se apertou alguma tecla.
        if event.type == pygame.KEYDOWN:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:

                player.image = protag_img_mirror
                bullet_img = bullet_img_mirror
                player.speedx -= 10
                    
            if event.key == pygame.K_RIGHT:
                player.speedx += 10
                player.image = protag_img
                bullet_img = bullet_img_mirror

            if event.key == pygame.K_UP:
                player.speedy -= 10
            if event.key == pygame.K_DOWN:
                player.speedy += 10
            if event.key == pygame.K_SPACE:
                player.shoot()
                bullet_img = bullet_img_mirror
        
        # Verifica se soltou alguma tecla.
        if event.type == pygame.KEYUP:
            # Dependendo da tecla, altera a velocidade.
            if event.key == pygame.K_LEFT:
                player.speedx += 10
            if event.key == pygame.K_RIGHT:
                player.speedx -= 10
            if event.key == pygame.K_UP:
                player.speedy += 10
            if event.key == pygame.K_DOWN:
                player.speedy -= 10
        
    
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

        state = DONE

    
    

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(dados['background'], (0, 0))
    # Desenhando inimigos
    all_sprites.draw(window)

    text_surface = dados['score_font'].render("{:010d}".format(score), True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH / 10,  10)
    window.blit(text_surface, text_rect)

    pygame.display.update()  # Mostra o novo frame para o jogador


with open('score.txt', 'r', encoding='utf-8') as arquivo:
    pontuacao_maxima = int(arquivo.read())

if pontuacao_maxima < score:
    with open('score.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(str(score))


while True:
    game_over_pont = pygame.font.Font('freesansbold.ttf', 20)
    game_over_pontos = game_over_pont.render(f'Pontuação máxima: {pontuacao_maxima}', True, (255,255,255))
    game_over_rect = game_over_pontos.get_rect()
    game_over_rect.midtop = (230, 120)
    print(game_over_rect.midtop)
    window.blit(game_over_pontos, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)

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

