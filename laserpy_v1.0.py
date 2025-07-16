#Versão atual

#Bibliotecas
import pygame
import time
import random
import sys

#inicia o pygame
pygame.init()

# Configurações
fonte_info = pygame.font.SysFont("verdana", 11)
tamanho_bloco = 50
linhas_grid = 10
colunas_grid = 10
largura_tela = 600
altura_tela = 600
offset_x = tamanho_bloco
offset_y = tamanho_bloco

# Inicializa tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("LaserPy 1.0")
logo_img = pygame.image.load("logo_laserpy.png")
logo_img = pygame.transform.scale(logo_img, (350, 260))

# config de cores
COR_GRID = (60, 60, 60)
COR_FUNDO = (20, 20, 20)
COR_DESTINO = (255, 10, 10)
COR_ESPELHO = (180, 180, 255)
COR_LASER = (255, 0, 0)
COR_EMISSOR = (255, 0, 0)
COR_HOVER = (40, 40, 40)
COR_PAREDE = (100, 100, 100)

# config dicionario de direções e reflexos
direcoes = {
    "cima": (0, -1),
    "baixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0)
}

reflexoes = {
    0: {"esquerda": "baixo", "cima": "direita", "direita": "cima", "baixo": "esquerda"},
    1: {"esquerda": "cima", "baixo": "direita", "direita": "baixo", "cima": "esquerda"}
}

# configuração dos levels
levels = {
    1: {
        "emissor": (1, 2),
        "destino": (8, 9),
        "direcao": "direita",
        "movimentos_esperados": 5,
        "espelhos": [
            {"linha": 4, "coluna": 3, "rotacao": 0},
            {"linha": 4, "coluna": 2, "rotacao": 0}
        ],
        "paredes": [
            (0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,2),(7,3),(7,5),(7,6),(7,7),(7,8),(7,9),(9,9)
        ]
    },
    2: {
        "emissor": (1, 1),
        "destino": (8, 8),
        "direcao": "baixo",
        "movimentos_esperados": 5,
        "espelhos": [
            {"linha": 1, "coluna": 4, "rotacao": 0},
            {"linha": 2, "coluna": 6, "rotacao": 1},
            {"linha": 6, "coluna": 8, "rotacao": 1}
        ],
        "paredes": [
            (2,0),(2,5),(3,6),(5,8),(6,2),(6,5),(7,4),(7,8),(8,3),(8,7),(9,3)
        ]
    },
    3: {
        "emissor": (4, 5),
        "destino": (9, 0),
        "direcao": "cima",
        "movimentos_esperados": 5,
        "espelhos": [
            {"linha": 1, "coluna": 3, "rotacao": 0},
            {"linha": 1, "coluna": 9, "rotacao": 1},
            {"linha": 4, "coluna": 7, "rotacao": 1},
            {"linha": 3, "coluna": 7, "rotacao": 0},
            {"linha": 4, "coluna": 0, "rotacao": 1},
            {"linha": 9, "coluna": 6, "rotacao": 1}
        ],
        "paredes": [
            (0,0),(1,2),(2,4),(2,6),(1,7),(3,9),(5,7),(3,2),(5,1),(6,2),(7,0),(9,2),(7,5),(8,6),(9,9),(9,4)
        ]
    },
    4: {
        "emissor": (5, 1),
        "destino": (9, 8),
        "direcao": "cima",
        "movimentos_esperados": 5,
        "espelhos": [
            {"linha": 2, "coluna": 3, "rotacao": 0},
            {"linha": 4, "coluna": 2, "rotacao": 1},
            {"linha": 7, "coluna": 2, "rotacao": 1},
            {"linha": 6, "coluna": 0, "rotacao": 0},
            {"linha": 2, "coluna": 0, "rotacao": 1},
            {"linha": 3, "coluna": 0, "rotacao": 1},
            {"linha": 9, "coluna": 0, "rotacao": 1}
        ],
        "paredes": [
            (0,0),(0,2),(0,5),(2,7),(1,9),(4,8),(6,8),(8,8),(9,9),(8,7),(7,6),(5,5),(3,5),(3,4),(3,2),(4,0),(6,1),(5,3),(6,4),(7,3),(8,4),(9,3),(8,1),(2,6)
        ]
    }
}

# objeto espelho no jogo
class Espelho:
    def __init__(self, linha, coluna, rotacao=0):
        self.linha = linha
        self.coluna = coluna
        self.rotacao = rotacao
        self.tempo_ultimo_clique = 0

    def desenhar(self, tela):
        x = offset_x + self.coluna * tamanho_bloco
        y = offset_y + self.linha * tamanho_bloco
        if self.rotacao == 0:
            p1 = (x + 10, y + 40)
            p2 = (x + 40, y + 10)
        else:
            p1 = (x + 10, y + 10)
            p2 = (x + 40, y + 40)
        pygame.draw.line(tela, COR_ESPELHO, p1, p2, 3)

    def mover_para(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna

    def girar(self):
        self.rotacao = (self.rotacao + 1) % 2

# função de criação dos levels
def carregar_nivel(n):
    dados = levels[n]
    return (
        dados["emissor"],
        dados["destino"],
        dados["direcao"],
        [Espelho(e["linha"], e["coluna"], e["rotacao"]) for e in dados["espelhos"]],
        dados["paredes"],
        dados["movimentos_esperados"]
    )

# calculo das trajetórias (e iteração com o espelho)
def calcular_trajetoria_laser(emissor_pos, destino_pos, direcao_inicial, espelhos, paredes):
    segmentos = []
    linha, coluna = emissor_pos
    direcao = direcao_inicial
    dx, dy = direcoes[direcao]

    x_ini = offset_x + coluna * tamanho_bloco + tamanho_bloco // 2
    y_ini = offset_y + linha * tamanho_bloco + tamanho_bloco // 2

    while 0 <= linha < linhas_grid and 0 <= coluna < colunas_grid:
        x_fim = x_ini + dx * tamanho_bloco
        y_fim = y_ini + dy * tamanho_bloco
        segmentos.append(((x_ini, y_ini), (x_fim, y_fim)))

        linha += dy
        coluna += dx
        x_ini = x_fim
        y_ini = y_fim

        if (linha, coluna) in paredes:
            break

        for esp in espelhos:
            if (linha, coluna) == (esp.linha, esp.coluna):
                if direcao in reflexoes[esp.rotacao]:
                    direcao = reflexoes[esp.rotacao][direcao]
                    dx, dy = direcoes[direcao]
                else:
                    return segmentos

        if (linha, coluna) == destino_pos and not explodido:
            break

    return segmentos

#tela de game over - créditos
def exibir_tela_final():
    tela.fill(COR_FUNDO)
    fonte_titulo = pygame.font.SysFont("verdana", 24, bold=True)
    fonte_texto = pygame.font.SysFont("verdana", 14)

    linhas = [
        "Parabéns!",
        "Você conclui todos os levels!",
        "",
        "Desenvolvido por Evandro Ferreira",
        "www.EvandroGF.com.br",
        "Mais jogos: https://archaicbit.itch.io/",
        "",
        "Este é um projeto open source, criado com fins didáticos.",
        "Você pode baixar, estudar e melhorar o código.",
        "contato@evandrogf.com.br",
    ]

    y = 120
    for linha in linhas:
        texto = fonte_texto.render(linha, True, (220, 220, 220)) if "Parabéns" not in linha else fonte_titulo.render(linha, True, (255, 255, 255))
        tela.blit(texto, ((largura_tela - texto.get_width()) // 2, y))
        y += 30

    texto_sair = fonte_texto.render("Pressione qualquer tecla para sair", True, (180, 180, 180))
    tela.blit(texto_sair, ((largura_tela - texto_sair.get_width()) // 2, y + 30))
    pygame.display.flip()

    aguardando = True
    while aguardando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                aguardando = False

    pygame.quit()
    sys.exit()

def exibir_tela_inicial():
    fonte_titulo = pygame.font.SysFont("verdana", 40, bold=True)
    fonte_botao = pygame.font.SysFont("verdana", 18)
    fonte_rodape = pygame.font.SysFont("verdana", 12)

    botao_iniciar = pygame.Rect((largura_tela - 200) // 2, 360, 200, 40)
    botao_sair = pygame.Rect((largura_tela - 200) // 2, 420, 200, 40)

    aguardando = True
    while aguardando:
        tela.fill(COR_FUNDO)

        # logo
        tela.blit(logo_img, ((largura_tela - logo_img.get_width()) // 2, 40))

        # Botões
        mouse_pos = pygame.mouse.get_pos()

        for botao, texto in [(botao_iniciar, "Iniciar Jogo"), (botao_sair, "Sair")]:
            cor = (100, 100, 100) if botao.collidepoint(mouse_pos) else (80, 80, 80)
            pygame.draw.rect(tela, cor, botao, border_radius=5)
            texto_render = fonte_botao.render(texto, True, (255, 255, 255))
            tela.blit(texto_render, (botao.x + (botao.width - texto_render.get_width()) // 2,
                                     botao.y + (botao.height - texto_render.get_height()) // 2))

        # Rodapé
        rodape1 = fonte_rodape.render("Evandro Ferreira", True, (150, 150, 150))
        rodape2 = fonte_rodape.render("ArchaicBit 2025", True, (150, 150, 150))
        tela.blit(rodape1, ((largura_tela - rodape1.get_width()) // 2, altura_tela - 50))
        tela.blit(rodape2, ((largura_tela - rodape2.get_width()) // 2, altura_tela - 30))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    aguardando = False
                elif botao_sair.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

## iniciar mostrando o menu
exibir_tela_inicial()

nivel_atual = 4
emissor_pos, destino_pos, direcao_inicial, espelhos, paredes, movimentos_esperados = carregar_nivel(nivel_atual)
tempo_inicio_fase = pygame.time.get_ticks()
movimentos = 0
laser_atingiu = False
tempo_atingiu = None
explodido = False
particulas = []
arrastando = False
clock = pygame.time.Clock()
botao_reiniciar = pygame.Rect(largura_tela - 130, 10, 120, 25)

#loop do jogo
while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    coluna_mouse = (mouse_x - offset_x) // tamanho_bloco
    linha_mouse = (mouse_y - offset_y) // tamanho_bloco

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            tempo_atual = time.time()
            for esp in espelhos:
                if (linha_mouse, coluna_mouse) == (esp.linha, esp.coluna):
                    if tempo_atual - esp.tempo_ultimo_clique < 0.3:
                        esp.girar()
                    else:
                        arrastando = esp
                    esp.tempo_ultimo_clique = tempo_atual
            # clique no botão de reiniciar
            if botao_reiniciar.collidepoint(evento.pos):
                emissor_pos, destino_pos, direcao_inicial, espelhos, paredes, movimentos_esperados = carregar_nivel(nivel_atual)
                tempo_inicio_fase = pygame.time.get_ticks()
                movimentos = 0
                laser_atingiu = False
                tempo_atingiu = None
                explodido = False
                particulas = []

        elif evento.type == pygame.MOUSEBUTTONUP:
            if arrastando:
                if 0 <= linha_mouse < linhas_grid and 0 <= coluna_mouse < colunas_grid:
                    arrastando.mover_para(linha_mouse, coluna_mouse)
                    movimentos += 1
                arrastando = False

    tela.fill(COR_FUNDO)

    for linha in range(linhas_grid):
        for coluna in range(colunas_grid):
            x = offset_x + coluna * tamanho_bloco
            y = offset_y + linha * tamanho_bloco
            pygame.draw.rect(tela, COR_GRID, (x, y, tamanho_bloco, tamanho_bloco), 1)

    if 0 <= linha_mouse < linhas_grid and 0 <= coluna_mouse < colunas_grid:
        x_hover = offset_x + coluna_mouse * tamanho_bloco
        y_hover = offset_y + linha_mouse * tamanho_bloco
        pygame.draw.rect(tela, COR_HOVER, (x_hover, y_hover, tamanho_bloco, tamanho_bloco))

    linha, coluna = emissor_pos
    x = offset_x + coluna * tamanho_bloco
    y = offset_y + linha * tamanho_bloco
    if direcao_inicial == "direita":
        pontos = [(x + 10, y + 10), (x + 10, y + 40), (x + 40, y + 25)]
    elif direcao_inicial == "esquerda":
        pontos = [(x + 40, y + 10), (x + 40, y + 40), (x + 10, y + 25)]
    elif direcao_inicial == "cima":
        pontos = [(x + 10, y + 40), (x + 40, y + 40), (x + 25, y + 10)]
    elif direcao_inicial == "baixo":
        pontos = [(x + 10, y + 10), (x + 40, y + 10), (x + 25, y + 40)]
    pygame.draw.polygon(tela, COR_EMISSOR, pontos)

    segmentos = calcular_trajetoria_laser(emissor_pos, destino_pos, direcao_inicial, espelhos, paredes)
    laser_atingiu = False
    for seg in segmentos:
        # efeito de fluxo no laser (pontinhos se movendo ao longo do feixe)
        for i in range(0, 100, 20):
            t = (pygame.time.get_ticks() // 5 + i) % 100 / 100
            x_fluxo = seg[0][0] + (seg[1][0] - seg[0][0]) * t
            y_fluxo = seg[0][1] + (seg[1][1] - seg[0][1]) * t
            pygame.draw.circle(tela, (255, 0, 0), (int(x_fluxo), int(y_fluxo)), 2)

            
        pygame.draw.line(tela, COR_LASER, seg[0], seg[1], 2)
        fim_x, fim_y = seg[1]
        fim_col = (fim_x - offset_x) // tamanho_bloco
        fim_lin = (fim_y - offset_y) // tamanho_bloco
        if (fim_lin, fim_col) == destino_pos:
            laser_atingiu = True
            if tempo_atingiu is None:
                tempo_atingiu = pygame.time.get_ticks()

    linha, coluna = destino_pos
    x = offset_x + coluna * tamanho_bloco
    y = offset_y + linha * tamanho_bloco
    centro = (x + tamanho_bloco // 2, y + tamanho_bloco // 2)
    tempo_atual = pygame.time.get_ticks()

    if laser_atingiu:
        tempo_passado = (tempo_atual - tempo_atingiu) / 1000
        if tempo_passado < 2:
            raio = int(15 + tempo_passado * 3)
            pygame.draw.circle(tela, (255, 255, 255), centro, raio)
        elif not explodido:
            explodido = True
            for _ in range(50):
                particulas.append({
                    "x": centro[0],
                    "y": centro[1],
                    "vx": (2 - 4 * random.random()),
                    "vy": (2 - 4 * random.random()),
                    "tempo": tempo_atual
                })
    elif not explodido:
        pygame.draw.circle(tela, COR_DESTINO, centro, 15, 3)

    for parede in paredes:
        px = offset_x + parede[1] * tamanho_bloco
        py = offset_y + parede[0] * tamanho_bloco
        pygame.draw.rect(tela, COR_PAREDE, (px, py, tamanho_bloco, tamanho_bloco))

    novas_particulas = []
    for p in particulas:
        t = (tempo_atual - p["tempo"]) / 1000
        if t < 2:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            pygame.draw.circle(tela, (255, 0, 0), (int(p["x"]), int(p["y"])), 3)
            novas_particulas.append(p)
    particulas = novas_particulas

    for esp in espelhos:
        esp.desenhar(tela)

    if explodido and not particulas:
        nivel_atual += 1
        if nivel_atual in levels:
            emissor_pos, destino_pos, direcao_inicial, espelhos, paredes, movimentos_esperados = carregar_nivel(nivel_atual)
            tempo_inicio_fase = pygame.time.get_ticks()
            movimentos = 0
            laser_atingiu = False
            tempo_atingiu = None
            explodido = False
            particulas = []
        else:
            pygame.time.delay(1000)
            exibir_tela_final()

    # GUI
    tempo_fase_seg = (pygame.time.get_ticks() - tempo_inicio_fase) // 1000
    texto_gui = fonte_info.render(f"Nível: {nivel_atual}   Tempo: {tempo_fase_seg}s   Movimentos: {movimentos}/{movimentos_esperados}", True, (200, 200, 200))
    tela.blit(texto_gui, (10, 30))
    texto_info = fonte_info.render("LaserPy v1.0 – ArchaicBit", True, (200, 200, 200))
    tela.blit(texto_info, (10, 10))
    # botão de reiniciar
    cor_botao = (80, 80, 80)
    if botao_reiniciar.collidepoint(pygame.mouse.get_pos()):
        cor_botao = (100, 100, 100)
    
    pygame.draw.rect(tela, cor_botao, botao_reiniciar, border_radius=5)
    texto_reiniciar = fonte_info.render("Reiniciar Level", True, (255, 255, 255))
    tela.blit(texto_reiniciar, (botao_reiniciar.x + 10, botao_reiniciar.y + 5))
    
    pygame.display.flip()
    clock.tick(60)