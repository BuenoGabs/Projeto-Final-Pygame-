import pygame
import os
from CONFIG import Inimigo_WIDTH, Inimigo_HEIGHT, protag_WHIDTH, protag_HEIGHT, img_DIR, sons_DIR, font_DIR


font = pygame.font.SysFont(None, 70)
background = pygame.image.load('img/space.png').convert()  #carrega as imagens de fundo 
enemy_img = pygame.image.load('img/ghost_pac_r.png').convert_alpha() #carrega as imagens do inimigo
inimigo_img_small = pygame.transform.scale(enemy_img, (Inimigo_WIDTH, Inimigo_HEIGHT))
protag_img = pygame.image.load('img/megamen.png').convert_alpha()
protag_img = pygame.transform.scale(protag_img, (protag_WHIDTH, protag_HEIGHT))
protag_img_mirror = pygame.transform.flip(protag_img, True, False)
bullet_img = pygame.image.load('img/laserRed16.png').convert_alpha()
bullet_img_mirror = pygame.transform.flip(bullet_img, True, False)
img_humberto = pygame.image.load('img/humberto')
EXPLOSION_ANIM = 'explosion_anim'
SCORE_FONT = 'score_font'
BOOM_SOUND = 'boom_sound'
DESTROY_SOUND = 'destroy_sound'
PEW_SOUND = 'pew_sound'

def load_dados():
    dados = {}
    dados[background] = pygame.image.load(os.path.join(img_DIR, 'space.png')).convert()
    dados[enemy_img] = pygame.image.load(os.path.join(img_DIR, 'ghost_pac_r.png')).convert_alpha()
    dados[inimigo_img_small] = pygame.transform.scale(dados['enemy_img'], (Inimigo_WIDTH, Inimigo_HEIGHT))
    dados[protag_img] = pygame.image.load(os.path.join(img_DIR, 'megamen.png')).convert_alpha()
    dados[protag_img] = pygame.transform.scale(dados['protag_img'], (protag_HEIGHT, protag_HEIGHT))
    dados[bullet_img] = pygame.image.load(os.path.join(img_DIR, 'laserRed16.png')).convert_alpha()
    dados[img_humberto] = pygame.image.load(os.path.join(img_DIR, 'img_humberto')).convert_alpha()
    
    explosion_anim = []
    for i in range(9):
        # Os arquivos de animação são numerados de 00 a 08
        filename = os.path.join(img_DIR, 'regularExplosion0{}.png'.format(i))
        img = pygame.image.load(filename).convert()
        img = pygame.transform.scale(img, (32, 32))
        explosion_anim.append(img)
    dados[EXPLOSION_ANIM] = explosion_anim
    dados[SCORE_FONT] = pygame.font.Font(os.path.join(font_DIR, 'PressStart2P.ttf'), 28)

    # Carrega os sons do jogo
    pygame.mixer.music.load(os.path.join(sons_DIR, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
    pygame.mixer.music.set_volume(0.4)
    dados[BOOM_SOUND] = pygame.mixer.Sound(os.path.join(sons_DIR, 'expl3.wav'))
    dados[DESTROY_SOUND] = pygame.mixer.Sound(os.path.join(sons_DIR, 'expl6.wav'))
    dados[PEW_SOUND] = pygame.mixer.Sound(os.path.join(sons_DIR, 'pew.wav'))
    return dados
