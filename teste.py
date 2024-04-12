import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações de tela
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Fonte para o texto
font = pygame.font.Font(None, 36)

# Lista de opções do menu
menu_options = ["Opção " + str(i) for i in range(1, 20)]
selected_option = 0  # Índice da opção selecionada
scroll_offset = 0  # Offset para o scroll

# Função para desenhar o menu
def draw_menu(screen):
    screen.fill(WHITE)
    visible_options = menu_options[scroll_offset : scroll_offset + 5]  # Mostra 5 opções por vez
    for i, option in enumerate(visible_options):
        text = font.render(option, True, BLACK if i == selected_option else WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50 + i * 50))
        screen.blit(text, text_rect)

# Inicializa a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu com Pygame")
clock = pygame.time.Clock()

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:  # Move para cima
                selected_option = max(0, selected_option - 1)
                if selected_option < scroll_offset:  # Scroll para cima
                    scroll_offset = max(0, scroll_offset - 1)
            elif event.key == pygame.K_k:  # Move para baixo
                selected_option = min(len(menu_options) - 1, selected_option + 1)
                if selected_option >= scroll_offset + 5:  # Scroll para baixo
                    scroll_offset = min(len(menu_options) - 5, scroll_offset + 1)
            elif event.key == pygame.K_RETURN:  # Seleciona a opção
                print("Selecionado:", menu_options[selected_option])

    # Desenha o menu
    draw_menu(screen)

    # Atualiza a tela
    pygame.display.flip()

    # Limita a taxa de quadros por segundo
    clock.tick(FPS)

# Finaliza o Pygame
pygame.quit()
sys.exit()