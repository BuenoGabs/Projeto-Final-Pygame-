# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame

pygame.init()

# ----- Gera tela principal
window = pygame.display.set_mode((500, 400))
pygame.display.set_caption('Gun')

# ----- Inicia estruturas de dados
game = True

# ----- Inicia assets
font = pygame.font.SysFont(None, 48) #fonte de texto
text = font.render('Atire pra matar', True, (255, 0, 0)) #mensagem #deixar o texto mais leve #cor
text_1 = font.render('Pressione Qualquer tecla', True, (0,0,255)) #mensagem #deixa o testo mais leve #cor
# ===== Loop principal =====
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(text, (10, 10)) #passando a posição do texto
    window.blit(text_1, (40, 100)) #passando a posição do texto

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

