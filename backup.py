import os
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

largura = 1000
altura = 700
tamanho_janela = (largura, altura)
espaco_entre_janelas = 20
total_largura_janelas_internas = 300 * 3 + espaco_entre_janelas * 2
posicao_x_primeira_janela = (largura - total_largura_janelas_internas) // 2
posicao_y_janelas = (altura - 290) // 2

background = pygame.image.load('background.bmp')
background = pygame.transform.scale(background, tamanho_janela)

janela_esquerda = pygame.Surface((300, 290))
janela_meio = pygame.Surface((300, 290))
janela_direita = pygame.Surface((300, 290))

janela_esquerda.fill((255, 0, 0))
janela_meio.fill((0, 0, 255))
janela_direita.fill((0, 255, 0))

diretorio_albums = "albums"
diretorio_principal = diretorio_albums

fonte = pygame.font.Font(None, 20)
pastas = []
arquivos = []

deslocamento_lista = 0

cores = {
    "selecionado": (0, 102, 204),
    "normal": (200, 200, 200),
    "texto_selecionado": (255, 255, 255),
    "texto_normal": (0, 102, 204),
}

def obter_pastas_e_arquivos(diretorio):
    pastas_e_arquivos = os.listdir(diretorio)
    pastas = [f for f in pastas_e_arquivos if os.path.isdir(os.path.join(diretorio, f))]
    arquivos = [f for f in pastas_e_arquivos if os.path.isfile(os.path.join(diretorio, f))]
    return pastas, arquivos

def desenhar_lista(surface, items, y_start):
    global deslocamento_lista
    for i, item in enumerate(items):
        if deslocamento_lista <= i < deslocamento_lista + 10:  # Mostrar apenas 10 itens por vez
            x = 10
            y = y_start + (i - deslocamento_lista) * 30
            cor_fundo = cores["selecionado"] if i == indice_selecionado else cores["normal"]
            cor_texto = cores["texto_selecionado"] if i == indice_selecionado else cores["texto_normal"]
            pygame.draw.rect(surface, cor_fundo, (x, y, 280, 25))
            texto = fonte.render(item, True, cor_texto)
            surface.blit(texto, (x + 5, y + 5))

def desenhar_pastas_e_arquivos(surface, pastas, arquivos):
    surface.fill((255, 255, 255))
    desenhar_lista(surface, pastas, 10)
    desenhar_lista(surface, arquivos, 10 + len(pastas) * 30)

def navegar_pasta(indice):
    global diretorio_principal, pastas, arquivos, indice_selecionado
    nova_pasta = os.path.join(diretorio_principal, pastas[indice])
    if os.path.isdir(nova_pasta):
        diretorio_principal = nova_pasta
        pastas, arquivos = obter_pastas_e_arquivos(diretorio_principal)
        indice_selecionado = 0

def voltar_pasta():
    global diretorio_principal, pastas, arquivos, indice_selecionado, deslocamento_lista
    if diretorio_principal != diretorio_albums and os.path.dirname(diretorio_principal) == diretorio_albums:
        diretorio_principal = diretorio_albums
        pastas, arquivos = obter_pastas_e_arquivos(diretorio_principal)
        indice_selecionado = 0
        deslocamento_lista = 0  # Resetar o deslocamento para o topo da lista
    else:
        pasta_pai = os.path.dirname(diretorio_principal)
        if os.path.exists(pasta_pai):
            diretorio_principal = pasta_pai
            pastas, arquivos = obter_pastas_e_arquivos(diretorio_principal)
            indice_selecionado = pastas.index(os.path.basename(diretorio_principal)) if os.path.basename(diretorio_principal) in pastas else 0
            deslocamento_lista = 0  # Resetar o deslocamento para o topo da lista


def adicionar_a_fila(caminho):
    with open("queue.txt", "r") as fila_leitura:
        musicas_na_fila = fila_leitura.readlines()
    
    # Verificar se o caminho já está na fila
    if caminho + "\n" not in musicas_na_fila:
        with open("queue.txt", "a") as fila:
            fila.write(caminho + "\n")

def remover_da_fila():
    with open("queue.txt", "r") as fila_leitura:
        musicas_na_fila = fila_leitura.readlines()
    
    # Remover o caminho da fila
    if musicas_na_fila:
        musicas_na_fila = musicas_na_fila[1:]  # Removendo a primeira música da lista
    
    with open("queue.txt", "w") as fila:
        fila.writelines(musicas_na_fila)

def tocar_proxima_se_houver():
    with open("queue.txt", "r") as fila_leitura:
        musicas_na_fila = fila_leitura.readlines()

    if musicas_na_fila:
        pygame.mixer.music.load(musicas_na_fila[0].strip())
        pygame.mixer.music.play()

def carregar_indice():
    try:
        with open("indice_selecionado.txt", "r") as arquivo:
            return int(arquivo.read())
    except FileNotFoundError:
        return 0

# Carregar o índice selecionado ou usar 0 se o arquivo não existir
indice_selecionado = carregar_indice()

# Definir o evento de música terminada
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

janela = pygame.display.set_mode(tamanho_janela)
pygame.display.set_caption("Jukebox")

pastas, arquivos = obter_pastas_e_arquivos(diretorio_principal)

tocar_proxima_se_houver()  # Tocar a próxima música na fila, se houver

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif evento.type == MUSIC_END:  # Quando a música atual terminar
            remover_da_fila()  # Remover da fila após a música terminar
            tocar_proxima_se_houver()  # Tocar a próxima música na fila, se houver
        elif evento.type == KEYDOWN:
            if evento.key == K_y:
                indice_selecionado = max(0, indice_selecionado - 1)
                deslocamento_lista = max(0, deslocamento_lista - 1) if indice_selecionado < deslocamento_lista else deslocamento_lista
            elif evento.key == K_g:
                indice_selecionado = min(len(pastas) + len(arquivos) - 1, indice_selecionado + 1)
                deslocamento_lista = min(len(pastas) + len(arquivos) - 10, deslocamento_lista + 1) if indice_selecionado >= deslocamento_lista + 10 else deslocamento_lista
            elif evento.key == K_e:
                if indice_selecionado < len(pastas):
                    navegar_pasta(indice_selecionado)
                elif indice_selecionado < len(pastas) + len(arquivos):
                    arquivo_selecionado = arquivos[indice_selecionado - len(pastas)]
                    if arquivo_selecionado.endswith(".mp3"):
                        caminho_arquivo = os.path.join(diretorio_principal, arquivo_selecionado)
                        adicionar_a_fila(caminho_arquivo)
                        if not pygame.mixer.music.get_busy():
                            tocar_proxima_se_houver()
            elif evento.key == K_a:
                voltar_pasta()
            elif evento.key == K_q:  # Se a tecla "Q" for pressionada, pular para a próxima música
                remover_da_fila()  # Remover da fila imediatamente ao pular
                tocar_proxima_se_houver()  # Tocar a próxima música na fila, se houver

    janela.blit(background, (0, 0))
    janela.blit(janela_esquerda, (posicao_x_primeira_janela, posicao_y_janelas))
    janela.blit(janela_meio, (posicao_x_primeira_janela + 320, posicao_y_janelas))
    janela.blit(janela_direita, (posicao_x_primeira_janela + 640, posicao_y_janelas))

    desenhar_pastas_e_arquivos(janela_esquerda, pastas, arquivos)

    pygame.display.update()