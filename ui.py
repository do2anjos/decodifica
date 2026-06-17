import pygame
import math
from data import *

pygame.font.init()
font_mega = pygame.font.SysFont("Georgia", 56, bold=True)
font_title = pygame.font.SysFont("georgia", 42, bold=True)
font_subtitle = pygame.font.SysFont("georgia", 28, italic=True)
font_text = pygame.font.SysFont("verdana", 19)
font_btn = pygame.font.SysFont("verdana", 22, bold=True)
font_hud = pygame.font.SysFont("verdana", 18, bold=True)
font_small = pygame.font.SysFont("verdana", 14)
font_icon = pygame.font.SysFont("verdana", 26, bold=True)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line: lines.append(current_line)
            current_line = word + " "
    if current_line: lines.append(current_line)
    return lines

def clean_word(w):
    return w.strip('.,!?"\'\n').lower()



class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        bg = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, bg, self.rect, border_radius=8)
        pygame.draw.rect(surface, GOLD_DIM, self.rect, width=2, border_radius=8)
        
        txt_surf = font_btn.render(self.text, True, TEXT_COLOR)
        tx = self.rect.centerx - txt_surf.get_width() // 2
        ty = self.rect.centery - txt_surf.get_height() // 2
        surface.blit(txt_surf, (tx, ty))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class DraggableCard:
    def __init__(self, x, y, w, h, para_id, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.para_id = para_id
        self.text = text
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.snapped_to = -1

    def draw(self, surface):
        bg_col = (50, 80, 60) if self.dragging else CARD_BG
        pygame.draw.rect(surface, bg_col, self.rect, border_radius=6)
        pygame.draw.rect(surface, GOLD_DIM, self.rect, width=2, border_radius=6)
        
        id_surf = font_title.render(self.para_id, True, GOLD_LIGHT)
        surface.blit(id_surf, (self.rect.x + 10, self.rect.y + 10))
        
        lines = wrap_text(self.text, font_small, self.rect.width - 60)
        ly = self.rect.y + 10
        for line in lines:
            ts = font_small.render(line, True, TEXT_COLOR)
            surface.blit(ts, (self.rect.x + 50, ly))
            ly += ts.get_height() + 2

class ClickableWord:
    def __init__(self, word, x, y):
        self.original = word
        self.clean = clean_word(word)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 10, 10)
        self.set_text(word)
        
    def set_text(self, new_word):
        self.surf = font_text.render(new_word, True, TEXT_COLOR)
        self.rect.width = self.surf.get_width()
        self.rect.height = self.surf.get_height()
        
    def draw(self, surface, is_hovered):
        if is_hovered:
            pygame.draw.rect(surface, (80, 80, 100), self.rect)
        surface.blit(self.surf, (self.x, self.y))

def draw_hud(surface, lives, score, insig_dec, insig_abs, btn_lupa=None):
    hud_panel = pygame.Surface((WIDTH, 55), pygame.SRCALPHA)
    hud_panel.fill((10, 30, 18, 160))
    surface.blit(hud_panel, (0, 0))
    pygame.draw.line(surface, GOLD_DIM, (0, 55), (WIDTH, 55), 1)
    
    lx = 30
    label = font_hud.render("Vidas:", True, TEXT_DIM)
    surface.blit(label, (lx, 17))
    lx += label.get_width() + 10
    for i in range(3):
        color = DANGER if i < lives else (60, 30, 30)
        pygame.draw.circle(surface, color, (lx + i * 28, 28), 10)
        if i < lives:
            pygame.draw.circle(surface, DANGER_LIGHT, (lx + i * 28 - 3, 25), 3)
            
    px = WIDTH - 320
    diamond_pts = [(px, 28), (px+10, 18), (px+20, 28), (px+10, 38)]
    pygame.draw.polygon(surface, GOLD, diamond_pts)
    pygame.draw.polygon(surface, GOLD_LIGHT, [(px+5, 28), (px+10, 20), (px+15, 28)])
    
    pts_text = font_hud.render(f"{score} Pontos", True, GOLD_LIGHT)
    surface.blit(pts_text, (px + 28, 17))
    
    ix = WIDTH - 520
    pygame.draw.circle(surface, (40, 120, 200), (ix, 28), 10)
    pygame.draw.circle(surface, (100, 180, 255), (ix, 28), 10, 2)
    surf_dec = font_hud.render(str(insig_dec), True, (100, 180, 255))
    surface.blit(surf_dec, (ix + 15, 17))
    
    ix += 60
    pygame.draw.circle(surface, (150, 60, 180), (ix, 28), 10)
    pygame.draw.circle(surface, (255, 120, 220), (ix, 28), 10, 2)
    surf_abs = font_hud.render(str(insig_abs), True, (255, 120, 220))
    surface.blit(surf_abs, (ix + 15, 17))
    
    if btn_lupa:
        btn_lupa.draw(surface)

def draw_lupa(surface, mouse_pos):
    zoom = 1.5
    size = 110
    cx, cy = mouse_pos
    cap_w = int((size * 2) / zoom)
    cap_h = int((size * 2) / zoom)
    
    tx, ty = cx - cap_w // 2, cy - cap_h // 2
    if tx < 0: tx = 0
    if ty < 0: ty = 0
    if tx + cap_w > WIDTH: tx = WIDTH - cap_w
    if ty + cap_h > HEIGHT: ty = HEIGHT - cap_h
    
    cap_rect = pygame.Rect(tx, ty, cap_w, cap_h)
    if cap_rect.width <= 0 or cap_rect.height <= 0: return
    
    try:
        sub = surface.subsurface(cap_rect).copy()
        scaled = pygame.transform.smoothscale(sub, (size * 2, size * 2))
        
        mask = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (size, size), size)
        
        scaled.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        surface.blit(scaled, (cx - size, cy - size))
        pygame.draw.circle(surface, GOLD, (cx, cy), size, 3)
        pygame.draw.circle(surface, (255, 255, 255), (cx - size//3, cy - size//3), size//4, 2)
    except Exception:
        pass


def draw_gradient_bg(surface):
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(BG_TOP[0] * (1 - t) + BG_BOT[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOT[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOT[2] * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

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
        pygame.draw.line(surface, GOLD_DIM, (dz.right, dz.y + i), (dz.right, dz.y + min(i+8, dz.h)), 1)
    
    hint = font_small.render("Solte os parágrafos da lenda aqui", True, TEXT_DIM)
    surface.blit(hint, (dz.centerx - hint.get_width()//2, dz.y + 15))

def draw_trash_zone(surface, chapter):
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

