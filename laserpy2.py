import pygame
import time
import random
import sys
import math

try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
except Exception:
    pass
pygame.init()
SOM_ATIVO = pygame.mixer.get_init() is not None

tamanho_bloco = 50
linhas_grid = 10
colunas_grid = 10
largura_tela = 600
altura_tela = 660
offset_x = 50
offset_y = 60

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("LaserPy 2.0")

fonte_info = pygame.font.SysFont("verdana", 13)
fonte_info_b = pygame.font.SysFont("verdana", 14, bold=True)
fonte_popup = pygame.font.SysFont("verdana", 20)
fonte_popup_grande = pygame.font.SysFont("verdana", 28, bold=True)
fonte_botao = pygame.font.SysFont("verdana", 16)

COR_GRID = (44, 44, 58)
COR_FUNDO = (12, 12, 18)
COR_PAREDE = (96, 100, 112)
COR_HOVER = (38, 40, 56)
COR_TEXTO = (225, 228, 240)
COR_LASERS = {
    "vermelho": (255, 60, 60),
    "azul": (60, 150, 255),
    "verde": (70, 230, 120)
}
COR_ESPELHOS = {
    "verde": (114, 203, 38),
    "vermelho": (255, 90, 90),
    "cinza": (130, 130, 145)
}

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

levels = {
    1: {
        "lasers": [{"emissor": (1, 2), "destino": (8, 9), "direcao": "direita", "cor": "vermelho"}],
        "movimentos_esperados": 3,
        "espelhos": [
            {"linha": 4, "coluna": 3, "rotacao": 0, "cor": "vermelho"},
            {"linha": 4, "coluna": 2, "rotacao": 0, "cor": "verde"},
            {"linha": 4, "coluna": 4, "rotacao": 0, "cor": "cinza"},
            {"linha": 8, "coluna": 1, "rotacao": 1, "cor": "cinza"}
        ],
        "paredes": [(0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,2),(7,3),(7,5),(7,6),(7,7),(7,8),(7,9),(9,9)]
    },
    2: {
        "lasers": [{"emissor": (1, 1), "destino": (8, 8), "direcao": "baixo", "cor": "vermelho"}],
        "movimentos_esperados": 3,
        "espelhos": [
            {"linha": 1, "coluna": 4, "rotacao": 0, "cor": "vermelho"},
            {"linha": 2, "coluna": 6, "rotacao": 1, "cor": "vermelho"},
            {"linha": 6, "coluna": 8, "rotacao": 1, "cor": "vermelho"}
        ],
        "paredes": [(2,0),(2,5),(3,6),(5,8),(6,2),(6,5),(7,4),(7,8),(8,3),(8,7),(9,3)]
    },
    3: {
        "lasers": [{"emissor": (4, 5), "destino": (9, 0), "direcao": "cima", "cor": "vermelho"}],
        "movimentos_esperados": 6,
        "espelhos": [
            {"linha": 8, "coluna": 0, "rotacao": 0, "cor": "verde"},
            {"linha": 6, "coluna": 8, "rotacao": 0, "cor": "cinza"},
            {"linha": 4, "coluna": 7, "rotacao": 0, "cor": "vermelho"},
            {"linha": 3, "coluna": 7, "rotacao": 0, "cor": "vermelho"},
            {"linha": 4, "coluna": 0, "rotacao": 0, "cor": "vermelho"},
            {"linha": 9, "coluna": 6, "rotacao": 0, "cor": "vermelho"}
        ],
        "paredes": [(0,0),(1,2),(2,4),(2,6),(1,7),(3,9),(5,7),(3,2),(5,1),(6,2),(7,0),(9,2),(7,5),(8,6),(9,9),(9,4)]
    },
    4: {
        "lasers": [{"emissor": (5, 1), "destino": (9, 8), "direcao": "cima", "cor": "vermelho"}],
        "movimentos_esperados": 7,
        "espelhos": [
            {"linha": 2, "coluna": 3, "rotacao": 0, "cor": "vermelho"},
            {"linha": 4, "coluna": 2, "rotacao": 0, "cor": "vermelho"},
            {"linha": 7, "coluna": 2, "rotacao": 0, "cor": "vermelho"},
            {"linha": 6, "coluna": 0, "rotacao": 1, "cor": "vermelho"},
            {"linha": 2, "coluna": 0, "rotacao": 0, "cor": "vermelho"},
            {"linha": 3, "coluna": 0, "rotacao": 1, "cor": "vermelho"},
            {"linha": 9, "coluna": 0, "rotacao": 0, "cor": "vermelho"}
        ],
        "paredes": [(0,0),(0,2),(0,5),(2,7),(1,9),(4,8),(6,8),(8,8),(9,9),(8,7),(7,6),(5,5),(3,5),(3,4),(3,2),(4,0),(6,1),(5,3),(6,4),(7,3),(8,4),(9,3),(8,1),(2,6)]
    },
    5: {
        "lasers": [
            {"emissor": (2, 2), "destino": (8, 5), "direcao": "direita", "cor": "vermelho"},
            {"emissor": (1, 5), "destino": (8, 3), "direcao": "baixo", "cor": "azul"}
        ],
        "movimentos_esperados": 4,
        "espelhos": [
            {"linha": 0, "coluna": 9, "rotacao": 0, "cor": "vermelho"},
            {"linha": 5, "coluna": 4, "rotacao": 1, "cor": "vermelho"},
            {"linha": 0, "coluna": 2, "rotacao": 0, "cor": "vermelho"},
            {"linha": 8, "coluna": 2, "rotacao": 0, "cor": "vermelho"},
            {"linha": 9, "coluna": 7, "rotacao": 0, "cor": "vermelho"}
        ],
        "paredes": [(3,7),(3,4),(4,2),(6,4),(8,2),(8,6)]
    },
    6: {
        "lasers": [
            {"emissor": (1, 2), "destino": (5, 8), "direcao": "direita", "cor": "vermelho"},
            {"emissor": (3, 2), "destino": (1, 8), "direcao": "direita", "cor": "azul"},
            {"emissor": (5, 2), "destino": (3, 8), "direcao": "direita", "cor": "verde"}
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
        "paredes": [(0,0)]
    },
    7: {
        "lasers": [{"emissor": (0, 1), "destino": (0, 8), "direcao": "baixo", "cor": "vermelho"}],
        "movimentos_esperados": 2,
        "tempo_limite": 40,
        "espelhos": [
            {"linha": 3, "coluna": 4, "rotacao": 0, "cor": "verde"},
            {"linha": 7, "coluna": 6, "rotacao": 1, "cor": "verde"}
        ],
        "paredes": [(2,3),(3,6),(7,2),(8,7),(2,6)]
    },
    8: {
        "lasers": [
            {"emissor": (0, 0), "destino": (9, 4), "direcao": "direita", "cor": "vermelho"},
            {"emissor": (3, 9), "destino": (9, 5), "direcao": "esquerda", "cor": "azul"}
        ],
        "movimentos_esperados": 2,
        "tempo_limite": 50,
        "espelhos": [
            {"linha": 5, "coluna": 2, "rotacao": 0, "cor": "verde"},
            {"linha": 6, "coluna": 7, "rotacao": 1, "cor": "verde"}
        ],
        "paredes": [(1,2),(2,7),(5,8),(7,2),(8,7),(6,3)]
    },
    9: {
        "lasers": [
            {"emissor": (0, 0), "destino": (4, 3), "direcao": "direita", "cor": "vermelho"},
            {"emissor": (0, 9), "destino": (5, 6), "direcao": "baixo", "cor": "azul"},
            {"emissor": (9, 0), "destino": (8, 8), "direcao": "cima", "cor": "verde"}
        ],
        "movimentos_esperados": 4,
        "tempo_limite": 60,
        "espelhos": [
            {"linha": 2, "coluna": 5, "rotacao": 0, "cor": "verde"},
            {"linha": 3, "coluna": 7, "rotacao": 1, "cor": "verde"},
            {"linha": 6, "coluna": 2, "rotacao": 0, "cor": "verde"},
            {"linha": 8, "coluna": 5, "rotacao": 1, "cor": "verde"}
        ],
        "paredes": [(1,1),(2,6),(3,5),(4,7),(6,4),(8,3),(2,1),(6,8)]
    }
}


def carregar_imagem(caminho, tamanho=None):
    try:
        img = pygame.image.load(caminho)
        if tamanho:
            img = pygame.transform.scale(img, tamanho)
        return img.convert_alpha()
    except Exception:
        return None


logo_img = carregar_imagem("logo_laserpy.png", (350, 260))
estrela_cheia = carregar_imagem("estrela.png", (40, 40))
estrela_vazia = carregar_imagem("sem_estrela.png", (40, 40))


def gerar_som(frequencias, dur, volume=0.3, decaimento=True):
    if not SOM_ATIVO:
        return None
    try:
        import numpy as np
        sr = 44100
        n = max(1, int(sr * dur))
        t = np.linspace(0, dur, n, False)
        if isinstance(frequencias, (int, float)):
            frequencias = [frequencias]
        onda = np.zeros(n)
        for f in frequencias:
            onda += np.sin(2 * np.pi * f * t)
        onda /= len(frequencias)
        env = np.linspace(1, 0, n) ** 2 if decaimento else np.ones(n)
        onda = onda * env * volume
        audio = np.int16(onda * 32767)
        estereo = np.ascontiguousarray(np.column_stack((audio, audio)))
        return pygame.sndarray.make_sound(estereo)
    except Exception:
        return None


som_mover = gerar_som([330], 0.07, 0.25)
som_girar = gerar_som([520, 700], 0.06, 0.20)
som_vitoria = gerar_som([523, 659, 784], 0.5, 0.30)
som_explosao = gerar_som([120, 70], 0.4, 0.35)
som_erro = gerar_som([180, 110], 0.35, 0.30)
som_clique = gerar_som([600], 0.05, 0.20)


def tocar(som):
    if som is not None:
        try:
            som.play()
        except Exception:
            pass


def criar_fundo():
    s = pygame.Surface((largura_tela, altura_tela))
    topo = (20, 20, 32)
    base = (8, 8, 14)
    for y in range(altura_tela):
        k = y / altura_tela
        c = (int(topo[0] + (base[0] - topo[0]) * k),
             int(topo[1] + (base[1] - topo[1]) * k),
             int(topo[2] + (base[2] - topo[2]) * k))
        pygame.draw.line(s, c, (0, y), (largura_tela, y))
    return s


fundo_surf = criar_fundo()


def circulo_alpha(superficie, cor, pos, raio, alpha):
    raio = int(raio)
    if raio < 1:
        return
    s = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (cor[0], cor[1], cor[2], alpha), (raio, raio), raio)
    superficie.blit(s, (int(pos[0]) - raio, int(pos[1]) - raio))


def desenhar_estrela(superficie, centro, raio, cor, preenchida=True):
    pontos = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = raio if i % 2 == 0 else raio * 0.45
        pontos.append((centro[0] + math.cos(ang) * r, centro[1] + math.sin(ang) * r))
    if preenchida:
        pygame.draw.polygon(superficie, cor, pontos)
        pygame.draw.polygon(superficie, (255, 255, 255), pontos, 2)
    else:
        pygame.draw.polygon(superficie, (70, 70, 84), pontos)
        pygame.draw.polygon(superficie, (110, 110, 124), pontos, 2)


def desenhar_botao(superficie, rect, texto, fonte, hover, destaque=False):
    if destaque:
        base = (66, 120, 92) if hover else (50, 96, 74)
        borda = (120, 220, 150)
    else:
        base = (66, 66, 88) if hover else (48, 48, 64)
        borda = (118, 118, 150)
    pygame.draw.rect(superficie, base, rect, border_radius=8)
    pygame.draw.rect(superficie, borda, rect, 2, border_radius=8)
    r = fonte.render(texto, True, COR_TEXTO)
    superficie.blit(r, (rect.centerx - r.get_width() // 2, rect.centery - r.get_height() // 2))


class Espelho:
    def __init__(self, linha, coluna, rotacao=0, cor="verde"):
        self.linha = linha
        self.coluna = coluna
        self.rotacao = rotacao
        self.tempo_ultimo_clique = 0
        self.cor = cor

    def desenhar(self, superficie, hover=False):
        x = offset_x + self.coluna * tamanho_bloco
        y = offset_y + self.linha * tamanho_bloco
        if self.rotacao == 0:
            p1 = (x + 10, y + 40)
            p2 = (x + 40, y + 10)
        else:
            p1 = (x + 10, y + 10)
            p2 = (x + 40, y + 40)
        cor = COR_ESPELHOS.get(self.cor, COR_ESPELHOS["verde"])
        if hover and self.cor != "cinza":
            pygame.draw.rect(superficie, (cor[0], cor[1], cor[2], 40),
                             (x + 4, y + 4, tamanho_bloco - 8, tamanho_bloco - 8), border_radius=6)
        meio = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
        circulo_alpha(superficie, cor, meio, 16, 45)
        pygame.draw.line(superficie, (20, 20, 26), p1, p2, 7)
        pygame.draw.line(superficie, cor, p1, p2, 4)
        pygame.draw.line(superficie, (255, 255, 255), p1, p2, 1)
        if self.cor == "cinza":
            pygame.draw.circle(superficie, (200, 200, 210), meio, 3)

    def mover_para(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna

    def girar(self):
        self.rotacao = (self.rotacao + 1) % 2


def carregar_nivel(n):
    dados = levels[n]
    lasers = [dict(l) for l in dados.get("lasers", [])]
    espelhos = [Espelho(e["linha"], e["coluna"], e["rotacao"], e.get("cor", "verde")) for e in dados["espelhos"]]
    paredes = list(dados["paredes"])
    return lasers, espelhos, paredes, dados["movimentos_esperados"], dados.get("tempo_limite", 30)


def preparar_nivel(n):
    lasers, espelhos, paredes, mov_esp, tlim = carregar_nivel(n)
    for laser in lasers:
        laser["atingiu"] = False
        laser["explodiu"] = False
        laser["tempo_atingiu"] = None
    return lasers, espelhos, paredes, mov_esp, tlim


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


def criar_explosao(centro, cor, n=60):
    parts = []
    agora = pygame.time.get_ticks()
    for _ in range(n):
        ang = random.uniform(0, 2 * math.pi)
        vel = random.uniform(1.0, 5.5)
        branca = random.random() < 0.25
        parts.append({
            "x": centro[0], "y": centro[1],
            "vx": math.cos(ang) * vel, "vy": math.sin(ang) * vel,
            "tempo": agora, "cor": (255, 255, 255) if branca else cor,
            "raio": random.uniform(2, 5), "vida": random.uniform(0.6, 1.4)
        })
    return parts


def desenhar_emissor(superficie, laser):
    linha, coluna = laser["emissor"]
    x = offset_x + coluna * tamanho_bloco
    y = offset_y + linha * tamanho_bloco
    cor = COR_LASERS[laser["cor"]]
    circulo_alpha(superficie, cor, (x + 25, y + 25), 22, 50)
    pygame.draw.rect(superficie, (30, 30, 40), (x + 6, y + 6, 38, 38), border_radius=8)
    pygame.draw.rect(superficie, cor, (x + 6, y + 6, 38, 38), 2, border_radius=8)
    d = laser["direcao"]
    if d == "direita":
        pontos = [(x + 14, y + 14), (x + 14, y + 36), (x + 40, y + 25)]
    elif d == "esquerda":
        pontos = [(x + 36, y + 14), (x + 36, y + 36), (x + 10, y + 25)]
    elif d == "cima":
        pontos = [(x + 14, y + 36), (x + 36, y + 36), (x + 25, y + 10)]
    else:
        pontos = [(x + 14, y + 14), (x + 36, y + 14), (x + 25, y + 40)]
    pygame.draw.polygon(superficie, cor, pontos)


def desenhar_destino(superficie, laser, atingiu, t):
    linha_d, coluna_d = laser["destino"]
    cx = offset_x + coluna_d * tamanho_bloco + tamanho_bloco // 2
    cy = offset_y + linha_d * tamanho_bloco + tamanho_bloco // 2
    cor = COR_LASERS[laser["cor"]]
    if laser["explodiu"]:
        return
    pulso = (math.sin(t * 0.005) + 1) / 2
    if atingiu:
        circulo_alpha(superficie, cor, (cx, cy), 18 + pulso * 6, 90)
        pygame.draw.circle(superficie, cor, (cx, cy), 11)
        pygame.draw.circle(superficie, (255, 255, 255), (cx, cy), 11, 2)
    else:
        circulo_alpha(superficie, cor, (cx, cy), 14 + pulso * 5, 50)
        pygame.draw.circle(superficie, cor, (cx, cy), int(10 + pulso * 2), 2)
        pygame.draw.circle(superficie, (255, 255, 255), (cx, cy), 3)


def desenhar_beam(superficie, segmentos, cor, tempo_ms):
    clara = tuple(min(255, c + 90) for c in cor)
    for seg in segmentos:
        pygame.draw.line(superficie, (cor[0], cor[1], cor[2], 35), seg[0], seg[1], 9)
        pygame.draw.line(superficie, (cor[0], cor[1], cor[2], 110), seg[0], seg[1], 4)
        pygame.draw.line(superficie, (clara[0], clara[1], clara[2], 235), seg[0], seg[1], 2)
        for i in range(0, 100, 18):
            tt = ((tempo_ms // 4 + i) % 100) / 100
            x = seg[0][0] + (seg[1][0] - seg[0][0]) * tt
            y = seg[0][1] + (seg[1][1] - seg[0][1]) * tt
            circulo_alpha(superficie, (255, 255, 255), (x, y), 3, 200)


def tela_inicial():
    bw = 240
    bx = (largura_tela - bw) // 2
    botao_iniciar = pygame.Rect(bx, 400, bw, 46)
    botao_fases = pygame.Rect(bx, 458, bw, 46)
    botao_sair = pygame.Rect(bx, 516, bw, 46)
    fonte_titulo = pygame.font.SysFont("verdana", 46, bold=True)
    fonte_sub = pygame.font.SysFont("verdana", 14)
    fonte_rodape = pygame.font.SysFont("verdana", 11)
    feixes = [{"x": random.randint(0, largura_tela), "y": random.randint(0, altura_tela),
               "v": random.uniform(0.6, 1.8), "cor": random.choice(list(COR_LASERS.values()))}
              for _ in range(36)]
    clock = pygame.time.Clock()

    while True:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(fundo_surf, (0, 0))

        for f in feixes:
            f["y"] += f["v"]
            if f["y"] > altura_tela:
                f["y"] = -10
                f["x"] = random.randint(0, largura_tela)
            circulo_alpha(tela, f["cor"], (f["x"], f["y"]), 2, 120)

        if logo_img:
            tela.blit(logo_img, ((largura_tela - logo_img.get_width()) // 2, 50))
        else:
            pulso = (math.sin(now * 0.003) + 1) / 2
            cor_t = (int(120 + pulso * 135), int(60 + pulso * 60), int(60 + pulso * 40))
            titulo = fonte_titulo.render("LaserPy", True, cor_t)
            tela.blit(titulo, ((largura_tela - titulo.get_width()) // 2, 120))
            pygame.draw.line(tela, COR_LASERS["vermelho"],
                             (largura_tela // 2 - 120, 200), (largura_tela // 2 + 120, 200), 3)
        sub = fonte_sub.render("Puzzle de espelhos e lasers", True, (160, 160, 180))
        tela.blit(sub, ((largura_tela - sub.get_width()) // 2, 320))

        botoes = [(botao_iniciar, "Iniciar jogo", True),
                  (botao_fases, "Selecionar fase", False),
                  (botao_sair, "Sair", False)]
        for rect, txt, dest in botoes:
            desenhar_botao(tela, rect, txt, fonte_botao, rect.collidepoint(mouse_pos), dest)

        r1 = fonte_rodape.render("Evandro Ferreira", True, (150, 150, 165))
        r2 = fonte_rodape.render("ArchaicBit 2025", True, (150, 150, 165))
        tela.blit(r1, ((largura_tela - r1.get_width()) // 2, altura_tela - 50))
        tela.blit(r2, ((largura_tela - r2.get_width()) // 2, altura_tela - 30))

        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    tocar(som_clique)
                    return "iniciar"
                elif botao_fases.collidepoint(evento.pos):
                    tocar(som_clique)
                    return "selecionar"
                elif botao_sair.collidepoint(evento.pos):
                    return "sair"


def selecionar_fase():
    fonte_titulo = pygame.font.SysFont("verdana", 30, bold=True)
    fonte_num = pygame.font.SysFont("verdana", 28, bold=True)
    cols = 3
    cel = 130
    esp = 24
    total_w = cols * cel + (cols - 1) * esp
    inicio_x = (largura_tela - total_w) // 2
    inicio_y = 140
    rects = {}
    niveis = sorted(levels.keys())
    for idx, n in enumerate(niveis):
        linha = idx // cols
        coluna = idx % cols
        x = inicio_x + coluna * (cel + esp)
        y = inicio_y + linha * (cel + esp)
        rects[n] = pygame.Rect(x, y, cel, cel)
    botao_voltar = pygame.Rect((largura_tela - 200) // 2, altura_tela - 70, 200, 42)
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(fundo_surf, (0, 0))
        titulo = fonte_titulo.render("Selecionar fase", True, COR_TEXTO)
        tela.blit(titulo, ((largura_tela - titulo.get_width()) // 2, 70))

        for n, rect in rects.items():
            hover = rect.collidepoint(mouse_pos)
            base = (60, 60, 84) if hover else (42, 42, 58)
            pygame.draw.rect(tela, base, rect, border_radius=12)
            pygame.draw.rect(tela, (120, 120, 155), rect, 2, border_radius=12)
            num = fonte_num.render(str(n), True, COR_TEXTO)
            tela.blit(num, (rect.centerx - num.get_width() // 2, rect.centery - num.get_height() // 2))

        desenhar_botao(tela, botao_voltar, "Voltar", fonte_botao, botao_voltar.collidepoint(mouse_pos))
        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(evento.pos):
                    tocar(som_clique)
                    return None
                for n, rect in rects.items():
                    if rect.collidepoint(evento.pos):
                        tocar(som_clique)
                        return n


def tela_vitoria():
    fonte_t = pygame.font.SysFont("verdana", 40, bold=True)
    fonte_s = pygame.font.SysFont("verdana", 18)
    botao_ok = pygame.Rect((largura_tela - 220) // 2, 440, 220, 46)
    particulas = []
    clock = pygame.time.Clock()
    tocar(som_vitoria)
    inicio = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(fundo_surf, (0, 0))

        if now - inicio < 4000 and random.random() < 0.3:
            centro = (random.randint(100, largura_tela - 100), random.randint(120, 360))
            particulas += criar_explosao(centro, random.choice(list(COR_LASERS.values())), 25)

        novas = []
        for p in particulas:
            t = (now - p["tempo"]) / 1000
            if t < p["vida"]:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.05
                a = int(255 * (1 - t / p["vida"]))
                r = max(1, p["raio"] * (1 - t / p["vida"]))
                circulo_alpha(tela, p["cor"], (p["x"], p["y"]), r, a)
                novas.append(p)
        particulas = novas

        titulo = fonte_t.render("Voce venceu!", True, (255, 215, 90))
        tela.blit(titulo, ((largura_tela - titulo.get_width()) // 2, 180))
        sub = fonte_s.render("Todas as fases concluidas", True, COR_TEXTO)
        tela.blit(sub, ((largura_tela - sub.get_width()) // 2, 250))
        for i in range(3):
            desenhar_estrela(tela, (largura_tela // 2 - 70 + i * 70, 340), 26, (255, 215, 90), True)

        desenhar_botao(tela, botao_ok, "Voltar ao menu", fonte_botao, botao_ok.collidepoint(mouse_pos), True)
        pygame.display.flip()
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.MOUSEBUTTONDOWN and botao_ok.collidepoint(evento.pos):
                tocar(som_clique)
                return "menu"


def jogar(nivel_inicial):
    clock = pygame.time.Clock()
    nivel_atual = nivel_inicial

    botao_reiniciar = pygame.Rect(30, altura_tela - 52, 165, 36)
    botao_desfazer = pygame.Rect(216, altura_tela - 52, 165, 36)
    botao_menu = pygame.Rect(402, altura_tela - 52, 165, 36)
    popup_botao = pygame.Rect((largura_tela - 130) // 2, altura_tela // 2 + 10, 130, 36)
    popup_botao_proximo = pygame.Rect(0, 0, 150, 36)

    def estado_atual(esp, mov):
        return ([(e.linha, e.coluna, e.rotacao) for e in esp], mov)

    lasers, espelhos, paredes, mov_esperados, tempo_limite = preparar_nivel(nivel_atual)
    movimentos = 0
    arrastando = False
    historico = []
    particulas = []
    tempo_inicio_fase = pygame.time.get_ticks()
    tempo_animacao_comum = None
    tempo_restante_congelado = None
    popup_ativa = False
    popup_fase_concluida = False
    tocou_erro = False
    tocou_vitoria = False
    shake_inicio = 0

    def resetar_nivel():
        nonlocal lasers, espelhos, paredes, mov_esperados, tempo_limite
        nonlocal movimentos, historico, particulas, tempo_inicio_fase
        nonlocal tempo_animacao_comum, tempo_restante_congelado
        nonlocal popup_ativa, popup_fase_concluida, tocou_erro, tocou_vitoria, shake_inicio
        lasers, espelhos, paredes, mov_esperados, tempo_limite = preparar_nivel(nivel_atual)
        movimentos = 0
        historico = []
        particulas = []
        tempo_inicio_fase = pygame.time.get_ticks()
        tempo_animacao_comum = None
        tempo_restante_congelado = None
        popup_ativa = False
        popup_fase_concluida = False
        tocou_erro = False
        tocou_vitoria = False
        shake_inicio = 0

    superficie_jogo = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)

    while True:
        now = pygame.time.get_ticks()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        coluna_mouse = (mouse_x - offset_x) // tamanho_bloco
        linha_mouse = (mouse_y - offset_y) // tamanho_bloco

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if popup_fase_concluida:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if popup_botao.collidepoint(evento.pos):
                        tocar(som_clique)
                        resetar_nivel()
                    elif popup_botao_proximo.collidepoint(evento.pos):
                        tocar(som_clique)
                        if nivel_atual + 1 in levels:
                            nivel_atual += 1
                            resetar_nivel()
                        else:
                            return "vitoria"
                continue

            if popup_ativa:
                if evento.type == pygame.MOUSEBUTTONDOWN and popup_botao.collidepoint(evento.pos):
                    tocar(som_clique)
                    resetar_nivel()
                continue

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_z and historico:
                    estados, mov = historico.pop()
                    for esp, (l, c, r) in zip(espelhos, estados):
                        esp.linha, esp.coluna, esp.rotacao = l, c, r
                    movimentos = mov
                    particulas = []
                    tempo_animacao_comum = None
                    tempo_restante_congelado = None
                    for laser in lasers:
                        laser["atingiu"] = False
                        laser["explodiu"] = False
                        laser["tempo_atingiu"] = None
                    tocar(som_girar)
                elif evento.key == pygame.K_r:
                    resetar_nivel()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_reiniciar.collidepoint(evento.pos):
                    tocar(som_clique)
                    resetar_nivel()
                    continue
                if botao_desfazer.collidepoint(evento.pos):
                    if historico:
                        estados, mov = historico.pop()
                        for esp, (l, c, r) in zip(espelhos, estados):
                            esp.linha, esp.coluna, esp.rotacao = l, c, r
                        movimentos = mov
                        particulas = []
                        tempo_animacao_comum = None
                        tempo_restante_congelado = None
                        for laser in lasers:
                            laser["atingiu"] = False
                            laser["explodiu"] = False
                            laser["tempo_atingiu"] = None
                        tocar(som_girar)
                    continue
                if botao_menu.collidepoint(evento.pos):
                    tocar(som_clique)
                    return "menu"

                tempo_atual = time.time()
                for esp in espelhos:
                    if (linha_mouse, coluna_mouse) == (esp.linha, esp.coluna):
                        if esp.cor == "cinza":
                            break
                        elif esp.cor == "vermelho":
                            if tempo_atual - esp.tempo_ultimo_clique >= 0.3:
                                historico.append(estado_atual(espelhos, movimentos))
                                arrastando = esp
                        else:
                            if tempo_atual - esp.tempo_ultimo_clique < 0.3:
                                historico.append(estado_atual(espelhos, movimentos))
                                esp.girar()
                                tocar(som_girar)
                            else:
                                historico.append(estado_atual(espelhos, movimentos))
                                arrastando = esp
                        esp.tempo_ultimo_clique = tempo_atual
                        break

            elif evento.type == pygame.MOUSEBUTTONUP:
                if arrastando:
                    if 0 <= linha_mouse < linhas_grid and 0 <= coluna_mouse < colunas_grid:
                        arrastando.mover_para(linha_mouse, coluna_mouse)
                        movimentos += 1
                        tocar(som_mover)
                    elif historico:
                        historico.pop()
                    arrastando = False

        superficie_jogo.fill((0, 0, 0, 0))

        for linha in range(linhas_grid):
            for coluna in range(colunas_grid):
                x = offset_x + coluna * tamanho_bloco
                y = offset_y + linha * tamanho_bloco
                pygame.draw.rect(superficie_jogo, COR_GRID, (x, y, tamanho_bloco, tamanho_bloco), 1)

        if 0 <= linha_mouse < linhas_grid and 0 <= coluna_mouse < colunas_grid:
            x_h = offset_x + coluna_mouse * tamanho_bloco
            y_h = offset_y + linha_mouse * tamanho_bloco
            pygame.draw.rect(superficie_jogo, COR_HOVER, (x_h, y_h, tamanho_bloco, tamanho_bloco))

        for parede in paredes:
            px = offset_x + parede[1] * tamanho_bloco
            py = offset_y + parede[0] * tamanho_bloco
            pygame.draw.rect(superficie_jogo, COR_PAREDE, (px + 2, py + 2, tamanho_bloco - 4, tamanho_bloco - 4), border_radius=4)
            pygame.draw.rect(superficie_jogo, (60, 62, 72), (px + 2, py + 2, tamanho_bloco - 4, tamanho_bloco - 4), 2, border_radius=4)

        laser_atingiu_todos = True
        beam_surface = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)

        for laser in lasers:
            segmentos, atingiu = calcular_trajetoria_laser(laser, espelhos, paredes)
            cor = COR_LASERS[laser["cor"]]
            desenhar_emissor(superficie_jogo, laser)
            desenhar_beam(beam_surface, segmentos, cor, now)

            if atingiu:
                if not laser["atingiu"]:
                    laser["atingiu"] = True
                    laser["tempo_atingiu"] = now
            else:
                laser["atingiu"] = False
                laser_atingiu_todos = False

            desenhar_destino(superficie_jogo, laser, atingiu, now)

        superficie_jogo.blit(beam_surface, (0, 0))

        for esp in espelhos:
            hover = (linha_mouse, coluna_mouse) == (esp.linha, esp.coluna)
            esp.desenhar(superficie_jogo, hover)

        if laser_atingiu_todos:
            if tempo_animacao_comum is None:
                tempo_animacao_comum = now
            tempo_passado = (now - tempo_animacao_comum) / 500
            for laser in lasers:
                linha_d, coluna_d = laser["destino"]
                cx = offset_x + coluna_d * tamanho_bloco + tamanho_bloco // 2
                cy = offset_y + linha_d * tamanho_bloco + tamanho_bloco // 2
                cor = COR_LASERS[laser["cor"]]
                if tempo_passado < 2:
                    raio = int(11 + tempo_passado * 4)
                    circulo_alpha(superficie_jogo, cor, (cx, cy), raio + 8, 120)
                    pygame.draw.circle(superficie_jogo, cor, (cx, cy), raio)
                    pygame.draw.circle(superficie_jogo, (255, 255, 255), (cx, cy), raio, 2)
                elif not laser["explodiu"]:
                    laser["explodiu"] = True
                    particulas += criar_explosao((cx, cy), cor)
                    if not tocou_vitoria:
                        tocar(som_explosao)
                        tocou_vitoria = True
                        shake_inicio = now

        novas_particulas = []
        for p in particulas:
            t = (now - p["tempo"]) / 1000
            if t < p["vida"]:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.05
                a = int(255 * (1 - t / p["vida"]))
                r = max(1, p["raio"] * (1 - t / p["vida"]))
                circulo_alpha(superficie_jogo, p["cor"], (p["x"], p["y"]), r, a)
                novas_particulas.append(p)
        particulas = novas_particulas

        if tempo_animacao_comum:
            decorrido = (tempo_animacao_comum - tempo_inicio_fase) / 1000
        else:
            decorrido = (now - tempo_inicio_fase) / 1000
        tempo_restante = max(0, tempo_limite - int(decorrido))
        if tempo_restante_congelado is not None:
            tempo_restante = tempo_restante_congelado

        if tempo_restante == 0 and not laser_atingiu_todos and not popup_fase_concluida:
            if not popup_ativa:
                popup_ativa = True
                if not tocou_erro:
                    tocar(som_erro)
                    tocou_erro = True

        tempo_desde_animacao = (now - tempo_animacao_comum) / 1000 if tempo_animacao_comum else 0
        if laser_atingiu_todos and not particulas and tempo_desde_animacao >= 1 and not popup_fase_concluida:
            popup_fase_concluida = True
            if tempo_restante_congelado is None:
                tempo_restante_congelado = tempo_restante

        shake_dx = shake_dy = 0
        if shake_inicio and now - shake_inicio < 400:
            forca = 8 * (1 - (now - shake_inicio) / 400)
            shake_dx = random.uniform(-forca, forca)
            shake_dy = random.uniform(-forca, forca)

        tela.blit(fundo_surf, (0, 0))
        tela.blit(superficie_jogo, (shake_dx, shake_dy))

        info = fonte_info_b.render(f"Nivel {nivel_atual}", True, COR_TEXTO)
        tela.blit(info, (24, 16))
        mov_txt = fonte_info.render(f"Movimentos: {movimentos}/{mov_esperados}", True, (190, 190, 205))
        tela.blit(mov_txt, (largura_tela - mov_txt.get_width() - 24, 18))

        barra_x, barra_y, barra_w = 24, 42, largura_tela - 48
        fracao = tempo_restante / tempo_limite if tempo_limite else 0
        cor_barra = (90, 220, 120) if fracao > 0.5 else (240, 200, 70) if fracao > 0.2 else (240, 80, 80)
        pygame.draw.rect(tela, (40, 40, 54), (barra_x, barra_y, barra_w, 8), border_radius=4)
        pygame.draw.rect(tela, cor_barra, (barra_x, barra_y, int(barra_w * fracao), 8), border_radius=4)
        t_txt = fonte_info.render(f"{tempo_restante}s", True, (190, 190, 205))
        tela.blit(t_txt, (largura_tela // 2 - t_txt.get_width() // 2, barra_y + 12))

        desenhar_botao(tela, botao_reiniciar, "Reiniciar", fonte_botao, botao_reiniciar.collidepoint((mouse_x, mouse_y)))
        cor_undo = botao_desfazer.collidepoint((mouse_x, mouse_y))
        desenhar_botao(tela, botao_desfazer, "Desfazer (Z)", fonte_botao, cor_undo)
        desenhar_botao(tela, botao_menu, "Menu", fonte_botao, botao_menu.collidepoint((mouse_x, mouse_y)))

        if popup_ativa:
            overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            tela.blit(overlay, (0, 0))
            rect = pygame.Rect((largura_tela - 320) // 2, (altura_tela - 180) // 2, 320, 180)
            pygame.draw.rect(tela, (48, 48, 64), rect, border_radius=16)
            pygame.draw.rect(tela, (240, 90, 90), rect, 2, border_radius=16)
            t1 = fonte_popup.render("Tempo esgotado!", True, COR_TEXTO)
            tela.blit(t1, (largura_tela // 2 - t1.get_width() // 2, rect.top + 40))
            desenhar_botao(tela, popup_botao, "Reiniciar", fonte_botao, popup_botao.collidepoint((mouse_x, mouse_y)), True)

        if popup_fase_concluida:
            overlay = pygame.Surface((largura_tela, altura_tela), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            tela.blit(overlay, (0, 0))
            rect = pygame.Rect((largura_tela - 380) // 2, (altura_tela - 280) // 2, 380, 280)
            pygame.draw.rect(tela, (54, 54, 72), rect, border_radius=20)
            pygame.draw.rect(tela, (120, 200, 150), rect, 2, border_radius=20)

            titulo = fonte_popup_grande.render(f"Nivel {nivel_atual} concluido!", True, COR_TEXTO)
            tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, rect.top + 24))

            if movimentos <= mov_esperados:
                estrelas = 3
            elif movimentos <= mov_esperados + 2:
                estrelas = 2
            else:
                estrelas = 1

            for i in range(3):
                cx = largura_tela // 2 - 75 + i * 55
                cy = rect.top + 100
                preenchida = i < estrelas
                if preenchida and estrela_cheia:
                    tela.blit(estrela_cheia, (cx - 20, cy - 20))
                elif not preenchida and estrela_vazia:
                    tela.blit(estrela_vazia, (cx - 20, cy - 20))
                else:
                    desenhar_estrela(tela, (cx, cy), 24, (255, 215, 90), preenchida)

            s1 = fonte_popup.render(f"Tempo restante: {tempo_restante}s", True, COR_TEXTO)
            tela.blit(s1, (largura_tela // 2 - s1.get_width() // 2, rect.top + 145))
            s2 = fonte_popup.render(f"Movimentos: {movimentos}/{mov_esperados}", True, COR_TEXTO)
            tela.blit(s2, (largura_tela // 2 - s2.get_width() // 2, rect.top + 175))

            popup_botao = pygame.Rect(rect.left + 30, rect.bottom - 56, 150, 38)
            popup_botao_proximo = pygame.Rect(rect.right - 180, rect.bottom - 56, 150, 38)
            desenhar_botao(tela, popup_botao, "Reiniciar", fonte_botao, popup_botao.collidepoint((mouse_x, mouse_y)))
            ultimo = nivel_atual + 1 not in levels
            desenhar_botao(tela, popup_botao_proximo, "Finalizar" if ultimo else "Proximo nivel",
                           fonte_botao, popup_botao_proximo.collidepoint((mouse_x, mouse_y)), True)

        pygame.display.flip()
        clock.tick(60)


def main():
    while True:
        acao = tela_inicial()
        if acao == "sair":
            break
        if acao == "iniciar":
            nivel = 1
        elif acao == "selecionar":
            nivel = selecionar_fase()
            if nivel is None:
                continue
            if nivel == "sair":
                break
        else:
            continue
        resultado = jogar(nivel)
        if resultado == "sair":
            break
        if resultado == "vitoria":
            if tela_vitoria() == "sair":
                break
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
