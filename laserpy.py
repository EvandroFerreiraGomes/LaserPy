import pygame
import time
import random
import sys

pygame.init()

# Configurações gerais
fonte_info = pygame.font.SysFont("verdana", 11)
tamanho_bloco = 50
linhas_grid = 10
colunas_grid = 10
largura_tela = 600
altura_tela = 600
offset_x = tamanho_bloco
offset_y = tamanho_bloco

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("LaserPy 1.1")
logo_img = pygame.image.load("logo_laserpy.png")
logo_img = pygame.transform.scale(logo_img, (350, 260))

# Cores
COR_GRID = (60, 60, 60)
COR_FUNDO = (20, 20, 20)
COR_ESPELHO = (180, 180, 255)
COR_PAREDE = (100, 100, 100)
COR_HOVER = (40, 40, 40)
COR_LASERS = {
    "vermelho": (255, 0, 0),
    "azul": (0, 128, 255),
    "verde": (0, 255, 100)
}

# Direções e reflexões
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

# levels
levels = {
    1: {
        "lasers": [{"emissor": (1, 2), "destino": (8, 9), "direcao": "direita", "cor": "vermelho"}],
        "movimentos_esperados": 5,
        "espelhos": [
            {"linha": 4, "coluna": 3, "rotacao": 0},
            {"linha": 4, "coluna": 2, "rotacao": 0}
        ],
        "paredes": [(0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,2),(7,3),(7,5),(7,6),(7,7),(7,8),(7,9),(9,9)]
    },
    2: {
        "lasers": [{"emissor": (1, 1), "destino": (8, 8), "direcao": "baixo", "cor": "vermelho"}],
        "movimentos_esperados": 5,
        "espelhos": [
            {"linha": 1, "coluna": 4, "rotacao": 0},
            {"linha": 2, "coluna": 6, "rotacao": 1},
            {"linha": 6, "coluna": 8, "rotacao": 1}
        ],
        "paredes": [(2,0),(2,5),(3,6),(5,8),(6,2),(6,5),(7,4),(7,8),(8,3),(8,7),(9,3)]
    },
    3: {
        "lasers": [{"emissor": (4, 5), "destino": (9, 0), "direcao": "cima", "cor": "vermelho"}],
        "movimentos_esperados": 5,
        "espelhos": [
            {"linha": 1, "coluna": 3, "rotacao": 0},
            {"linha": 1, "coluna": 9, "rotacao": 1},
            {"linha": 4, "coluna": 7, "rotacao": 1},
            {"linha": 3, "coluna": 7, "rotacao": 0},
            {"linha": 4, "coluna": 0, "rotacao": 1},
            {"linha": 9, "coluna": 6, "rotacao": 1}
        ],
        "paredes": [(0,0),(1,2),(2,4),(2,6),(1,7),(3,9),(5,7),(3,2),(5,1),(6,2),(7,0),(9,2),(7,5),(8,6),(9,9),(9,4)]
    },
    4: {
        "lasers": [{"emissor": (5, 1), "destino": (9, 8), "direcao": "cima", "cor": "vermelho"}],
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
        "paredes": [(0,0),(0,2),(0,5),(2,7),(1,9),(4,8),(6,8),(8,8),(9,9),(8,7),(7,6),(5,5),(3,5),(3,4),(3,2),(4,0),(6,1),(5,3),(6,4),(7,3),(8,4),(9,3),(8,1),(2,6)]
    },
    5: {
        "lasers": [
            {"emissor": (1, 2), "destino": (8, 9), "direcao": "direita", "cor": "vermelho"},
            {"emissor": (2, 2), "destino": (7, 8), "direcao": "direita", "cor": "azul"},
            {"emissor": (3, 2), "destino": (6, 7), "direcao": "direita", "cor": "verde"},
        ],
        "movimentos_esperados": 6,
        "espelhos": [
            {"linha": 5, "coluna": 5, "rotacao": 0},
            {"linha": 4, "coluna": 4, "rotacao": 1},
            {"linha": 6, "coluna": 6, "rotacao": 0},
            {"linha": 6, "coluna": 7, "rotacao": 0},
            {"linha": 6, "coluna": 8, "rotacao": 0},
            {"linha": 6, "coluna": 9, "rotacao": 0}
        ],
        "paredes": [(0,9),(9,0),(5,7),(7,3)]
    }
}

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

def carregar_nivel(n):
    dados = levels[n]
    lasers = dados.get("lasers", [])
    return (
        lasers,
        [Espelho(e["linha"], e["coluna"], e["rotacao"]) for e in dados["espelhos"]],
        dados["paredes"],
        dados["movimentos_esperados"]
    )

def calcular_trajetoria_laser(laser, espelhos, paredes):
    segmentos = []
    linha, coluna = laser["emissor"]
    destino_pos = laser["destino"]
    direcao = laser["direcao"]
    dx, dy = direcoes[direcao]
    x_ini = offset_x + coluna * tamanho_bloco + tamanho_bloco // 2
    y_ini = offset_y + linha * tamanho_bloco + tamanho_bloco // 2

    atingiu_destino = False

    while 0 <= linha < linhas_grid and 0 <= coluna < colunas_grid:
        x_fim = x_ini + dx * tamanho_bloco
        y_fim = y_ini + dy * tamanho_bloco
        segmentos.append(((x_ini, y_ini), (x_fim, y_fim)))

        linha += dy
        coluna += dx
        x_ini = x_fim
        y_ini = y_fim

        if (linha, coluna) == destino_pos:
            atingiu_destino = True
            if not laser["explodiu"]:
                break  
        if (linha, coluna) in paredes:
            break

        for esp in espelhos:
            if (linha, coluna) == (esp.linha, esp.coluna):
                if direcao in reflexoes[esp.rotacao]:
                    direcao = reflexoes[esp.rotacao][direcao]
                    dx, dy = direcoes[direcao]
                else:
                    return segmentos, atingiu_destino

    return segmentos, atingiu_destino


def exibir_tela_inicial():
    fonte_titulo = pygame.font.SysFont("verdana", 40, bold=True)
    fonte_botao = pygame.font.SysFont("verdana", 18)
    fonte_rodape = pygame.font.SysFont("verdana", 12)

    botao_iniciar = pygame.Rect((largura_tela - 200) // 2, 360, 200, 40)
    botao_sair = pygame.Rect((largura_tela - 200) // 2, 420, 200, 40)

    aguardando = True
    while aguardando:
        tela.fill(COR_FUNDO)

        tela.blit(logo_img, ((largura_tela - logo_img.get_width()) // 2, 40))

        mouse_pos = pygame.mouse.get_pos()

        for botao, texto in [(botao_iniciar, "Iniciar Jogo"), (botao_sair, "Sair")]:
            cor = (100, 100, 100) if botao.collidepoint(mouse_pos) else (80, 80, 80)
            pygame.draw.rect(tela, cor, botao, border_radius=5)
            texto_render = fonte_botao.render(texto, True, (255, 255, 255))
            tela.blit(texto_render, (botao.x + (botao.width - texto_render.get_width()) // 2,
                                     botao.y + (botao.height - texto_render.get_height()) // 2))

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

# inicialização do jogo
exibir_tela_inicial()
nivel_atual = 1

lasers, espelhos, paredes, movimentos_esperados = carregar_nivel(nivel_atual)
movimentos = 0
arrastando = False
clock = pygame.time.Clock()
botao_reiniciar = pygame.Rect(largura_tela - 130, 10, 120, 25)
tempo_inicio_fase = pygame.time.get_ticks()

for laser in lasers:
    laser["atingiu"] = False
    laser["explodiu"] = False
    laser["tempo_atingiu"] = None

particulas = []
tempo_animacao_comum = None

# Loop principal INICIO
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

            if botao_reiniciar.collidepoint(evento.pos):
                lasers, espelhos, paredes, movimentos_esperados = carregar_nivel(nivel_atual)
                tempo_inicio_fase = pygame.time.get_ticks()
                movimentos = 0
                tempo_atingiu = None
                explodido = False
                particulas = []
                
                        
            for esp in espelhos:
                if (linha_mouse, coluna_mouse) == (esp.linha, esp.coluna):
                    if tempo_atual - esp.tempo_ultimo_clique < 0.3:
                        esp.girar()
                    else:
                        arrastando = esp
                    esp.tempo_ultimo_clique = tempo_atual
        elif evento.type == pygame.MOUSEBUTTONUP:
            if arrastando:
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

    laser_atingiu_todos = True
    
    for laser in lasers:
        segmentos, atingiu = calcular_trajetoria_laser(laser, espelhos, paredes)
        cor = COR_LASERS[laser["cor"]]
        linha_d, coluna_d = laser["destino"]
        x_d = offset_x + coluna_d * tamanho_bloco
        y_d = offset_y + linha_d * tamanho_bloco
        centro_d = (x_d + tamanho_bloco // 2, y_d + tamanho_bloco // 2)

        # Desenhar emissor
        linha, coluna = laser["emissor"]
        x = offset_x + coluna * tamanho_bloco
        y = offset_y + linha * tamanho_bloco
        if laser["direcao"] == "direita":
            pontos = [(x + 10, y + 10), (x + 10, y + 40), (x + 40, y + 25)]
        elif laser["direcao"] == "esquerda":
            pontos = [(x + 40, y + 10), (x + 40, y + 40), (x + 10, y + 25)]
        elif laser["direcao"] == "cima":
            pontos = [(x + 10, y + 40), (x + 40, y + 40), (x + 25, y + 10)]
        elif laser["direcao"] == "baixo":
            pontos = [(x + 10, y + 10), (x + 40, y + 10), (x + 25, y + 40)]
        pygame.draw.polygon(tela, cor, pontos)

        # animação do laser
        for seg in segmentos:
            for i in range(0, 100, 20):
                t = (pygame.time.get_ticks() // 5 + i) % 100 / 100
                x_fluxo = seg[0][0] + (seg[1][0] - seg[0][0]) * t
                y_fluxo = seg[0][1] + (seg[1][1] - seg[0][1]) * t
                pygame.draw.circle(tela, cor, (int(x_fluxo), int(y_fluxo)), 2)
            pygame.draw.line(tela, cor, seg[0], seg[1], 2)
    
            linha_d, coluna_d = laser["destino"]
            x_d = offset_x + coluna_d * tamanho_bloco
            y_d = offset_y + linha_d * tamanho_bloco
            centro_d = (x_d + tamanho_bloco // 2, y_d + tamanho_bloco // 2)
    
        if atingiu:
            if not laser["atingiu"]:
                laser["atingiu"] = True
                laser["tempo_atingiu"] = pygame.time.get_ticks()
        else:
            laser["atingiu"] = False
            laser_atingiu_todos = False
            
        if not laser["explodiu"]:
            pygame.draw.circle(tela, cor, centro_d, 10, 2)
    
        if not laser["atingiu"]:
            laser_atingiu_todos = False
    
        for esp in espelhos:
            esp.desenhar(tela)
    
        for parede in paredes:
            px = offset_x + parede[1] * tamanho_bloco
            py = offset_y + parede[0] * tamanho_bloco
            pygame.draw.rect(tela, COR_PAREDE, (px, py, tamanho_bloco, tamanho_bloco))


    if laser_atingiu_todos:
        if tempo_animacao_comum is None:
            tempo_animacao_comum = pygame.time.get_ticks()
    
        tempo_passado = (pygame.time.get_ticks() - tempo_animacao_comum) / 1000
    
        for laser in lasers:
            linha_d, coluna_d = laser["destino"]
            x_d = offset_x + coluna_d * tamanho_bloco
            y_d = offset_y + linha_d * tamanho_bloco
            centro_d = (x_d + tamanho_bloco // 2, y_d + tamanho_bloco // 2)
            cor = COR_LASERS[laser["cor"]]
    
            if tempo_passado < 2:
                raio = int(10 + tempo_passado * 2)
                pygame.draw.circle(tela, cor, centro_d, raio)
                pygame.draw.circle(tela, (255, 255, 255), centro_d, raio, 2)
            elif not laser["explodiu"]:
                laser["explodiu"] = True
                for _ in range(50):
                    particulas.append({
                        "x": centro_d[0],
                        "y": centro_d[1],
                        "vx": (2 - 4 * random.random()),
                        "vy": (2 - 4 * random.random()),
                        "tempo": pygame.time.get_ticks(),
                        "cor": cor
                    })

    # GUI
    tempo_fase_seg = (pygame.time.get_ticks() - tempo_inicio_fase) // 1000
    texto_gui = fonte_info.render(f"Nível: {nivel_atual}   Tempo: {tempo_fase_seg}s   Movimentos: {movimentos}/{movimentos_esperados}", True, (200, 200, 200))
    tela.blit(texto_gui, (10, 30))
    
    texto_info = fonte_info.render("LaserPy v1.1 – ArchaicBit", True, (200, 200, 200))
    tela.blit(texto_info, (10, 10))
    
    # botão de reiniciar
    cor_botao = (80, 80, 80)
    if botao_reiniciar.collidepoint(pygame.mouse.get_pos()):
        cor_botao = (100, 100, 100)
    
    pygame.draw.rect(tela, cor_botao, botao_reiniciar, border_radius=5)
    texto_reiniciar = fonte_info.render("Reiniciar Level", True, (255, 255, 255))
    tela.blit(texto_reiniciar, (botao_reiniciar.x + 10, botao_reiniciar.y + 5))

    # Animação das partículas (explosão)
    novas_particulas = []
    for p in particulas:
        t = (pygame.time.get_ticks() - p["tempo"]) / 1000
        if t < 2:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            pygame.draw.circle(tela, p["cor"], (int(p["x"]), int(p["y"])), 3)
            novas_particulas.append(p)
    particulas = novas_particulas

    tempo_agora = pygame.time.get_ticks()
    tempo_desde_animacao = (pygame.time.get_ticks() - tempo_animacao_comum) / 1000 if tempo_animacao_comum else 0

    # verifica se todos os lasers atingiram e tempo da animação terminou
    if laser_atingiu_todos and not particulas and tempo_desde_animacao >= 5:
        nivel_atual += 1
        if nivel_atual in levels:
            lasers, espelhos, paredes, movimentos_esperados = carregar_nivel(nivel_atual)
            for laser in lasers:
                laser["atingiu"] = False
                laser["explodiu"] = False
                laser["tempo_atingiu"] = None
            movimentos = 0
            tempo_inicio_fase = pygame.time.get_ticks()
            particulas = []
            tempo_animacao_comum = None
        else:
            pygame.time.delay(1000)
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
# Loop principal FIM
