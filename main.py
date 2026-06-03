import asyncio
import pygame
import sys
import re
import math
import random

# Inicializa o Pygame
pygame.init()

# Task 11: Resolução 16:9
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DECODIFICA: Guardiões das Lendas")

# Task 1: Paleta Amazônica
BG_TOP = (6, 28, 14)
BG_BOT = (2, 10, 6)
GOLD = (212, 175, 55)
GOLD_LIGHT = (240, 210, 100)
GOLD_DIM = (140, 115, 35)
FOREST = (34, 100, 50)
FOREST_DARK = (18, 50, 28)
CARD_BG = (14, 38, 22)
CARD_BORDER = (30, 70, 40)
CARD_HOVER_COL = (22, 55, 35)
ACCENT_ORANGE = (255, 140, 0)
DANGER = (200, 50, 50)
DANGER_LIGHT = (230, 80, 80)
TEXT_COLOR = (235, 225, 205)
TEXT_DIM = (160, 150, 130)
PARCHMENT = (245, 235, 215)
PARCHMENT_DARK = (200, 185, 160)
HUD_BG = (10, 30, 18, 180)

# Task 2: Fontes e Tipografia
pygame.font.init()
font_mega = pygame.font.SysFont("georgia", 72, bold=True)
font_title = pygame.font.SysFont("georgia", 42, bold=True)
font_subtitle = pygame.font.SysFont("georgia", 28, italic=True)
font_text = pygame.font.SysFont("verdana", 19)
font_btn = pygame.font.SysFont("verdana", 22, bold=True)
font_hud = pygame.font.SysFont("verdana", 18, bold=True)
font_small = pygame.font.SysFont("verdana", 14)
font_icon = pygame.font.SysFont("verdana", 26, bold=True)

# Dados dos Capítulos
CHAPTERS_DATA = [
    {
        "name": "Capítulo 1: Lenda do Guaraná",
        "rank": "Aprendiz",
        "color": FOREST,
        "paragraphs": [
            {"id": "A", "text": "Toda a tribo xorou muito a perda da criança. Tupã se compadeceu do terrível zacrifício e enviou uma mensagem aos pajés."},
            {"id": "B", "text": "Há muito tempo, numa aldeia na floresta, vivia um indiozinho muito querido. Ele trazia muita alegria e forca para o seu povo."},
            {"id": "C", "text": "A mãe plantou os olhos do menino na terra fértil. Ali nasceu uma planta nova, cujas sementes parecem olhos: o guaraná."},
            {"id": "D", "text": "Jurupari, o espírito do mal, sentiu inveja da criança e se transformou em uma serpente poderoza para atacá-la na floresta."}
        ],
        "correct_order": ["B", "D", "A", "C"],
        "bugs": {
            "xorou": {"correto": "chorou", "opcoes": ["chorou", "xorou", "xourou"]},
            "zacrifício": {"correto": "sacrifício", "opcoes": ["sacrifício", "zacrifício", "sacrifisio"]},
            "forca": {"correto": "força", "opcoes": ["força", "forca", "forsa"]},
            "poderoza": {"correto": "poderosa", "opcoes": ["poderosa", "poderoza", "poderoça"]}
        },
        "mec4_options": [
            ("Trocas de S por Z", True),
            ("Trocas de CH por X", False),
            ("Trocas de C por Ç", False),
            ("Trocas de G por J", False)
        ]
    },
    {
        "name": "Capítulo 2: Lenda do Mapinguari",
        "rank": "Explorador",
        "color": ACCENT_ORANGE,
        "paragraphs": [
            {"id": "A", "text": "A fera andava pesadamente pelas matas, devorando tudo o que encontrava. Os caçadores evitavam a selva, com medo de encontrar a criatura selvajem."},
            {"id": "B", "text": "Dizem que o Mapinguari era um antigo índio guerreiro que descobriu o segredo da imortalidade. Mas a magia teve um preço terrível."},
            {"id": "C", "text": "Hoje, quem se arrisca numa longa viajem pela mata densa sabe que não deve chingar a natureza, para não acordar o monstro."},
            {"id": "D", "text": "Ele se transformou num monstro enorme, coberto de pelos ruivos, com um olho só e uma boca assustadora na barriga, impossível não enchergar de longe."}
        ],
        "correct_order": ["B", "D", "A", "C"],
        "bugs": {
            "selvajem": {"correto": "selvagem", "opcoes": ["selvagem", "selvajem", "selvagên"]},
            "enchergar": {"correto": "enxergar", "opcoes": ["enxergar", "enchergar", "enxegar"]},
            "viajem": {"correto": "viagem", "opcoes": ["viagem", "viajem", "viagen"]},
            "chingar": {"correto": "xingar", "opcoes": ["xingar", "chingar", "ximgar"]}
        },
        "mec4_options": [
            ("Troca de G por J e X por CH", True),
            ("Troca de S por Z e C por Ç", False),
            ("Uso incorreto de H no início", False),
            ("Omissão de R no infinitivo", False)
        ]
    },
    {
        "name": "Capítulo 3: Lenda da Cobra Grande",
        "rank": "Guardião",
        "color": DANGER,
        "paragraphs": [
            {"id": "A", "text": "Com o passar do tempo, a cobra cresceu tanto que o rio ficou pequeno. Ela se tornou a Boiúna, uma assonbração dos rios."},
            {"id": "B", "text": "Conta a lenda que uma mulher grávida deu à luz duas crianças gêmeas. Uma delas tinha a forma de uma serpente escura e assustadora."},
            {"id": "C", "text": "A mãe, com medo, jogou a serpente no rio. Lá, ela se alimentava dos peixes e de qualquer animau que caísse na água."},
            {"id": "D", "text": "Os pescadores dizem que, à noite, seus olhos brilham como fogo, e quando ela se move, um forte temporau e o som de tanbor anunciam sua chegada."},
            {"id": "E", "text": "A Iara, sereia dos rios, cantava uma música suave para atrair os pescadores. Ninguém resistia ao seu encanto na floresta."}
        ],
        "correct_order": ["B", "C", "A", "D"],
        "bugs": {
            "assonbração": {"correto": "assombração", "opcoes": ["assombração", "assonbração", "asombração"]},
            "animau": {"correto": "animal", "opcoes": ["animal", "animau", "animalo"]},
            "temporau": {"correto": "temporal", "opcoes": ["temporal", "temporau", "temporaw"]},
            "tanbor": {"correto": "tambor", "opcoes": ["tambor", "tanbor", "tâmbor"]}
        },
        "mec4_options": [
            ("Uso de N antes de P/B e U no final", True),
            ("Troca de J por G e X por CH", False),
            ("Uso incorreto de SS ou Ç", False),
            ("Confusão de R e RR", False)
        ]
    },
    {
        "name": "Capítulo 4: Lenda da Vitória-Régia",
        "rank": "Mestre",
        "color": GOLD,
        "paragraphs": [
            {"id": "A", "text": "Certa noite, Naiá viu o reflexo da lua nas águas escuras do lago. Pensando que a lua tinha descido para buscá-la, ela mergulhou com muita corassão."},
            {"id": "B", "text": "Naiá era uma jovem índia que se apaixonou por Jaci, a lua. Ela sonhava em ser transformada em uma estrela brilhante no céu, ao lado de Jaci."},
            {"id": "C", "text": "Jaci ficou com pena da belesa da jovem e a transformou não em uma estrela do céu, mas na Estrela das águas: a Vitória-Régia, que floresce à noite para encantar cada páçaro."},
            {"id": "D", "text": "Toda noite, ela corria pelas matas tentando alcançar a lua. A bela índia ficava triste quando não conseguia, sentindo uma enorme emossão."},
            {"id": "E", "text": "O boto cor-de-rosa surgia nas festas vestido de branco, dançando com as moças mais bonitas da aldeia."},
            {"id": "F", "text": "Nas noites de lua cheia, o lobisomem corria pelos campos assustando as ovelhas e os moradores da região."}
        ],
        "correct_order": ["B", "D", "A", "C"],
        "bugs": {
            "corassão": {"correto": "coração", "opcoes": ["coração", "corassão", "corasão"]},
            "belesa": {"correto": "beleza", "opcoes": ["beleza", "belesa", "beleça"]},
            "páçaro": {"correto": "pássaro", "opcoes": ["pássaro", "páçaro", "pácaro"]},
            "emossão": {"correto": "emoção", "opcoes": ["emoção", "emossão", "emosão"]}
        },
        "mec4_options": [
            ("Confusão entre SS, Ç e Z", True),
            ("Troca de C por S e H por NH", False),
            ("Uso incorreto de L no lugar de U", False),
            ("Omissão de M antes de P e B", False)
        ]
    }
]

# --- Estado Global ---
game_state = "MENU"
lives = 3
score = 0
message = ""
message_timer = 0
frame_count = 0
current_chapter_index = 0
unlocked_chapters = 4
typed_word = ""

cinematic_slide = 0
cinematic_timer = 0
saved_order = []
m5_start_frame = 0
cinematic_texts = [
    "No coração da floresta amazônica...",
    "As lendas mantinham o equilíbrio da natureza por milênios.",
    "Até que o 'Bug da Ortografia' corrompeu as histórias!",
    "Se as palavras se perderem, as lendas desaparecerão. Precisamos de um Guardião."
]

cards = []
clickable_words = []
bugs_to_fix = []
current_bug_index = 0
modal_buttons = []
mec4_buttons = []
roadmap_buttons = []

# Task 3: Sistema de Partículas (Vagalumes)
class Firefly:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed_x = random.uniform(-0.3, 0.3)
        self.speed_y = random.uniform(-0.2, 0.2)
        self.phase = random.uniform(0, math.pi * 2)
        self.size = random.uniform(1.5, 3.5)
        self.brightness = random.uniform(0.3, 1.0)
        
    def update(self, dt):
        self.x += self.speed_x + math.sin(self.phase) * 0.15
        self.y += self.speed_y + math.cos(self.phase * 0.7) * 0.1
        self.phase += 0.02
        self.brightness = 0.4 + 0.6 * abs(math.sin(self.phase * 0.5))
        
        if self.x < -10: self.x = WIDTH + 10
        if self.x > WIDTH + 10: self.x = -10
        if self.y < -10: self.y = HEIGHT + 10
        if self.y > HEIGHT + 10: self.y = -10
        
    def draw(self, surface):
        alpha = int(self.brightness * 180)
        if game_state == "CINEMATIC" and cinematic_slide == 2:
            r, g, b = 200, 20, 20
        else:
            r = int(GOLD[0] * self.brightness)
            g = int(GOLD[1] * self.brightness)
            b = int(GOLD[2] * self.brightness * 0.6)
        r = min(255, r)
        g = min(255, g)
        
        glow_surf = pygame.Surface((int(self.size*8), int(self.size*8)), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (r, g, b, alpha//3), (int(self.size*4), int(self.size*4)), int(self.size*4))
        pygame.draw.circle(glow_surf, (r, g, b, alpha), (int(self.size*4), int(self.size*4)), int(self.size*1.5))
        surface.blit(glow_surf, (int(self.x - self.size*4), int(self.y - self.size*4)))

fireflies = [Firefly() for _ in range(35)]

# Partículas de vitória
class VictoryParticle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = -random.randint(10, 200)
        self.speed = random.uniform(1.5, 4)
        self.size = random.uniform(2, 5)
        self.drift = random.uniform(-1, 1)
        self.color = random.choice([GOLD, GOLD_LIGHT, ACCENT_ORANGE, FOREST])
        
    def update(self):
        self.y += self.speed
        self.x += self.drift + math.sin(self.y * 0.02) * 0.5
        if self.y > HEIGHT + 10:
            self.y = -10
            self.x = random.randint(0, WIDTH)
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

victory_particles = [VictoryParticle() for _ in range(60)]

# --- Funções de Desenho ---
def draw_gradient_bg(surface):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(BG_TOP[0] * (1 - t) + BG_BOT[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOT[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOT[2] * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

# Pre-render o gradiente (performance)
bg_surface = pygame.Surface((WIDTH, HEIGHT))
draw_gradient_bg(bg_surface)

bg_surface_glitch = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    t = y / HEIGHT
    gr = int(80 * (1 - t) + 30 * t)
    gg = int(10 * (1 - t) + 0 * t)
    gb = int(10 * (1 - t) + 0 * t)
    pygame.draw.line(bg_surface_glitch, (gr, gg, gb), (0, y), (WIDTH, y))

def draw_fireflies(surface):
    for f in fireflies:
        f.update(1)
        f.draw(surface)

def draw_hud(surface):
    hud_panel = pygame.Surface((WIDTH, 55), pygame.SRCALPHA)
    hud_panel.fill((10, 30, 18, 160))
    surface.blit(hud_panel, (0, 0))
    pygame.draw.line(surface, GOLD_DIM, (0, 55), (WIDTH, 55), 1)
    
    # Vidas como círculos
    lx = 30
    label = font_hud.render("Vidas:", True, TEXT_DIM)
    surface.blit(label, (lx, 17))
    lx += label.get_width() + 10
    for i in range(3):
        color = DANGER if i < lives else (60, 30, 30)
        pygame.draw.circle(surface, color, (lx + i * 28, 28), 10)
        if i < lives:
            pygame.draw.circle(surface, DANGER_LIGHT, (lx + i * 28 - 3, 25), 3)
    
    # Pontuação com diamante
    px = WIDTH - 250
    # Diamante (losango)
    diamond_pts = [(px, 28), (px+10, 18), (px+20, 28), (px+10, 38)]
    pygame.draw.polygon(surface, GOLD, diamond_pts)
    pygame.draw.polygon(surface, GOLD_LIGHT, [(px+5, 28), (px+10, 20), (px+15, 28)])
    
    pts_text = font_hud.render(f"{score} Pontos de Código", True, GOLD_LIGHT)
    surface.blit(pts_text, (px + 28, 17))

# --- Funções Auxiliares ---
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        fw, fh = font.size(' '.join(current_line))
        if fw > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def clean_word(w):
    return re.sub(r'[^\w]', '', w.lower())

def show_msg(msg, frames=180):
    global message, message_timer
    message = msg
    message_timer = frames

# --- Classes ---
class DraggableCard:
    def __init__(self, x, y, w, h, paragraph_data, color_index):
        self.rect = pygame.Rect(x, y, w, h)
        self.data = paragraph_data
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
        # Scaffolding visual apenas na Fase 1
        if current_chapter_index == 0:
            cores = [FOREST, ACCENT_ORANGE, GOLD, DANGER]
            self.border_color = cores[color_index % len(cores)]
        else:
            self.border_color = CARD_BORDER
            
        self.lines = wrap_text(self.data["text"], font_text, w - 40)
        
    def draw(self, surface):
        # Sombra
        if self.dragging:
            shadow = pygame.Surface((self.rect.w + 6, self.rect.h + 6), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 60))
            surface.blit(shadow, (self.rect.x + 4, self.rect.y + 6))
            
        color = CARD_HOVER_COL if self.dragging else CARD_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, CARD_BORDER, self.rect, width=1, border_radius=12)
        # Barra lateral
        bar = pygame.Rect(self.rect.x, self.rect.y, 12, self.rect.height)
        pygame.draw.rect(surface, self.border_color, bar, border_top_left_radius=12, border_bottom_left_radius=12)
        
        y_offset = self.rect.y + 15
        for line in self.lines:
            text_surf = font_text.render(line, True, TEXT_COLOR)
            surface.blit(text_surf, (self.rect.x + 24, y_offset))
            y_offset += 26

class ClickableWord:
    def __init__(self, x, y, word_text):
        self.text = word_text
        self.clean = clean_word(word_text)
        self.surf = font_text.render(self.text, True, PARCHMENT)
        self.rect = pygame.Rect(x, y, self.surf.get_width() + 6, self.surf.get_height() + 4)
        self.marked = False
        self.corrected = False
        
    def set_text(self, new_text):
        self.text = new_text
        self.clean = clean_word(new_text)
        self.surf = font_text.render(self.text, True, GOLD_LIGHT)
        
    def draw(self, surface):
        if self.marked:
            pygame.draw.rect(surface, ACCENT_ORANGE, self.rect, border_radius=4)
            tsurf = font_text.render(self.text, True, (20, 10, 0))
            surface.blit(tsurf, (self.rect.x + 3, self.rect.y + 2))
        else:
            surface.blit(self.surf, (self.rect.x + 3, self.rect.y + 2))
            if self.corrected:
                pygame.draw.line(surface, GOLD, (self.rect.x, self.rect.bottom - 1), (self.rect.right, self.rect.bottom - 1), 2)

class Button:
    def __init__(self, x, y, w, h, text, color=FOREST, text_color=GOLD_LIGHT):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False
        self.text_surf = font_btn.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
    def draw(self, surface):
        # Sombra
        shadow_rect = self.rect.move(3, 4)
        pygame.draw.rect(surface, (0, 0, 0, 80) if not self.hovered else (0,0,0), shadow_rect, border_radius=10)
        
        if self.hovered:
            # Borda glow
            glow_rect = self.rect.inflate(4, 4)
            pygame.draw.rect(surface, GOLD, glow_rect, border_radius=12)
            
        col = tuple(min(255, c + 25) for c in self.color) if self.hovered else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=10)
        
        if not self.hovered:
            pygame.draw.rect(surface, GOLD_DIM, self.rect, width=1, border_radius=10)
        
        self.text_surf = font_btn.render(self.text, True, (255,255,255) if self.hovered else self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        surface.blit(self.text_surf, self.text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Botões
btn_play_menu = Button(WIDTH//2 - 140, HEIGHT//2 + 80, 280, 55, "Iniciar Aventura", FOREST_DARK, GOLD_LIGHT)
btn_next_intro = Button(WIDTH//2 - 110, HEIGHT - 110, 220, 50, "Entendi!", FOREST_DARK, GOLD_LIGHT)
btn_check = Button(WIDTH//2 - 120, HEIGHT - 85, 240, 52, "Verificar Ordem", FOREST_DARK, GOLD_LIGHT)
btn_finish_bugs = Button(WIDTH//2 - 120, HEIGHT - 85, 240, 52, "Terminei a Busca", FOREST_DARK, GOLD_LIGHT)
btn_back_roadmap = Button(WIDTH//2 - 140, HEIGHT - 100, 280, 55, "Voltar ao Mapa", FOREST_DARK, GOLD_LIGHT)

btn_skip_cine = Button(WIDTH - 160, HEIGHT - 60, 130, 40, "Pular >>", (60, 60, 60), (200, 200, 200))
btn_start_mission = Button(WIDTH//2 - 140, HEIGHT//2 + 50, 280, 55, "Assumir Missão", DANGER, GOLD_LIGHT)
btn_finish_book = Button(WIDTH//2 - 120, HEIGHT - 85, 240, 52, "Concluir Lenda", FOREST_DARK, GOLD_LIGHT)

all_buttons = [btn_play_menu, btn_next_intro, btn_check, btn_finish_bugs, btn_back_roadmap, btn_skip_cine, btn_start_mission, btn_finish_book]

def setup_mecanica_1():
    global cards
    cards = []
    start_y = 100
    chapter = CHAPTERS_DATA[current_chapter_index]
    num_cards = len(chapter["paragraphs"])
    
    # Ajustar tamanho e espaçamento dependendo da quantidade (até 6 cartas)
    card_h = 95
    y_inc = 95
    
    for i, p in enumerate(chapter["paragraphs"]):
        cards.append(DraggableCard(20, start_y, 540, card_h, p, i))
        start_y += y_inc

def setup_mecanica_2(ordered_ids):
    global clickable_words
    clickable_words = []
    start_x = 120
    start_y = 160
    max_w = WIDTH - 120
    current_x = start_x
    current_y = start_y
    chapter = CHAPTERS_DATA[current_chapter_index]
    for pid in ordered_ids:
        pdata = next(p for p in chapter["paragraphs"] if p["id"] == pid)
        words = pdata["text"].split(' ')
        for w in words:
            surf = font_text.render(w, True, PARCHMENT)
            if current_x + surf.get_width() > max_w:
                current_x = start_x
                current_y += 38
            cw = ClickableWord(current_x, current_y, w)
            clickable_words.append(cw)
            current_x += surf.get_width() + 12
        current_x = start_x
        current_y += 55

def setup_mecanica_3():
    global bugs_to_fix, current_bug_index, modal_buttons, typed_word
    chapter_bugs = CHAPTERS_DATA[current_chapter_index]["bugs"]
    bugs_to_fix = [cw for cw in clickable_words if cw.clean in chapter_bugs.keys()]
    current_bug_index = 0
    typed_word = ""
    create_modal_buttons()
    
def create_modal_buttons():
    global modal_buttons, typed_word
    modal_buttons = []
    typed_word = ""
    if current_bug_index >= len(bugs_to_fix):
        return
    
    # Se for Capítulo 3 ou 4 (index >= 2), não criamos botões de múltipla escolha
    if current_chapter_index >= 2:
        return

    bug_cw = bugs_to_fix[current_bug_index]
    chapter_bugs = CHAPTERS_DATA[current_chapter_index]["bugs"]
    opcoes = chapter_bugs[bug_cw.clean]["opcoes"]
    start_y = HEIGHT//2 + 10
    for i, op in enumerate(opcoes):
        btn = Button(WIDTH//2 - 160, start_y, 320, 48, op, CARD_BG, PARCHMENT)
        btn.is_correct = (op == chapter_bugs[bug_cw.clean]["correto"])
        modal_buttons.append(btn)
        all_buttons.append(btn)
        start_y += 62

def setup_mecanica_4():
    global mec4_buttons
    mec4_buttons = []
    start_y = HEIGHT//2 - 40
    opcoes = CHAPTERS_DATA[current_chapter_index]["mec4_options"]
    for txt, correct in opcoes:
        btn = Button(WIDTH//2 - 160, start_y, 320, 48, txt, CARD_BG, PARCHMENT)
        btn.is_correct = correct
        mec4_buttons.append(btn)
        all_buttons.append(btn)
        start_y += 62

def check_order():
    global game_state, lives, saved_order
    # Apenas cartões na zona alvo (exclui a lixeira no fundo)
    cards_in_zone = [c for c in cards if c.rect.centerx > 600 and c.rect.centery < HEIGHT - 90]
    cards_in_zone.sort(key=lambda c: c.rect.y)
    
    correct = CHAPTERS_DATA[current_chapter_index]["correct_order"]
    
    if len(cards_in_zone) < len(correct):
        show_msg(f"Coloque os {len(correct)} parágrafos da lenda na zona alvo!", 180)
        return
        
    order = [c.data["id"] for c in cards_in_zone]
    
    if order == correct:
        show_msg("A lenda faz sentido! Avançando...", 120)
        saved_order = order
        game_state = "MECANICA_1_WIN"
    else:
        lives -= 1
        if len(order) > len(correct):
            show_msg("Há um parágrafo intruso! Jogue-o na Lixeira.", 180)
        else:
            show_msg("Ordem incorreta! Lembre-se do Início, Meio e Fim.", 120)
            
        if lives <= 0:
            show_msg("Fim de Jogo! A lenda foi corrompida.", 180)
            game_state = "FIM"

def check_bugs():
    global game_state, score, lives
    marked_words = [cw for cw in clickable_words if cw.marked]
    if not marked_words:
        show_msg("Clique nas palavras com erro ortográfico para marcá-las.", 180)
        return
    real_bugs = 0
    fakes = 0
    chapter_bugs = CHAPTERS_DATA[current_chapter_index]["bugs"]
    for cw in marked_words:
        if cw.clean in chapter_bugs.keys():
            real_bugs += 1
        else:
            fakes += 1
            cw.marked = False
    if fakes > 0:
        score -= fakes * 5
        show_msg(f"Você marcou {fakes} palavras corretas como bug! (-{fakes*5} pts)", 200)
    elif real_bugs == len(chapter_bugs):
        score += 100
        show_msg("Todos os bugs encontrados! Hora de corrigir.", 120)
        game_state = "MECANICA_2_WIN"
    else:
        show_msg(f"Faltam bugs... Encontrou {real_bugs} de {len(chapter_bugs)}.", 180)

def snap_cards():
    cards_in_zone = [c for c in cards if c.rect.centerx > 600 and c.rect.centery < HEIGHT - 90]
    cards_in_zone.sort(key=lambda c: c.rect.y)
    start_y = 110
    for c in cards_in_zone:
        c.rect.x = 610
        c.rect.y = start_y
        start_y += 100

def draw_parchment(surface, rect):
    pygame.draw.rect(surface, PARCHMENT_DARK, rect.inflate(6,6), border_radius=14)
    pygame.draw.rect(surface, PARCHMENT, rect, border_radius=12)
    # Ornamento superior
    pygame.draw.line(surface, GOLD_DIM, (rect.x + 20, rect.y + 12), (rect.x + rect.w - 20, rect.y + 12), 1)
    pygame.draw.line(surface, GOLD_DIM, (rect.x + 20, rect.y + 15), (rect.x + rect.w - 20, rect.y + 15), 1)
    # Ornamento inferior
    pygame.draw.line(surface, GOLD_DIM, (rect.x + 20, rect.bottom - 15), (rect.x + rect.w - 20, rect.bottom - 15), 1)
    pygame.draw.line(surface, GOLD_DIM, (rect.x + 20, rect.bottom - 12), (rect.x + rect.w - 20, rect.bottom - 12), 1)

def draw_modal(surface, rect, border_color=GOLD):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    surface.blit(overlay, (0, 0))
    
    # Glow atrás do modal
    glow = rect.inflate(12, 12)
    pygame.draw.rect(surface, border_color, glow, border_radius=18)
    
    pygame.draw.rect(surface, BG_TOP, rect, border_radius=15)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=15)
    
    # Decoração superior
    pygame.draw.line(surface, GOLD_DIM, (rect.x + 30, rect.y + 55), (rect.x + rect.w - 30, rect.y + 55), 1)

def draw_drop_zone(surface):
    dz = pygame.Rect(600, 100, WIDTH - 640, HEIGHT - 200)
    pygame.draw.rect(surface, (10, 25, 16), dz, border_radius=12)
    # Borda pontilhada
    for i in range(0, dz.w, 16):
        pygame.draw.line(surface, GOLD_DIM, (dz.x + i, dz.y), (dz.x + min(i+8, dz.w), dz.y), 1)
        pygame.draw.line(surface, GOLD_DIM, (dz.x + i, dz.bottom), (dz.x + min(i+8, dz.w), dz.bottom), 1)
    for i in range(0, dz.h, 16):
        pygame.draw.line(surface, GOLD_DIM, (dz.x, dz.y + i), (dz.x, dz.y + min(i+8, dz.h)), 1)
        pygame.draw.line(surface, GOLD_DIM, (dz.right, dz.y + i), (dz.right, dz.y + min(i+8, dz.h)), 1)
    
    hint = font_small.render("Solte os parágrafos da lenda aqui", True, TEXT_DIM)
    surface.blit(hint, (dz.centerx - hint.get_width()//2, dz.y + 15))

def draw_trash_zone(surface):
    chapter = CHAPTERS_DATA[current_chapter_index]
    if len(chapter["paragraphs"]) > len(chapter["correct_order"]):
        tz = pygame.Rect(600, HEIGHT - 85, WIDTH - 640, 65)
        pygame.draw.rect(surface, (30, 10, 10), tz, border_radius=10)
        pygame.draw.rect(surface, DANGER_LIGHT, tz, width=2, border_radius=10)
        hint = font_small.render("LIXEIRA (Parágrafos Intrusos)", True, DANGER_LIGHT)
        surface.blit(hint, (tz.centerx - hint.get_width()//2, tz.centery - hint.get_height()//2))

def draw_roadmap_line(surface):
    # Linha vertical da trilha
    x = 80
    for y in range(200, 620, 4):
        color = FOREST if y < 300 else CARD_BORDER
        pygame.draw.line(surface, color, (x, y), (x, y+2), 2)

async def main():
    global game_state, message_timer, current_bug_index, score, lives, frame_count
    global current_chapter_index, unlocked_chapters, typed_word, active_card, m5_start_frame
    clock = pygame.time.Clock()
    running = True
    active_card = None
    mouse_pos = (0, 0)

    while running:
        frame_count += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for btn in all_buttons: btn.update_hover(mouse_pos)
                for btn in modal_buttons: btn.update_hover(mouse_pos)
                for btn in mec4_buttons: btn.update_hover(mouse_pos)
                    
                if active_card:
                    active_card.rect.x = event.pos[0] + active_card.offset_x
                    active_card.rect.y = event.pos[1] + active_card.offset_y
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "MENU":
                    if btn_play_menu.is_clicked(event.pos):
                        game_state = "CINEMATIC"
                        cinematic_slide, cinematic_timer = 0, 0
                elif game_state == "CINEMATIC":
                    if btn_skip_cine.is_clicked(event.pos) and cinematic_slide < 3:
                        game_state = "INTRO"
                    elif cinematic_slide == 3 and btn_start_mission.is_clicked(event.pos):
                        game_state = "INTRO"
                elif game_state == "INTRO" and btn_next_intro.is_clicked(event.pos):
                    game_state = "ROADMAP"
                elif game_state == "ROADMAP":
                    for btn in roadmap_buttons:
                        if btn.is_clicked(event.pos):
                            current_chapter_index = btn.chapter_index
                            setup_mecanica_1()
                            game_state = "MECANICA_1"
                elif game_state == "MECANICA_1":
                    if btn_check.is_clicked(event.pos): check_order()
                    else:
                        for card in reversed(cards):
                            if card.rect.collidepoint(event.pos):
                                active_card = card
                                card.dragging = True
                                card.offset_x = card.rect.x - event.pos[0]
                                card.offset_y = card.rect.y - event.pos[1]
                                cards.remove(card); cards.append(card)
                                break
                elif game_state == "MECANICA_2":
                    if btn_finish_bugs.is_clicked(event.pos): check_bugs()
                    else:
                        for cw in clickable_words:
                            if cw.rect.collidepoint(event.pos): cw.marked = not cw.marked; break
                elif game_state == "MECANICA_3":
                    for btn in modal_buttons:
                        if btn.is_clicked(event.pos):
                            if btn.is_correct:
                                score += 20; show_msg("Ortografia correta! +20 pts", 90)
                                cw = bugs_to_fix[current_bug_index]
                                cw.marked = False; cw.corrected = True
                                cw.set_text(cw.text.replace(cw.clean, btn.text))
                                current_bug_index += 1
                                if current_bug_index >= len(bugs_to_fix): game_state = "MECANICA_3_WIN"
                                else: create_modal_buttons()
                            else: lives -= 1; show_msg("Grafia incorreta! -1 vida", 120)
                            break
                elif game_state == "MECANICA_4" and any(btn.is_clicked(event.pos) for btn in mec4_buttons):
                    for btn in mec4_buttons:
                        if btn.is_clicked(event.pos):
                            if btn.is_correct: 
                                score += 150; show_msg("Padrão identificado! +150 pts. Avançando...", 120); game_state = "MECANICA_4_WIN"
                            else: lives -= 1; show_msg("Esse não foi o padrão principal. Tente novamente!", 120)
                elif game_state == "MECANICA_5" and btn_finish_book.is_clicked(event.pos):
                    game_state = "FIM"
                elif game_state == "FIM" and btn_back_roadmap.is_clicked(event.pos):
                    if current_chapter_index + 1 == unlocked_chapters and unlocked_chapters < len(CHAPTERS_DATA):
                        unlocked_chapters += 1
                    game_state = "ROADMAP"
                            
            if event.type == pygame.KEYDOWN and game_state == "MECANICA_3" and current_chapter_index >= 2:
                if event.key == pygame.K_BACKSPACE: typed_word = typed_word[:-1]
                elif event.key == pygame.K_RETURN:
                    bug_cw = bugs_to_fix[current_bug_index]
                    correct_word = CHAPTERS_DATA[current_chapter_index]["bugs"][bug_cw.clean]["correto"]
                    if typed_word.strip().lower() == correct_word.lower():
                        score += 40; show_msg("Ortografia perfeita! +40 pts", 90)
                        cw = bugs_to_fix[current_bug_index]
                        cw.marked = False; cw.corrected = True
                        cw.set_text(cw.text.replace(cw.clean, correct_word))
                        current_bug_index += 1; typed_word = ""
                        if current_bug_index >= len(bugs_to_fix): game_state = "MECANICA_3_WIN"
                    else: lives -= 1; show_msg("Grafia incorreta!", 120)
                elif len(typed_word) < 20: typed_word += event.unicode
                            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and active_card:
                active_card.dragging = False; active_card = None

        if message_timer <= 0:
            if game_state == "MECANICA_1_WIN": setup_mecanica_2(saved_order); game_state = "MECANICA_2"
            elif game_state == "MECANICA_2_WIN": setup_mecanica_3(); game_state = "MECANICA_3"
            elif game_state == "MECANICA_3_WIN": setup_mecanica_4(); game_state = "MECANICA_4"
            elif game_state == "MECANICA_4_WIN": m5_start_frame = frame_count; game_state = "MECANICA_5"

        if game_state == "CINEMATIC" and cinematic_slide == 2: screen.blit(bg_surface_glitch, (0, 0))
        else: screen.blit(bg_surface, (0, 0))
            
        draw_fireflies(screen)
        if game_state not in ["MENU", "CINEMATIC", "INTRO", "ROADMAP", "FIM"]: draw_hud(screen)
            
        if game_state == "MENU":
            pulse = 0.7 + 0.3 * math.sin(frame_count * 0.03)
            gr = int(GOLD[0] * pulse)
            gg = int(GOLD[1] * pulse)
            gb = int(GOLD[2] * pulse)
            
            title = font_mega.render("DECODIFICA", True, (min(255,gr), min(255,gg), min(255,gb)))
            title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//3 - 30))
            screen.blit(title, title_rect)
            
            # Linha ornamental
            lw = 300
            ly = HEIGHT//3 + 25
            pygame.draw.line(screen, GOLD_DIM, (WIDTH//2 - lw//2, ly), (WIDTH//2 + lw//2, ly), 1)
            pygame.draw.circle(screen, GOLD_DIM, (WIDTH//2, ly), 3)
            
            sub = font_subtitle.render("Guardiões das Lendas da Amazônia", True, TEXT_DIM)
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//3 + 40))
            
            ver = font_small.render("Jogo Educacional - Língua Portuguesa + Pensamento Computacional", True, TEXT_DIM)
            screen.blit(ver, (WIDTH//2 - ver.get_width()//2, HEIGHT - 40))
            
            btn_play_menu.draw(screen)
            
        elif game_state == "CINEMATIC":
            cinematic_timer += 1
            text = cinematic_texts[cinematic_slide]
            if cinematic_slide < 2:
                alpha = min(255, int(cinematic_timer * 1.5))
                tsurf = font_title.render(text, True, GOLD_LIGHT)
                tsurf.set_alpha(alpha)
                screen.blit(tsurf, (WIDTH//2 - tsurf.get_width()//2, HEIGHT//2 - 20))
                if cinematic_timer > 240:
                    cinematic_slide += 1
                    cinematic_timer = 0
            elif cinematic_slide == 2:
                tsurf = font_title.render(text, True, DANGER_LIGHT)
                screen.blit(tsurf, (WIDTH//2 - tsurf.get_width()//2 + random.randint(-4, 4), HEIGHT//2 - 20 + random.randint(-4, 4)))
                if cinematic_timer > 180:
                    cinematic_slide = 3
                    cinematic_timer = 0
            elif cinematic_slide == 3:
                tsurf = font_title.render(text, True, GOLD_LIGHT)
                screen.blit(tsurf, (WIDTH//2 - tsurf.get_width()//2, HEIGHT//3))
                btn_start_mission.draw(screen)
            if cinematic_slide < 3:
                btn_skip_cine.draw(screen)
                
        elif game_state == "INTRO":
            parch_rect = pygame.Rect(WIDTH//2 - 350, 70, 700, 500)
            draw_parchment(screen, parch_rect)
            
            title = font_title.render("A Missão do Guardião", True, FOREST_DARK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            lines = [
                "A Amazônia guarda segredos milenares, mas um vírus",
                "de bugs ortográficos está corrompendo nossas lendas!",
                "",
                "Você foi convocado para usar o Pensamento",
                "Computacional e restaurá-las. Para isso:",
                "",
                "1. Organizar as partes da história",
                "2. Caçar palavras corrompidas",
                "3. Corrigir os bugs de escrita",
                "4. Mapear os erros mais comuns",
            ]
            
            y_off = 180
            step_colors = [None, None, None, None, None, None, FOREST, ACCENT_ORANGE, DANGER, GOLD_DIM]
            for i, line in enumerate(lines):
                if line:
                    color = step_colors[i] if step_colors[i] else (60, 40, 20)
                    tsurf = font_text.render(line, True, color)
                    screen.blit(tsurf, (WIDTH//2 - tsurf.get_width()//2, y_off))
                y_off += 32
                
            btn_next_intro.draw(screen)
            
        elif game_state == "ROADMAP":
            title = font_title.render("Mapa das Lendas", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
            
            sub = font_small.render("Cada lenda é um capítulo. Complete-os para se tornar o Mestre dos Padrões.", True, TEXT_DIM)
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 90))
            
            draw_roadmap_line(screen)
            roadmap_buttons.clear()
            
            for i, ch in enumerate(CHAPTERS_DATA):
                cy = 210 + i * 110
                unlocked = i < unlocked_chapters
                
                # Nó da trilha
                node_color = ch["color"] if unlocked else CARD_BORDER
                pygame.draw.circle(screen, node_color, (80, cy + 25), 12)
                if unlocked:
                    pygame.draw.circle(screen, GOLD_LIGHT, (76, cy + 21), 4)
                else:
                    # Cadeado
                    pygame.draw.rect(screen, (80,80,80), (74, cy+20, 12, 10), border_radius=2)
                    pygame.draw.arc(screen, (80,80,80), (73, cy+14, 14, 14), 0, math.pi, 2)
                
                # Card do capítulo
                card_rect = pygame.Rect(120, cy, WIDTH - 180, 70)
                card_col = CARD_BG if unlocked else (12, 22, 16)
                pygame.draw.rect(screen, card_col, card_rect, border_radius=10)
                pygame.draw.rect(screen, ch["color"] if unlocked else CARD_BORDER, card_rect, width=1, border_radius=10)
                pygame.draw.rect(screen, ch["color"] if unlocked else CARD_BORDER, (card_rect.x, card_rect.y, 10, card_rect.h), border_top_left_radius=10, border_bottom_left_radius=10)
                
                name_color = TEXT_COLOR if unlocked else TEXT_DIM
                name_surf = font_btn.render(ch["name"], True, name_color)
                screen.blit(name_surf, (card_rect.x + 25, card_rect.y + 12))
                
                rank_surf = font_small.render(ch["rank"] + (" - BLOQUEADO" if not unlocked else ""), True, ch["color"] if unlocked else CARD_BORDER)
                screen.blit(rank_surf, (card_rect.x + 25, card_rect.y + 42))
                
                if unlocked:
                    btn = Button(WIDTH - 250, cy + 14, 160, 42, "Jogar", ch["color"], GOLD_LIGHT)
                    btn.chapter_index = i
                    btn.update_hover(mouse_pos)
                    btn.draw(screen)
                    roadmap_buttons.append(btn)
        elif game_state in ["MECANICA_1", "MECANICA_1_WIN"]:
            title = font_title.render("Reorganização Narrativa", True, GOLD)
            screen.blit(title, (40, 65))
            inst = font_small.render("Arraste os parágrafos para a zona à direita, na ordem lógica da lenda.", True, TEXT_DIM)
            screen.blit(inst, (42, 108))
            
            draw_drop_zone(screen)
            draw_trash_zone(screen)
            for card in cards:
                card.draw(screen)
            btn_check.draw(screen)
            
        elif game_state in ["MECANICA_2", "MECANICA_2_WIN"]:
            title = font_title.render("Caça ao Bug", True, GOLD)
            screen.blit(title, (40, 65))
            inst = font_small.render("Clique nas palavras com erro ortográfico para marcá-las em laranja.", True, TEXT_DIM)
            screen.blit(inst, (42, 108))
            
            text_panel = pygame.Rect(80, 135, WIDTH - 160, HEIGHT - 260)
            pygame.draw.rect(screen, CARD_BG, text_panel, border_radius=14)
            pygame.draw.rect(screen, CARD_BORDER, text_panel, width=1, border_radius=14)
            for cw in clickable_words:
                cw.draw(screen)
            btn_finish_bugs.draw(screen)
            
        elif game_state in ["MECANICA_3", "MECANICA_3_WIN"]:
            title = font_title.render("Correção Ortográfica", True, GOLD)
            screen.blit(title, (40, 65))
            
            text_panel = pygame.Rect(80, 135, WIDTH - 160, HEIGHT - 260)
            pygame.draw.rect(screen, CARD_BG, text_panel, border_radius=14)
            pygame.draw.rect(screen, CARD_BORDER, text_panel, width=1, border_radius=14)
            for cw in clickable_words:
                cw.draw(screen)
                
            if game_state == "MECANICA_3":
                modal_rect = pygame.Rect(WIDTH//2 - 220, HEIGHT//2 - 160, 440, 420)
                draw_modal(screen, modal_rect, GOLD)
                
                bug_word = bugs_to_fix[current_bug_index].clean
                mtitle = font_title.render("Corrigir Palavra", True, GOLD)
                screen.blit(mtitle, (WIDTH//2 - mtitle.get_width()//2, modal_rect.y + 18))
                
                mtext = font_text.render(f"Qual é a forma correta de '{bug_word}'?", True, PARCHMENT)
                screen.blit(mtext, (WIDTH//2 - mtext.get_width()//2, modal_rect.y + 80))
                
                for btn in modal_buttons:
                    btn.draw(screen)
                    
                if current_chapter_index >= 2:
                    input_rect = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 40, 320, 50)
                    pygame.draw.rect(screen, (20, 35, 25), input_rect, border_radius=8)
                    
                    cursor_color = GOLD_LIGHT if (frame_count // 30) % 2 == 0 else GOLD_DIM
                    pygame.draw.rect(screen, cursor_color, input_rect, width=2, border_radius=8)
                    
                    typed_surf = font_btn.render(typed_word, True, PARCHMENT)
                    screen.blit(typed_surf, (input_rect.x + 20, input_rect.y + 10))
                    
                    cursor_x = input_rect.x + 20 + typed_surf.get_width()
                    pygame.draw.line(screen, cursor_color, (cursor_x, input_rect.y + 10), (cursor_x, input_rect.y + 40), 2)
                    
                    hint = font_small.render("Digite a palavra correta e aperte ENTER", True, TEXT_DIM)
                    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, input_rect.bottom + 20))
                
        elif game_state in ["MECANICA_4", "MECANICA_4_WIN"]:
            title = font_title.render("Mapa de Padrões", True, GOLD)
            screen.blit(title, (40, 65))
            
            panel = pygame.Rect(WIDTH//2 - 300, 140, 600, 100)
            pygame.draw.rect(screen, CARD_BG, panel, border_radius=12)
            pygame.draw.rect(screen, CARD_BORDER, panel, width=1, border_radius=12)
            
            q_surf = font_btn.render("Qual padrão de erro ortográfico predominou nesta lenda?", True, PARCHMENT)
            screen.blit(q_surf, (WIDTH//2 - q_surf.get_width()//2, panel.y + 35))
            
            if game_state == "MECANICA_4":
                for btn in mec4_buttons:
                    btn.draw(screen)
                    
        elif game_state == "MECANICA_5":
            # Livro Animado
            title = font_title.render("A Lenda Restaurada", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
            
            book_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
            draw_parchment(screen, book_rect)
            
            chapter = CHAPTERS_DATA[current_chapter_index]
            full_text = ""
            for pid in saved_order:
                pdata = next(p for p in chapter["paragraphs"] if p["id"] == pid)
                full_text += pdata["text"] + "\n\n"
                
            chars_to_show = (frame_count - m5_start_frame) // 2
            display_text = full_text[:chars_to_show]
            
            y_offset = book_rect.y + 30
            paragraphs = display_text.split("\n\n")
            for p in paragraphs:
                if not p: continue
                lines = wrap_text(p, font_text, book_rect.w - 60)
                for line in lines:
                    tsurf = font_text.render(line, True, (60, 40, 20))
                    screen.blit(tsurf, (book_rect.x + 30, y_offset))
                    y_offset += 28
                y_offset += 15
                
            if chars_to_show > len(full_text):
                btn_finish_book.draw(screen)
            
        elif game_state == "FIM":
            # Chuva de partículas douradas
            for vp in victory_particles:
                vp.update()
                vp.draw(screen)
            
            title = font_mega.render("Parabéns, Guardião!", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            # Linha ornamental
            pygame.draw.line(screen, GOLD_DIM, (WIDTH//2 - 200, 175), (WIDTH//2 + 200, 175), 1)
            pygame.draw.circle(screen, GOLD, (WIDTH//2, 175), 4)
            
            score_text = font_title.render(f"Pontos Totais: {score}", True, ACCENT_ORANGE)
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
            
            final_msg = font_text.render("Você restaurou a Lenda do Guaraná e mapeou os padrões ortográficos!", True, TEXT_COLOR)
            screen.blit(final_msg, (WIDTH//2 - final_msg.get_width()//2, 260))
            
            # Lenda restaurada como "livro"
            book_rect = pygame.Rect(WIDTH//2 - 420, 310, 840, 280)
            draw_parchment(screen, book_rect)
            
            book_title = font_btn.render("Lenda do Guaraná - Restaurada", True, FOREST_DARK)
            screen.blit(book_title, (WIDTH//2 - book_title.get_width()//2, 330))
            
            start_x = book_rect.x + 30
            start_y_t = 370
            curr_x, curr_y = start_x, start_y_t
            max_w = book_rect.x + book_rect.width - 30
            
            for cw in clickable_words:
                if curr_x + cw.surf.get_width() > max_w:
                    curr_x = start_x
                    curr_y += 28
                col = FOREST_DARK if not cw.corrected else FOREST
                tsurf = font_text.render(cw.text, True, col)
                screen.blit(tsurf, (curr_x, curr_y))
                curr_x += tsurf.get_width() + 5
                
            btn_back_roadmap.draw(screen)

        # Mensagens Globais
        if message_timer > 0:
            is_bad = "incorreta" in message or "marcou" in message or "-1" in message or "não está certa" in message
            is_advancing = "Avançando" in message
            
            if is_advancing:
                msg_surf = font_subtitle.render(message, True, GOLD_LIGHT)
                m_width = msg_surf.get_width() + 80
                m_height = 180
                modal_rect = pygame.Rect(WIDTH//2 - m_width//2, HEIGHT//2 - m_height//2, m_width, m_height)
                draw_modal(screen, modal_rect, GOLD)
                
                mtitle = font_mega.render("MUITO BEM!", True, GOLD)
                screen.blit(mtitle, (WIDTH//2 - mtitle.get_width()//2, modal_rect.y + 35))
                
                screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, modal_rect.y + 110))
            else:
                msg_surf = font_text.render(message, True, (255, 255, 255))
                msg_rect = msg_surf.get_rect(center=(WIDTH//2, HEIGHT - 40))
                bg_rect = msg_rect.inflate(24, 12)
                
                msg_col = DANGER if is_bad else FOREST
                
                pygame.draw.rect(screen, (0,0,0), bg_rect.move(2,3), border_radius=8)
                pygame.draw.rect(screen, msg_col, bg_rect, border_radius=8)
                pygame.draw.rect(screen, GOLD_DIM if not is_bad else DANGER_LIGHT, bg_rect, width=1, border_radius=8)
                screen.blit(msg_surf, msg_rect)
                
            message_timer -= 1
        
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
