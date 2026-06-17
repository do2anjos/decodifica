import asyncio
import pygame
import sys
import re
import math
import random
try:
    import threading
except ImportError:
    threading = None

pyttsx3 = None
import array as arr_module
import json
import os
from data import *
from ui import *

# Inicializa o Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
if hasattr(pygame.key, 'start_text_input'):
    pygame.key.start_text_input()

# Task 11: Resolução 16:9
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DECODIFICA: Guardiões das Lendas")

# Task 1: Paleta Amazônica
# Task 2: Fontes e Tipografia
def generate_tone(frequency, duration_ms, volume=0.25, fade_out=True):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = arr_module.array('h')
    max_amp = int(32767 * volume)
    for i in range(n_samples):
        t = i / sample_rate
        fade = max(0.0, 1.0 - (i / n_samples)) if fade_out else 1.0
        val = int(max_amp * math.sin(2 * math.pi * frequency * t) * fade)
        buf.append(val)  # left
        buf.append(val)  # right
    return pygame.mixer.Sound(buffer=buf)

try:
    # Som de acerto: duas notas ascendentes (Dó → Mi)
    tone1 = generate_tone(523, 120, 0.2)
    tone2 = generate_tone(659, 180, 0.25)
    # Combinar em um único buffer
    buf_success = arr_module.array('h')
    buf_success.extend(tone1.get_raw())
    buf_success.extend(tone2.get_raw())
    snd_success = pygame.mixer.Sound(buffer=buf_success)
    
    # Som de erro: nota grave descendente
    snd_error = generate_tone(220, 250, 0.18)
except Exception:
    snd_success = None
    snd_error = None

def play_sound(sound):
    if sound:
        try: sound.play()
        except Exception: pass
font_title = pygame.font.SysFont("georgia", 42, bold=True)
# Dados dos Capítulos

# --- Estado Global ---
game_state = "MENU"
lives = 3
score = 0
player_name = ""
leaderboard_data = []
leaderboard_status = "loading"
message = ""
message_timer = 0
frame_count = 0
current_chapter_index = 0
unlocked_chapters = 1
typed_word = ""
lupa_active = False
state_before_gameover = ""
collected_fragments = []
fragment_reveal_timer = 0
fragment_reveal_text = ""
insignias_decomposicao = 0
insignias_abstracao = 0
chapter_start_time = 0
m4_start_time = 0
current_fakes_count = 0
student_explanation = ""

# --- Métricas de Aprendizagem (Teacher Dashboard) ---
learning_metrics = []

def export_learning_metrics(chapter_name, real_bugs, fakes, total_bugs, score_gained, time_spent):
    recall = real_bugs / total_bugs if total_bugs > 0 else 0
    precision = real_bugs / (real_bugs + fakes) if (real_bugs + fakes) > 0 else 0
    metric = {
        "chapter": chapter_name,
        "found_bugs": real_bugs,
        "false_positives": fakes,
        "total_bugs": total_bugs,
        "recall_percent": round(recall * 100, 1),
        "precision_percent": round(precision * 100, 1),
        "score_gained": score_gained,
        "time_spent_seconds": round(time_spent, 1)
    }
    learning_metrics.append(metric)
    try:
        with open("teacher_dashboard_log.json", "w", encoding="utf-8") as f:
            json.dump(learning_metrics, f, indent=4, ensure_ascii=False)
    except Exception:
        pass

def update_m4_metrics(m4_time_spent):
    if len(learning_metrics) > 0:
        learning_metrics[-1]["m4_time_spent_seconds"] = round(m4_time_spent, 1)
        try:
            with open("teacher_dashboard_log.json", "w", encoding="utf-8") as f:
                import json
                json.dump(learning_metrics, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

# --- Modo Criador de Lendas ---
creator_lines = [""]
creator_bugs = {}
creator_active_word = None
creator_input_error = ""
creator_words_cache = []

def show_msg(msg, duration=120):
    global message, message_timer
    message = msg
    message_timer = duration

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

# --- Inicialização do TTS (Text-to-Speech) ---
try:
    if sys.platform == 'emscripten':
        tts_engine = None
    elif pyttsx3:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 150)
    else:
        tts_engine = None
except Exception as e:
    tts_engine = None
    print(f"Aviso: Não foi possível carregar o TTS. {e}")

def speak_word_thread(word):
    if tts_engine:
        try:
            tts_engine.say(word)
            tts_engine.runAndWait()
        except Exception:
            pass

def play_phonetic_feedback(word):
    """Executa a fala da palavra correta em uma thread separada para não travar o jogo."""
    try:
        if threading:
            threading.Thread(target=speak_word_thread, args=(word,), daemon=True).start()
        else:
            speak_word_thread(word)
    except Exception as e:
        print(f"Erro no TTS (ignorado na Web): {e}")

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

# --- Classes ---
# Botões
btn_play_menu = Button(WIDTH//2 - 140, HEIGHT//2 + 60, 280, 55, "Iniciar Aventura", FOREST_DARK, GOLD_LIGHT)
btn_next_intro = Button(WIDTH//2 - 110, HEIGHT - 110, 220, 50, "Entendi!", FOREST_DARK, GOLD_LIGHT)
btn_check = Button(WIDTH//2 - 120, HEIGHT - 85, 240, 52, "Verificar Ordem", FOREST_DARK, GOLD_LIGHT)
btn_finish_bugs = Button(WIDTH//2 - 120, HEIGHT - 85, 240, 52, "Terminei a Busca", FOREST_DARK, GOLD_LIGHT)
btn_back_roadmap = Button(WIDTH//2 - 140, HEIGHT - 100, 280, 55, "Voltar ao Mapa", FOREST_DARK, GOLD_LIGHT)

btn_skip_cine = Button(WIDTH - 160, HEIGHT - 60, 130, 40, "Pular >>", (60, 60, 60), (200, 200, 200))
btn_start_mission = Button(WIDTH//2 - 140, HEIGHT//2 + 50, 280, 55, "Assumir Missão", DANGER, GOLD_LIGHT)
btn_finish_book = Button(WIDTH//2 - 120, HEIGHT - 85, 240, 52, "Concluir Lenda", FOREST_DARK, GOLD_LIGHT)
btn_lupa = Button(WIDTH - 150, 10, 130, 35, "Lupa (L)", FOREST_DARK, GOLD_LIGHT)
btn_voltar = Button(WIDTH - 150, 60, 130, 35, "< Voltar", FOREST_DARK, GOLD_LIGHT)
btn_ranking_menu = Button(WIDTH//2 - 140, HEIGHT//2 + 130, 280, 55, "Ver Ranking", FOREST, GOLD_LIGHT)
btn_confirm_name = Button(WIDTH//2 - 100, HEIGHT//2 + 80, 200, 50, "Confirmar", FOREST_DARK, GOLD_LIGHT)
btn_voltar_menu = Button(WIDTH//2 - 100, HEIGHT - 80, 200, 50, "Voltar", FOREST_DARK, GOLD_LIGHT)
btn_voltar_intro = Button(WIDTH//2 - 230, HEIGHT - 120, 220, 50, "Voltar", FOREST_DARK, GOLD_LIGHT)
btn_retry = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Tentar Novamente", DANGER, GOLD_LIGHT)
btn_galeria = Button(WIDTH - 200, HEIGHT - 70, 180, 50, "Galeria de Arte", FOREST_DARK, GOLD_LIGHT)

btn_creator = Button(WIDTH//2 - 120, HEIGHT - 70, 240, 50, "Criar Lenda Bônus", DANGER, GOLD_LIGHT)
btn_creator_next = Button(WIDTH - 250, HEIGHT - 80, 200, 50, "Pronto! Avançar", FOREST, GOLD_LIGHT)
btn_creator_play = Button(WIDTH//2 - 120, HEIGHT - 80, 240, 50, "Salvar e Jogar!", GOLD, (20,20,20))
btn_voltar_menu_principal = Button(20, 20, 150, 40, "< Menu", FOREST_DARK, GOLD_LIGHT)
btn_ready_tutorial = Button(WIDTH//2 + 10, HEIGHT - 120, 220, 50, "Estou Pronto!", FOREST, GOLD_LIGHT)

all_buttons = [btn_play_menu, btn_next_intro, btn_check, btn_finish_bugs, btn_back_roadmap, btn_skip_cine, btn_start_mission, btn_finish_book, btn_lupa, btn_voltar, btn_retry, btn_galeria, btn_creator, btn_creator_next, btn_creator_play, btn_ranking_menu, btn_confirm_name, btn_voltar_menu, btn_voltar_intro, btn_voltar_menu_principal, btn_ready_tutorial]

async def fetch_leaderboard_task():
    global leaderboard_status, leaderboard_data
    try:
        import js
        import json
        resp = await js.fetch("/api/leaderboard")
        text = await resp.text()
        leaderboard_data = json.loads(text)
        leaderboard_status = "loaded"
    except Exception as e:
        print("Erro fetch leaderboard", e)
        leaderboard_status = "error"

def fetch_leaderboard():
    global leaderboard_status
    leaderboard_status = "loading"
    asyncio.create_task(fetch_leaderboard_task())

def submit_score():
    try:
        import js
        import json
        opts = js.Object.new()
        opts.method = "POST"
        headers = js.Object.new()
        headers["Content-Type"] = "application/json"
        opts.headers = headers
        
        payload = {
            "nome": player_name,
            "pontos": score,
            "vidas": lives,
            "insignias_d": insignias_decomposicao,
            "insignias_a": insignias_abstracao
        }
        opts.body = json.dumps(payload)
        js.fetch("/api/score", opts)
    except Exception:
        pass

def setup_mecanica_1():
    global cards, chapter_start_time
    chapter_start_time = pygame.time.get_ticks()
    cards = []
    start_y = 100
    chapter = CHAPTERS_DATA[current_chapter_index]
    num_cards = len(chapter["paragraphs"])
    
    # Ajustar tamanho e espaçamento dependendo da quantidade (até 6 cartas)
    card_h = 95
    y_inc = 95
    
    for i, p in enumerate(chapter["paragraphs"]):
        cards.append(DraggableCard(20, start_y, 540, card_h, p["id"], p["text"]))
        start_y += y_inc

def setup_mecanica_2(ordered_ids):
    global clickable_words, bugs_to_fix, chapter_start_time, current_fakes_count
    current_fakes_count = 0
    if game_state == "CREATOR_WRITE":
        chapter_start_time = pygame.time.get_ticks() # Reinicia se for criador
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
            cw = ClickableWord(w, current_x, current_y)
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
        btn = Button(WIDTH//2 - 160, start_y, 320, 48, op, CARD_BG, FOREST_DARK)
        btn.is_correct = (op == chapter_bugs[bug_cw.clean]["correto"])
        modal_buttons.append(btn)
        all_buttons.append(btn)
        start_y += 62

def setup_mecanica_4():
    global mec4_buttons, m4_start_time
    m4_start_time = pygame.time.get_ticks()
    mec4_buttons = []
    start_y = HEIGHT//2 - 40
    opcoes = CHAPTERS_DATA[current_chapter_index]["mec4_options"]
    for txt, correct in opcoes:
        btn = Button(WIDTH//2 - 160, start_y, 320, 48, txt, CARD_BG, FOREST_DARK)
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
        
    order = [c.para_id for c in cards_in_zone]
    
    if order == correct:
        show_msg("A lenda faz sentido! Avançando...", 120)
        play_sound(snd_success)
        saved_order = order
        # Bônus: Insígnia de Decomposição
        global insignias_decomposicao
        if game_state == "MECANICA_1": insignias_decomposicao += 1
        game_state = "MECANICA_1_WIN"
    else:
        if len(order) > len(correct):
            show_msg("Há um parágrafo intruso! Jogue-o na Lixeira.", 180)
        else:
            show_msg("A ordem não faz sentido. Lembre-se: uma história precisa de Início, Meio e Fim.", 240)
            play_sound(snd_error)

def check_bugs():
    global game_state, score, lives, current_fakes_count
    marked_words = [cw for cw in clickable_words if cw.marked]
    if not marked_words:
        show_msg("Clique nas palavras com erro ortográfico para marcá-las.", 180)
        return
    real_bugs = 0
    chapter_bugs = CHAPTERS_DATA[current_chapter_index]["bugs"]
    for cw in marked_words:
        if cw.clean in chapter_bugs.keys():
            real_bugs += 1
        else:
            cw.marked = False
            
    min_bugs = math.ceil(len(chapter_bugs) * 0.7)
    
    if real_bugs >= min_bugs:
        score += 100
        if real_bugs == len(chapter_bugs):
            show_msg("Todos os bugs encontrados! Hora de corrigir.", 120)
        else:
            show_msg(f"Excelente! Encontrou {real_bugs} bugs (meta: {min_bugs}). Hora de corrigir.", 120)
        play_sound(snd_success)
        # Bônus: Insígnia de Abstração se não marcou fakes
        global insignias_abstracao
        if game_state == "MECANICA_2" and current_fakes_count == 0:  # Garante que só ganha 1 vez sem errar fakes
            insignias_abstracao += 1
            
        time_spent = (pygame.time.get_ticks() - chapter_start_time) / 1000.0
        export_learning_metrics(CHAPTERS_DATA[current_chapter_index]["name"], real_bugs, current_fakes_count, len(chapter_bugs), 100, time_spent)
        game_state = "MECANICA_2_WIN"
    else:
        show_msg(f"Faltam bugs... Encontrou {real_bugs} (Meta: {min_bugs}).", 180)


def compile_custom_legend():
    global game_state, current_chapter_index, unlocked_chapters, lives
    import re
    # Remover lenda customizada anterior se existir
    if len(CHAPTERS_DATA) > 4:
        CHAPTERS_DATA.pop()
    
    paragraphs = []
    for i, line in enumerate(creator_lines):
        if not line.strip(): continue
        final_line = line
        for bug_real, bug_data in creator_bugs.items():
            final_line = re.sub(r'\b' + bug_real + r'\b', bug_data["opcoes"][1], final_line, flags=re.IGNORECASE)
        paragraphs.append({"id": str(i), "text": final_line})
    
    if not paragraphs: return
        
    custom_chapter = {
        "name": "Cap. Bônus: Lenda Customizada",
        "rank": "Criador",
        "color": (150, 50, 200),
        "paragraphs": paragraphs,
        "correct_order": [str(i) for i in range(len(paragraphs))],
        "bugs": creator_bugs,
        "mec4_options": [
            ("Padrão Personalizado", True),
            ("Nenhum padrão", False)
        ]
    }
    
    CHAPTERS_DATA.append(custom_chapter)
    current_chapter_index = len(CHAPTERS_DATA) - 1
    unlocked_chapters = len(CHAPTERS_DATA)
    lives = 3
    
    # Inicia direto na M2
    setup_mecanica_2([str(i) for i in range(len(paragraphs))])
    game_state = "MECANICA_2"

def snap_cards():
    cards_in_zone = [c for c in cards if c.rect.centerx > 600 and c.rect.centery < HEIGHT - 90]
    cards_in_zone.sort(key=lambda c: c.rect.y)
    start_y = 110
    for c in cards_in_zone:
        c.rect.x = 610
        c.rect.y = start_y
        start_y += 100

async def main():
    global game_state, message_timer, current_bug_index, score, lives, frame_count
    global current_chapter_index, unlocked_chapters, typed_word, active_card, m5_start_frame, state_before_gameover, lupa_active
    global collected_fragments, fragment_reveal_timer, fragment_reveal_text, current_fakes_count
    global cinematic_slide, cinematic_timer, player_name, leaderboard_status, leaderboard_data, student_explanation
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
                if game_state not in ["MENU", "CINEMATIC", "INTRO", "ROADMAP", "FIM", "NAME_INPUT", "RANKING", "CHAPTER_INTRO"]:
                    if btn_lupa.is_clicked(event.pos):
                        lupa_active = not lupa_active
                    if btn_voltar.is_clicked(event.pos):
                        game_state = "ROADMAP"
                if game_state == "MENU":
                    if btn_play_menu.is_clicked(event.pos):
                        game_state = "NAME_INPUT"
                    if btn_ranking_menu.is_clicked(event.pos):
                        fetch_leaderboard()
                        game_state = "RANKING"
                elif game_state == "NAME_INPUT":
                    if btn_confirm_name.is_clicked(event.pos) and len(player_name.strip()) > 0:
                        game_state = "CINEMATIC"
                        cinematic_slide, cinematic_timer = 0, 0
                    elif btn_voltar_menu_principal.is_clicked(event.pos):
                        game_state = "MENU"
                elif game_state == "RANKING":
                    if btn_voltar_menu.is_clicked(event.pos):
                        game_state = "MENU"
                elif game_state == "CINEMATIC":
                    if btn_skip_cine.is_clicked(event.pos) and cinematic_slide < 3:
                        game_state = "ROADMAP"
                    elif cinematic_slide == 3 and btn_start_mission.is_clicked(event.pos):
                        game_state = "ROADMAP"
                elif game_state == "CHAPTER_INTRO":
                    if btn_ready_tutorial.is_clicked(event.pos):
                        setup_mecanica_1()
                        game_state = "MECANICA_1"
                    elif btn_voltar_intro.is_clicked(event.pos):
                        game_state = "ROADMAP"
                elif game_state == "ROADMAP":
                    if btn_voltar_menu_principal.is_clicked(event.pos):
                        game_state = "MENU"
                    elif btn_galeria.is_clicked(event.pos):
                        game_state = "GALERIA"
                    elif unlocked_chapters >= 4 and btn_creator.is_clicked(event.pos):
                        global creator_lines, creator_bugs, creator_active_word, creator_input_error
                        creator_lines = [""]
                        creator_bugs = {}
                        creator_active_word = None
                        creator_input_error = ""
                        game_state = "CREATOR_WRITE"
                    for btn in roadmap_buttons:
                        if btn.is_clicked(event.pos):
                            current_chapter_index = btn.chapter_index
                            lives = 3
                            game_state = "CHAPTER_INTRO"
                elif game_state == "GAME_OVER":
                    if btn_retry.is_clicked(event.pos):
                        lives = 3
                        game_state = state_before_gameover
                        if game_state in ["MECANICA_1", "MECANICA_1_WIN"]: 
                            setup_mecanica_1()
                            game_state = "MECANICA_1"
                        elif game_state in ["MECANICA_3", "MECANICA_3_WIN"]:
                            current_bug_index = 0; typed_word = ""
                            for cw in bugs_to_fix: 
                                cw.corrected = False
                                cw.set_text(cw.clean)
                            create_modal_buttons()
                            game_state = "MECANICA_3"
                        elif game_state in ["MECANICA_4", "MECANICA_4_WIN"]: 
                            setup_mecanica_4()
                            game_state = "MECANICA_4"
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
                elif game_state == "CREATOR_WRITE":
                    if btn_creator_next.is_clicked(event.pos):
                        if any(len(line.strip()) > 0 for line in creator_lines):
                            # Cache as palavras para clicar na próxima tela
                            global creator_words_cache
                            creator_words_cache = []
                            full_text = " ".join(creator_lines)
                            words = full_text.split()
                            wx, wy = 60, 200
                            for w in words:
                                cw = ClickableWord(w, wx, wy)
                                if cw.rect.right > WIDTH - 60:
                                    wx = 60
                                    wy += 40
                                    cw = ClickableWord(w, wx, wy)
                                creator_words_cache.append(cw)
                                wx += cw.rect.width + 6
                            game_state = "CREATOR_CORRUPT"
                elif game_state == "CREATOR_CORRUPT":
                    if btn_creator_play.is_clicked(event.pos):
                        compile_custom_legend()
                    elif not creator_active_word:
                        for cw in creator_words_cache:
                            if cw.rect.collidepoint(event.pos):
                                creator_active_word = cw.clean
                                creator_input_error = ""
                                break
                elif game_state == "MECANICA_2":
                    if btn_finish_bugs.is_clicked(event.pos): check_bugs()
                    else:
                        for cw in clickable_words:
                            if cw.rect.collidepoint(event.pos):
                                if not cw.marked:
                                    chapter_bugs = CHAPTERS_DATA[current_chapter_index]["bugs"]
                                    if cw.clean in chapter_bugs.keys():
                                        cw.marked = True
                                        play_sound(snd_success)
                                    else:
                                        score -= 5
                                        current_fakes_count += 1
                                        show_msg("Palavra correta! Falso positivo (-5 pts)", 90)
                                        play_sound(snd_error)
                                else:
                                    cw.marked = False
                                break
                elif game_state == "MECANICA_3":
                    for btn in modal_buttons:
                        if btn.is_clicked(event.pos):
                            if btn.is_correct:
                                score += 20; show_msg("Ortografia correta! +20 pts", 90)
                                play_sound(snd_success)
                                cw = bugs_to_fix[current_bug_index]
                                cw.marked = False; cw.corrected = True
                                cw.set_text(cw.text.replace(cw.clean, btn.text))
                                current_bug_index += 1
                                if current_bug_index >= len(bugs_to_fix): game_state = "MECANICA_3_WIN"
                                else: create_modal_buttons()
                            else: 
                                bug_cw = bugs_to_fix[current_bug_index]
                                correct_word = CHAPTERS_DATA[current_chapter_index]["bugs"][bug_cw.clean]["correto"]
                                play_phonetic_feedback(correct_word)
                                show_msg("Grafia incorreta! Reveja a regra ortográfica dessa palavra.", 240)
                                play_sound(snd_error)
                            break
                elif game_state == "MECANICA_4" and any(btn.is_clicked(event.pos) for btn in mec4_buttons):
                    for btn in mec4_buttons:
                        if btn.is_clicked(event.pos):
                            if btn.is_correct: 
                                score += 150
                                m4_time_spent = (pygame.time.get_ticks() - m4_start_time) / 1000.0
                                update_m4_metrics(m4_time_spent)
                                # Coletar fragmento do Mapa de Padrões
                                fragment_name = btn.text
                                if current_chapter_index not in [f["chapter"] for f in collected_fragments]:
                                    collected_fragments.append({"chapter": current_chapter_index, "rule": fragment_name, "legend": CHAPTERS_DATA[current_chapter_index]["name"]})
                                fragment_reveal_text = fragment_name
                                fragment_reveal_timer = 180
                                show_msg("Padrão identificado! +150 pts. Fragmento coletado!", 120)
                                play_sound(snd_success)
                                game_state = "MECANICA_4_WIN"
                            else: 
                                show_msg("Incorreto. Observe bem as palavras que você corrigiu para inferir a regra geral.", 240)
                                play_sound(snd_error)
                elif game_state == "MECANICA_5" and btn_finish_book.is_clicked(event.pos):
                    submit_score()
                    game_state = "ROADMAP"
                    if current_chapter_index == 0: unlocked_chapters = max(unlocked_chapters, 2)
                    elif current_chapter_index == 1: unlocked_chapters = max(unlocked_chapters, 3)
                    elif current_chapter_index == 2: unlocked_chapters = max(unlocked_chapters, 4)
                elif game_state in ["FIM", "GALERIA"] and btn_back_roadmap.is_clicked(event.pos):
                    if game_state == "FIM":
                        if current_chapter_index + 1 == unlocked_chapters and unlocked_chapters < len(CHAPTERS_DATA):
                            unlocked_chapters += 1
                    game_state = "ROADMAP"
                            
            if event.type == pygame.TEXTINPUT:
                if game_state == "NAME_INPUT":
                    if len(player_name) < 15:
                        player_name += event.text
                elif game_state == "MECANICA_4_EXPLAIN":
                    if len(student_explanation) < 300:
                        student_explanation += event.text
                elif game_state == "MECANICA_3" and current_chapter_index >= 2:
                    if len(typed_word) < 20: 
                        typed_word += event.text
                elif game_state == "CREATOR_WRITE":
                    if len(creator_lines[-1]) < 80:
                        creator_lines[-1] += event.text
                elif game_state == "CREATOR_CORRUPT" and creator_active_word:
                    if len(creator_input_error) < 20:
                        creator_input_error += event.text

            if event.type == pygame.KEYDOWN:
                if game_state == "NAME_INPUT":
                    if event.key == pygame.K_RETURN:
                        if len(player_name.strip()) > 0:
                            game_state = "CINEMATIC"
                            cinematic_slide, cinematic_timer = 0, 0
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                elif game_state == "CINEMATIC":
                    if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                        game_state = "ROADMAP"
                elif game_state == "MECANICA_4_EXPLAIN":
                    if event.key == pygame.K_RETURN:
                        if len(student_explanation.strip()) >= 10:
                            show_msg("Síntese registrada com sucesso! Avançando...", 120)
                            global m5_start_frame
                            m5_start_frame = frame_count
                            game_state = "MECANICA_5"
                        else:
                            show_msg("Por favor, escreva uma explicação mais detalhada.", 120)
                    elif event.key == pygame.K_BACKSPACE:
                        student_explanation = student_explanation[:-1]
                elif game_state == "MECANICA_3" and current_chapter_index >= 2:
                    if event.key == pygame.K_BACKSPACE: typed_word = typed_word[:-1]
                    elif event.key == pygame.K_RETURN:
                        try:
                            bug_cw = bugs_to_fix[current_bug_index]
                            correct_word = CHAPTERS_DATA[current_chapter_index]["bugs"][bug_cw.clean]["correto"]
                            if typed_word.strip().lower() == correct_word.lower():
                                score += 40; show_msg("Ortografia perfeita! +40 pts", 90)
                                play_sound(snd_success)
                                cw = bugs_to_fix[current_bug_index]
                                cw.marked = False; cw.corrected = True
                                cw.set_text(cw.text.replace(cw.clean, correct_word))
                                current_bug_index += 1; typed_word = ""
                                if current_bug_index >= len(bugs_to_fix): game_state = "MECANICA_3_WIN"
                            else: 
                                play_phonetic_feedback(correct_word)
                                show_msg("Grafia incorreta! Reveja a regra ortográfica dessa palavra.", 240)
                                play_sound(snd_error)
                        except Exception as err:
                            print(f"CRITICAL ERROR on K_RETURN: {err}")
                            show_msg("Erro interno! Veja o Console F12.", 180)
                
            if event.type == pygame.KEYDOWN and game_state == "CREATOR_WRITE":
                if event.key == pygame.K_BACKSPACE:
                    if len(creator_lines[-1]) > 0:
                        creator_lines[-1] = creator_lines[-1][:-1]
                    elif len(creator_lines) > 1:
                        creator_lines.pop()
                elif event.key == pygame.K_RETURN:
                    if len(creator_lines) < 8:
                        creator_lines.append("")
                        
            if event.type == pygame.KEYDOWN and game_state == "CREATOR_CORRUPT" and creator_active_word:
                if event.key == pygame.K_BACKSPACE:
                    creator_input_error = creator_input_error[:-1]
                elif event.key == pygame.K_RETURN and len(creator_input_error.strip()) > 0:
                    creator_bugs[creator_active_word] = {
                        "correto": creator_active_word,
                        "opcoes": [creator_active_word, creator_input_error, creator_input_error + "s"]
                    }
                    creator_active_word = None
                            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and active_card:
                active_card.dragging = False; active_card = None

        if message_timer <= 0:
            if game_state == "MECANICA_1_WIN": setup_mecanica_2(saved_order); game_state = "MECANICA_2"
            elif game_state == "MECANICA_2_WIN": setup_mecanica_3(); game_state = "MECANICA_3"
            elif game_state == "MECANICA_3_WIN":
                if current_chapter_index == 0:
                    # Cap 1 (Aprendiz): pula M4, vai direto para o Livro Animado
                    m5_start_frame = frame_count; game_state = "MECANICA_5"
                else:
                    setup_mecanica_4(); game_state = "MECANICA_4"
            elif game_state == "MECANICA_4_WIN":
                if fragment_reveal_timer > 0:
                    pass  # aguarda a animação de fragmento terminar
                else:
                    student_explanation = ""
                    game_state = "MECANICA_4_EXPLAIN"

        if game_state == "CINEMATIC" and cinematic_slide == 2: screen.blit(bg_surface_glitch, (0, 0))
        else: screen.blit(bg_surface, (0, 0))
            
        draw_fireflies(screen)
        if game_state not in ["MENU", "CINEMATIC", "INTRO", "ROADMAP", "FIM", "GALERIA", "CREATOR_WRITE", "CREATOR_PLAY", "NAME_INPUT", "RANKING", "CHAPTER_INTRO"]:
            draw_hud(screen, score, insignias_decomposicao, insignias_abstracao, btn_lupa)
            btn_voltar.draw(screen)
            
        if game_state == "MENU":
            pulse = 0.7 + 0.3 * math.sin(frame_count * 0.03)
            # Create golden title correctly
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
            btn_ranking_menu.draw(screen)
            
        elif game_state == "NAME_INPUT":
            title = font_title.render("Como você quer ser chamado?", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3 - 50))
            
            # Input Box
            input_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//3 + 30, 400, 60)
            pygame.draw.rect(screen, CARD_BG, input_rect, border_radius=8)
            pygame.draw.rect(screen, GOLD_DIM, input_rect, width=2, border_radius=8)
            
            name_surf = font_title.render(player_name + ("_" if frame_count % 60 < 30 else ""), True, TEXT_COLOR)
            screen.blit(name_surf, (input_rect.x + 20, input_rect.y + 10))
            
            if len(player_name.strip()) > 0:
                btn_confirm_name.draw(screen)
            btn_voltar_menu_principal.draw(screen)
                
        elif game_state == "RANKING":
            title = font_mega.render("Hall dos Guardiões", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
            
            if leaderboard_status == "loading":
                lbl = font_title.render("Carregando ranking...", True, TEXT_DIM)
                screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, HEIGHT//2))
            elif leaderboard_status == "error":
                lbl = font_title.render("Erro ao conectar no banco de dados.", True, DANGER_LIGHT)
                screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, HEIGHT//2))
            else:
                sy = 180
                for i, row in enumerate(leaderboard_data):
                    col = GOLD_LIGHT if i == 0 else TEXT_COLOR
                    r_text = f"{i+1}o. {row.get('nome', '???')} - {row.get('pontos', 0)} pts"
                    lbl = font_title.render(r_text, True, col)
                    screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, sy))
                    
                    sub_text = f"Vidas: {row.get('vidas', 0)} | Decomp: {row.get('insignias_d', 0)} | Abst: {row.get('insignias_a', 0)}"
                    lbl_sub = font_small.render(sub_text, True, TEXT_DIM)
                    screen.blit(lbl_sub, (WIDTH//2 - lbl_sub.get_width()//2, sy + 35))
                    
                    sy += 80
            
            btn_voltar_menu.draw(screen)
            
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
                
        elif game_state == "CHAPTER_INTRO":
            parch_rect = pygame.Rect(WIDTH//2 - 400, 70, 800, 500)
            draw_parchment(screen, parch_rect)
            
            ch_name = CHAPTERS_DATA[current_chapter_index]["name"]
            title = font_title.render(f"Missão: {ch_name}", True, FOREST_DARK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            lines = [
                "Você está prestes a restaurar esta lenda amazônica.",
                "",
                "Como funciona sua jornada:",
                "1. Organize as partes da história na sequência correta.",
                "2. Procure por erros ortográficos (Bugs) escondidos.",
                "3. Corrija-os reescrevendo a palavra corretamente.",
                "4. Descubra qual regra de ortografia foi quebrada.",
                "",
                "Atenção: Você tem 3 Vidas. Erros tiram vidas.",
                "Insígnias de Pensamento Computacional:",
                "   - Decomposição: Ganha ao organizar as partes sem errar.",
                "   - Abstração: Ganha ao descobrir o padrão sem dicas.",
                "Dica: Use a Lupa (L) se precisar, mas perderá pontos de bônus."
            ]
            
            y_off = 160
            for i, line in enumerate(lines):
                if "Atenção:" in line: col = DANGER
                elif "Insígnias" in line: col = FOREST
                elif "Dica:" in line: col = (100, 80, 20)
                else: col = (60, 40, 20)  # Dark brown for parchment
                tsurf = font_text.render(line, True, col)
                screen.blit(tsurf, (WIDTH//2 - tsurf.get_width()//2, y_off))
                y_off += 28
                
            btn_ready_tutorial.draw(screen)
            btn_voltar_intro.draw(screen)
            
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
                    pygame.draw.circle(screen, (80,80,80), (80, cy+14), 7, 2)
                
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
            
            btn_galeria.update_hover(mouse_pos)
            btn_galeria.draw(screen)
            btn_voltar_menu_principal.update_hover(mouse_pos)
            btn_voltar_menu_principal.draw(screen)
            
            # --- Mapa de Padrões (Fragmentos Coletados) ---
            if collected_fragments:
                frag_y = 665
                frag_title = font_small.render("Mapa de Padrões:", True, GOLD)
                screen.blit(frag_title, (80, frag_y))
                fx = 80 + frag_title.get_width() + 15
                for frag in collected_fragments:
                    # Ícone de fragmento (losango dourado)
                    pts = [(fx + 10, frag_y + 2), (fx + 20, frag_y + 12), (fx + 10, frag_y + 22), (fx, frag_y + 12)]
                    pygame.draw.polygon(screen, GOLD, pts)
                    pygame.draw.polygon(screen, GOLD_LIGHT, pts, 1)
                    # Tooltip com o nome da regra
                    rule_surf = font_small.render(frag["rule"][:25], True, GOLD_LIGHT)
                    screen.blit(rule_surf, (fx + 25, frag_y + 4))
                    fx += rule_surf.get_width() + 45
                # Fragmentos faltando
                missing = len(CHAPTERS_DATA) - len(collected_fragments)
                if missing > 0:
                    for m in range(missing):
                        pts = [(fx + 10, frag_y + 2), (fx + 20, frag_y + 12), (fx + 10, frag_y + 22), (fx, frag_y + 12)]
                        pygame.draw.polygon(screen, CARD_BORDER, pts)
                        pygame.draw.polygon(screen, (60, 60, 60), pts, 1)
                        miss_surf = font_small.render("???", True, TEXT_DIM)
                        screen.blit(miss_surf, (fx + 25, frag_y + 4))
                        fx += 65
            
            # --- Insígnias (Resumo Roadmap) ---
            ins_y = 665
            ins_x = WIDTH - 650
            ins_title = font_small.render("Insígnias:", True, GOLD)
            screen.blit(ins_title, (ins_x, ins_y))
            # Decomposição
            dx = ins_x + ins_title.get_width() + 20
            pygame.draw.circle(screen, (40, 120, 200), (dx, ins_y + 10), 12)
            pygame.draw.circle(screen, (100, 180, 255), (dx, ins_y + 10), 12, 2)
            td = font_small.render(f"Decomposição: {insignias_decomposicao}", True, (100, 180, 255))
            screen.blit(td, (dx + 18, ins_y))
            # Abstração
            dx += td.get_width() + 35
            pygame.draw.circle(screen, (150, 60, 180), (dx, ins_y + 10), 12)
            pygame.draw.circle(screen, (255, 120, 220), (dx, ins_y + 10), 12, 2)
            ta = font_small.render(f"Abstração: {insignias_abstracao}", True, (255, 120, 220))
            screen.blit(ta, (dx + 18, ins_y))
                        
            btn_galeria.update_hover(mouse_pos)
            btn_galeria.draw(screen)
            
        elif game_state == "GALERIA":
            title = font_title.render("Galeria de Lendas", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
            sub = font_small.render("Artes desbloqueadas das lendas restauradas.", True, TEXT_DIM)
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 100))
            
            restored = [f["chapter"] for f in collected_fragments]
            if unlocked_chapters >= 2 and 0 not in restored:
                restored.append(0)
            
            for i, ch in enumerate(CHAPTERS_DATA):
                # Posição do quadro (grid 2x2)
                col = i % 2
                row = i // 2
                qx = WIDTH//2 - 420 + col * 440
                qy = 135 + row * 240
                q_rect = pygame.Rect(qx, qy, 400, 220)
                
                pygame.draw.rect(screen, CARD_BG, q_rect, border_radius=12)
                pygame.draw.rect(screen, ch["color"] if i in restored else CARD_BORDER, q_rect, width=2, border_radius=12)
                
                name_surf = font_btn.render(ch["name"], True, TEXT_COLOR if i in restored else TEXT_DIM)
                screen.blit(name_surf, (qx + 200 - name_surf.get_width()//2, qy + 180))
                
                # Área da arte
                art_rect = pygame.Rect(qx + 20, qy + 20, 360, 150)
                pygame.draw.rect(screen, (20, 30, 25), art_rect, border_radius=8)
                
                cx, cy = art_rect.centerx, art_rect.centery
                if i in restored:
                    # Arte Procedural
                    if i == 0: # Guaraná
                        for j in range(5):
                            x_off = int(math.cos(j * 1.2) * 40)
                            y_off = int(math.sin(j * 1.2) * 20)
                            pygame.draw.circle(screen, (180, 40, 40), (cx + x_off, cy + y_off), 25)
                            pygame.draw.circle(screen, (255, 255, 255), (cx + x_off, cy + y_off - 5), 10)
                            pygame.draw.circle(screen, (0, 0, 0), (cx + x_off, cy + y_off - 5), 5)
                    elif i == 1: # Mapinguari
                        pygame.draw.circle(screen, (100, 60, 30), (cx, cy), 60)
                        pygame.draw.circle(screen, (255, 255, 255), (cx, cy - 20), 25)
                        pygame.draw.circle(screen, (180, 20, 20), (cx, cy - 20), 10)
                        pygame.draw.ellipse(screen, (40, 10, 10), (cx - 30, cy + 15, 60, 30))
                    elif i == 2: # Cobra Grande
                        for j in range(8):
                            sz = 30 - j * 2
                            x_off = int(math.sin(j * 0.8 + frame_count * 0.05) * 40)
                            pygame.draw.circle(screen, (20, 80, 40), (cx - 100 + j * 30, cy + x_off), sz)
                        eye_y = int(cy + math.sin(frame_count * 0.05) * 40 - 10)
                        pygame.draw.circle(screen, (255, 200, 0), (cx - 110, eye_y), 6)
                        pygame.draw.circle(screen, (255, 200, 0), (cx - 90, eye_y), 6)
                    elif i == 3: # Vitória Régia
                        pygame.draw.circle(screen, (40, 140, 60), (cx, cy), 60)
                        pygame.draw.polygon(screen, (20, 30, 25), [(cx, cy), (cx + 30, cy + 60), (cx - 30, cy + 60)])
                        for j in range(6):
                            ang = j * (math.pi / 3) + frame_count * 0.02
                            fx = int(cx + math.cos(ang) * 15)
                            fy = int(cy + math.sin(ang) * 15)
                            pygame.draw.circle(screen, (255, 150, 200), (fx, fy), 12)
                        pygame.draw.circle(screen, (255, 255, 100), (cx, cy), 8)
                else:
                    # Cadeado
                    pygame.draw.rect(screen, (80,80,80), (cx - 15, cy - 5, 30, 25), border_radius=4)
                    pygame.draw.circle(screen, (80,80,80), (cx, cy - 8), 10, 2)
                    lock_surf = font_small.render("Restaurar Lenda", True, (120,120,120))
                    screen.blit(lock_surf, (cx - lock_surf.get_width()//2, cy + 30))
            
            btn_back_roadmap.update_hover(mouse_pos)
            btn_back_roadmap.draw(screen)

        elif game_state in ["MECANICA_1", "MECANICA_1_WIN"]:
            title = font_title.render("Reorganização Narrativa", True, GOLD)
            screen.blit(title, (40, 65))
            inst = font_small.render("Arraste os parágrafos para a zona à direita, na ordem lógica da lenda.", True, TEXT_DIM)
            screen.blit(inst, (42, 108))
            
            draw_drop_zone(screen)
            
            # Dica visual (Scaffolding) para os capítulos
            if game_state == "MECANICA_1":
                correct_order = CHAPTERS_DATA[current_chapter_index]["correct_order"]
                hint_colors = [(50, 255, 50), (50, 200, 255), (255, 200, 50), (255, 100, 200)]
                # Desenhar slots coloridos no drop zone
                sy = 110
                for i in range(len(correct_order)):
                    c = hint_colors[i % len(hint_colors)]
                    alpha = int(100 + 80 * math.sin(frame_count * 0.05))
                    s_surf = pygame.Surface((WIDTH - 660, 95), pygame.SRCALPHA)
                    pygame.draw.rect(s_surf, (*c, alpha), s_surf.get_rect(), width=3, border_radius=6)
                    screen.blit(s_surf, (610, sy))
                    sy += 100
            
            draw_trash_zone(screen, CHAPTERS_DATA[current_chapter_index])
            for card in cards:
                card.draw(screen)
                if game_state == "MECANICA_1":
                    correct_order = CHAPTERS_DATA[current_chapter_index]["correct_order"]
                    if card.para_id in correct_order:
                        idx = correct_order.index(card.para_id)
                        c = hint_colors[idx % len(hint_colors)]
                        alpha = int(150 + 100 * math.sin(frame_count * 0.1))
                        glow_surf = pygame.Surface((card.rect.w, card.rect.h), pygame.SRCALPHA)
                        pygame.draw.rect(glow_surf, (*c, alpha), glow_surf.get_rect(), width=4, border_radius=6)
                        screen.blit(glow_surf, (card.rect.x, card.rect.y))
                        
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
                if getattr(cw, 'marked', False):
                    pygame.draw.rect(screen, ACCENT_ORANGE, cw.rect.inflate(4, 4), border_radius=4)
                elif cw.rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, (80, 80, 100), cw.rect.inflate(4, 4), border_radius=4)
                cw.draw(screen)
            btn_finish_bugs.draw(screen)
            
        elif game_state in ["MECANICA_3", "MECANICA_3_WIN"]:
            title = font_title.render("Correção Ortográfica", True, GOLD)
            screen.blit(title, (40, 65))
            
            text_panel = pygame.Rect(80, 135, WIDTH - 160, HEIGHT - 260)
            pygame.draw.rect(screen, CARD_BG, text_panel, border_radius=14)
            pygame.draw.rect(screen, CARD_BORDER, text_panel, width=1, border_radius=14)
            for cw in clickable_words:
                if getattr(cw, 'corrected', False):
                    pygame.draw.rect(screen, FOREST, cw.rect.inflate(4, 4), border_radius=4)
                elif getattr(cw, 'marked', False):
                    pygame.draw.rect(screen, ACCENT_ORANGE, cw.rect.inflate(4, 4), border_radius=4)
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
            
            # --- NPC Guardião Digital ---
            gx, gy = 140, 200  # posição central do guardião
            pulse_g = 0.5 + 0.5 * math.sin(frame_count * 0.04)
            
            # Aura brilhante atrás do guardião
            aura_surf = pygame.Surface((200, 280), pygame.SRCALPHA)
            aura_alpha = int(30 + 25 * pulse_g)
            pygame.draw.ellipse(aura_surf, (*GOLD, aura_alpha), (10, 20, 180, 250))
            screen.blit(aura_surf, (gx - 100, gy - 80))
            
            # Corpo / Manto (triângulo largo)
            body_pts = [(gx, gy - 55), (gx - 50, gy + 100), (gx + 50, gy + 100)]
            pygame.draw.polygon(screen, FOREST_DARK, body_pts)
            pygame.draw.polygon(screen, FOREST, body_pts, 2)
            
            # Capuz (arco sobre a cabeça)
            # Capuz (elipse já cobre)
            pygame.draw.ellipse(screen, FOREST_DARK, (gx - 30, gy - 85, 60, 50))
            pygame.draw.ellipse(screen, FOREST, (gx - 30, gy - 85, 60, 50), 2)
            
            # Rosto (oval escuro dentro do capuz)
            pygame.draw.ellipse(screen, (15, 10, 8), (gx - 18, gy - 72, 36, 40))
            
            # Olhos brilhantes
            eye_color = (int(200 + 55 * pulse_g), int(160 + 50 * pulse_g), 30)
            pygame.draw.circle(screen, eye_color, (gx - 7, gy - 55), 4)
            pygame.draw.circle(screen, eye_color, (gx + 7, gy - 55), 4)
            # Reflexo dos olhos
            pygame.draw.circle(screen, (255, 255, 200), (gx - 6, gy - 56), 1)
            pygame.draw.circle(screen, (255, 255, 200), (gx + 8, gy - 56), 1)
            
            # Cajado (linha vertical com cristal no topo)
            pygame.draw.line(screen, GOLD_DIM, (gx + 55, gy - 60), (gx + 55, gy + 100), 3)
            # Cristal no topo do cajado
            crystal_glow = int(180 + 75 * pulse_g)
            crystal_color = (crystal_glow, int(crystal_glow * 0.8), 20)
            crystal_pts = [(gx + 55, gy - 80), (gx + 48, gy - 62), (gx + 55, gy - 55), (gx + 62, gy - 62)]
            pygame.draw.polygon(screen, crystal_color, crystal_pts)
            pygame.draw.polygon(screen, GOLD_LIGHT, crystal_pts, 1)
            
            # Detalhes do manto (linhas decorativas)
            pygame.draw.line(screen, GOLD_DIM, (gx - 15, gy + 20), (gx + 15, gy + 20), 1)
            pygame.draw.line(screen, GOLD_DIM, (gx - 20, gy + 40), (gx + 20, gy + 40), 1)
            pygame.draw.line(screen, GOLD_DIM, (gx - 25, gy + 60), (gx + 25, gy + 60), 1)
            
            # Nome do NPC
            npc_name = font_small.render("Guardião Digital", True, GOLD_LIGHT)
            screen.blit(npc_name, (gx - npc_name.get_width()//2, gy + 110))
            
            # Balão de fala (conectado ao guardião)
            balloon = pygame.Rect(280, 140, WIDTH - 340, 100)
            pygame.draw.rect(screen, CARD_BG, balloon, border_radius=12)
            pygame.draw.rect(screen, GOLD_DIM, balloon, width=1, border_radius=12)
            # Seta do balão apontando para o guardião
            arrow_pts = [(280, 180), (250, 195), (280, 200)]
            pygame.draw.polygon(screen, CARD_BG, arrow_pts)
            pygame.draw.line(screen, GOLD_DIM, arrow_pts[0], arrow_pts[1], 1)
            pygame.draw.line(screen, GOLD_DIM, arrow_pts[1], arrow_pts[2], 1)
            
            q_surf = font_btn.render("Qual padrão de erro ortográfico predominou nesta lenda?", True, PARCHMENT)
            screen.blit(q_surf, (balloon.centerx - q_surf.get_width()//2, balloon.y + 35))
            
            if game_state == "MECANICA_4":
                for btn in mec4_buttons:
                    btn.draw(screen)
                    
        elif game_state == "MECANICA_4_EXPLAIN":
            title = font_title.render("Sintetize seu Conhecimento", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
            
            sub = font_text.render("Explique com suas palavras a regra ortográfica que você acabou de identificar:", True, PARCHMENT)
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 140))
            
            box_rect = pygame.Rect(WIDTH//2 - 400, 200, 800, 250)
            pygame.draw.rect(screen, (20, 30, 25), box_rect, border_radius=12)
            pygame.draw.rect(screen, GOLD_DIM, box_rect, width=2, border_radius=12)
            
            cursor = "|" if (frame_count % 60) < 30 else ""
            display_text = student_explanation + cursor
            
            lines = wrap_text(display_text, font_text, box_rect.width - 40)
            y_offset = box_rect.y + 20
            for line in lines:
                line_surf = font_text.render(line, True, PARCHMENT)
                screen.blit(line_surf, (box_rect.x + 20, y_offset))
                y_offset += font_text.get_height() + 5
                
            hint = font_small.render("Digite sua explicação e pressione ENTER para enviar", True, TEXT_DIM)
            screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 480))

        elif game_state == "MECANICA_5":
            # Livro Animado
            title = font_title.render("A Lenda Restaurada", True, GOLD)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
            
            book_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
            draw_parchment(screen, book_rect)
            
            chapter = CHAPTERS_DATA[current_chapter_index]
            full_text = ""
            import re
            for pid in saved_order:
                pdata = next(p for p in chapter["paragraphs"] if p["id"] == pid)
                p_text = pdata["text"]
                if "bugs" in chapter:
                    for bug, bdata in chapter["bugs"].items():
                        correct = bdata["correto"]
                        p_text = re.sub(r'\b' + bug + r'\b', correct, p_text, flags=re.IGNORECASE)
                full_text += p_text + "\n\n"
                
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
                
        elif game_state == "CREATOR_WRITE":
            title = font_title.render("Modo Criador: Escreva sua Lenda", True, DANGER)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
            sub = font_small.render("Escreva até 8 linhas. Pressione ENTER para quebrar a linha.", True, TEXT_DIM)
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 90))
            
            box_rect = pygame.Rect(100, 150, WIDTH - 200, 400)
            draw_parchment(screen, box_rect)
            
            y_off = 170
            for i, line in enumerate(creator_lines):
                tsurf = font_text.render(line, True, (40, 20, 10))
                screen.blit(tsurf, (130, y_off))
                # Cursor piscante na última linha
                if i == len(creator_lines) - 1 and (frame_count // 30) % 2 == 0:
                    cursor_x = 130 + tsurf.get_width() + 2
                    pygame.draw.line(screen, DANGER, (cursor_x, y_off), (cursor_x, y_off + 24), 2)
                y_off += 30
                
            btn_creator_next.update_hover(mouse_pos)
            btn_creator_next.draw(screen)
            
        elif game_state == "CREATOR_CORRUPT":
            title = font_title.render("Modo Criador: Injete os Bugs", True, DANGER)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
            sub = font_small.render("Clique nas palavras e digite a versão incorreta delas.", True, TEXT_DIM)
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 90))
            
            box_rect = pygame.Rect(40, 150, WIDTH - 80, 300)
            draw_parchment(screen, box_rect)
            
            for cw in creator_words_cache:
                if cw.clean in creator_bugs:
                    cw.marked = True
                    cw.set_text(creator_bugs[cw.clean]["opcoes"][1]) # Mostra a corrompida
                else:
                    cw.marked = False
                cw.draw(screen)
                
            if creator_active_word:
                # Modal para digitar o bug
                modal_rect = pygame.Rect(WIDTH//2 - 250, 480, 500, 150)
                pygame.draw.rect(screen, CARD_BG, modal_rect, border_radius=12)
                pygame.draw.rect(screen, DANGER, modal_rect, width=2, border_radius=12)
                
                txt1 = font_small.render(f"Como escrever '{creator_active_word}' errado?", True, PARCHMENT)
                screen.blit(txt1, (WIDTH//2 - txt1.get_width()//2, 500))
                
                txt2 = font_title.render(creator_input_error + ("|" if (frame_count//30)%2==0 else ""), True, GOLD_LIGHT)
                screen.blit(txt2, (WIDTH//2 - txt2.get_width()//2, 540))
                
                hint = font_small.render("Pressione ENTER para salvar", True, TEXT_DIM)
                screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 600))
                
            btn_creator_play.update_hover(mouse_pos)
            btn_creator_play.draw(screen)
            
        elif game_state == "GAME_OVER":
            title = font_mega.render("GAME OVER", True, DANGER)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
            sub = font_text.render("Suas vidas acabaram! A lenda foi corrompida.", True, TEXT_COLOR)
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 - 10))
            btn_retry.draw(screen)
            
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
            
            ch_name = CHAPTERS_DATA[current_chapter_index]['name']
            final_msg = font_text.render(f"Você restaurou a {ch_name} e mapeou os padrões ortográficos!", True, TEXT_COLOR)
            screen.blit(final_msg, (WIDTH//2 - final_msg.get_width()//2, 260))
            
            # Lenda restaurada como "livro"
            book_rect = pygame.Rect(WIDTH//2 - 420, 310, 840, 280)
            draw_parchment(screen, book_rect)
            
            book_title = font_btn.render(f"{ch_name} - Restaurada", True, FOREST_DARK)
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
            
        # Animação Global de revelação do fragmento (Pode sobrepor qualquer tela)
        if fragment_reveal_timer > 0:
            fragment_reveal_timer -= 1
            # Fundo escurecido
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, (0, 0))
            # Card do fragmento
            frag_rect = pygame.Rect(WIDTH//2 - 220, HEIGHT//2 - 120, 440, 240)
            pygame.draw.rect(screen, CARD_BG, frag_rect, border_radius=16)
            pygame.draw.rect(screen, GOLD, frag_rect, width=2, border_radius=16)
            # Losango grande animado
            scale_f = min(1.0, (180 - fragment_reveal_timer) / 30.0)
            sz = int(40 * scale_f)
            cx, cy_f = WIDTH//2, HEIGHT//2 - 40
            frag_pts = [(cx, cy_f - sz), (cx + sz, cy_f), (cx, cy_f + sz), (cx - sz, cy_f)]
            glow_a = int(80 + 60 * math.sin(frame_count * 0.08))
            glow_surf = pygame.Surface((sz*4, sz*4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*GOLD, glow_a), (sz*2, sz*2), sz*2)
            screen.blit(glow_surf, (cx - sz*2, cy_f - sz*2))
            pygame.draw.polygon(screen, GOLD, frag_pts)
            pygame.draw.polygon(screen, GOLD_LIGHT, frag_pts, 2)
            # Texto
            ft1 = font_subtitle.render("Fragmento Coletado!", True, GOLD_LIGHT)
            screen.blit(ft1, (WIDTH//2 - ft1.get_width()//2, HEIGHT//2 + 20))
            ft2 = font_text.render(fragment_reveal_text, True, PARCHMENT)
            screen.blit(ft2, (WIDTH//2 - ft2.get_width()//2, HEIGHT//2 + 55))
            
        if lupa_active and game_state not in ["MENU", "CINEMATIC", "INTRO", "ROADMAP", "FIM"]:
            draw_lupa(screen, mouse_pos)
        
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
