import pygame
import random
import heapq
import math

HUCRE_BOYUTU = 48
GRID_EN = 45       
GRID_BOY = 35

# Renk Paleti
RENK_DUVAR_ON = (54, 50, 64)
RENK_DUVAR_UST = (87, 82, 102)
RENK_ZEMIN = (28, 26, 33)
RENK_ZEMIN_CIZGI = (34, 31, 41)
RENK_GOLGE = (16, 15, 20)
RENK_ALTIN = (255, 215, 0)

def manhattan_mesafesi(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star_pathfinding(start, goal, grid):
    if grid[start[1]][start[0]] == 1 or grid[goal[1]][goal[0]] == 1:
        return []
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    iterasyon = 0
    while open_list and iterasyon < 300:
        iterasyon += 1
        current = heapq.heappop(open_list)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_EN and 0 <= neighbor[1] < GRID_BOY:
                if grid[neighbor[1]][neighbor[0]] == 1: continue
                gecici_g = g_score[current] + 1
                if neighbor not in g_score or gecici_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = gecici_g
                    f_score = gecici_g + manhattan_mesafesi(neighbor, goal)
                    heapq.heappush(open_list, (f_score, neighbor))
    return []

class HaritaUretici:
    def __init__(self):
        self.grid = [[1 for _ in range(GRID_EN)] for _ in range(GRID_BOY)]
        self.odalar = []

    def harita_olustur(self):
        self.grid = [[1 for _ in range(GRID_EN)] for _ in range(GRID_BOY)]
        self.odalar = []
        for _ in range(12):
            w, h = random.randint(6, 10), random.randint(6, 10)
            x, y = random.randint(2, GRID_EN - w - 2), random.randint(2, GRID_BOY - h - 2)
            yeni_oda = pygame.Rect(x, y, w, h)
            if not any(yeni_oda.colliderect(o.inflate(2, 2)) for o in self.odalar):
                for oy in range(yeni_oda.y, yeni_oda.y + yeni_oda.height):
                    for ox in range(yeni_oda.x, yeni_oda.x + yeni_oda.width):
                        self.grid[oy][ox] = 0
                if self.odalar:
                    ex, ey = self.odalar[-1].center
                    yx, yy = yeni_oda.center
                    if random.random() < 0.5:
                        self._kaz_y(ex, yx, ey)
                        self._kaz_d(ey, yy, yx)
                    else:
                        self._kaz_d(ey, yy, ex)
                        self._kaz_y(ex, yx, yy)
                self.odalar.append(yeni_oda)

    def _kaz_y(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1): self.grid[y][x] = 0
    def _kaz_d(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1): self.grid[y][x] = 0

class Oyuncu:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.px, self.py = x * HUCRE_BOYUTU, y * HUCRE_BOYUTU
        self.max_can = 100
        self.can = 100
        self.yon = (1, 0) # Bakılan yön (dx, dy)
        self.saldiri_kalan_sure = 0

    def guncelle(self):
        self.px += (self.grid_x * HUCRE_BOYUTU - self.px) * 0.25
        self.py += (self.grid_y * HUCRE_BOYUTU - self.py) * 0.25
        if self.saldiri_kalan_sure > 0: self.saldiri_kalan_sure -= 1

    def hareket_et(self, dx, dy, grid):
        self.yon = (dx, dy)
        hx, hy = self.grid_x + dx, self.grid_y + dy
        if 0 <= hx < GRID_EN and 0 <= hy < GRID_BOY and grid[hy][hx] == 0:
            self.grid_x, self.grid_y = hx, hy

    def ciz(self, ekran, k_x, k_y):
        cx, cy = int(self.px - k_x + HUCRE_BOYUTU//2), int(self.py - k_y + HUCRE_BOYUTU//2)
        pygame.draw.circle(ekran, (190, 200, 210), (cx, cy + 6), 12)
        pygame.draw.circle(ekran, (240, 200, 160), (cx, cy - 4), 10)
        pygame.draw.rect(ekran, (230, 50, 50), (cx - 10, cy - 12, 20, 6), border_radius=2)
        
        # Kılıç Savurma Animasyonu
        if self.saldiri_kalan_sure > 0:
            sx = cx + self.yon[0] * 24
            sy = cy + self.yon[1] * 24
            pygame.draw.circle(ekran, (255, 255, 255), (sx, sy), 14, 3)

class Dusman:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.px, self.py = x * HUCRE_BOYUTU, y * HUCRE_BOYUTU
        self.max_can = 30
        self.can = 30
        self.hasar_parlama = 0
        self._timer = random.randint(0, 15)

    def guncelle(self, o_grid, grid, oyuncu):
        self.px += (self.grid_x * HUCRE_BOYUTU - self.px) * 0.1
        self.py += (self.grid_y * HUCRE_BOYUTU - self.py) * 0.1
        if self.hasar_parlama > 0: self.hasar_parlama -= 1
        
        self._timer += 1
        if self._timer >= 30:
            if manhattan_mesafesi((self.grid_x, self.grid_y), o_grid) < 10:
                yol = a_star_pathfinding((self.grid_x, self.grid_y), o_grid, grid)
                if yol:
                    # Oyuncunun üzerine basacaksa basmasın, hasar versin
                    if yol[0] == o_grid:
                        oyuncu.can = max(0, oyuncu.can - 10)
                    else:
                        self.grid_x, self.grid_y = yol[0]
            self._timer = 0

    def ciz(self, ekran, k_x, k_y):
        cx, cy = int(self.px - k_x + HUCRE_BOYUTU//2), int(self.py - k_y + HUCRE_BOYUTU//2)
        renk = (255, 50, 50) if self.hasar_parlama > 0 else (140, 60, 170)
        pygame.draw.circle(ekran, renk, (cx, cy), 13)
        pygame.draw.circle(ekran, (255, 30, 30), (cx - 4, cy - 2), 3)
        pygame.draw.circle(ekran, (255, 30, 30), (cx + 4, cy - 2), 3)
        
        # Mini Can Barı
        if self.can < self.max_can:
            pygame.draw.rect(ekran, (50, 10, 10), (cx - 15, cy - 22, 30, 4))
            pygame.draw.rect(ekran, (255, 50, 50), (cx - 15, cy - 22, int(30 * (self.can / self.max_can)), 4))

class QuestGiver:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y

    def ciz(self, ekran, k_x, k_y, gorev_durum):
        px = int(self.grid_x * HUCRE_BOYUTU - k_x + HUCRE_BOYUTU//2)
        py = int(self.grid_y * HUCRE_BOYUTU - k_y + HUCRE_BOYUTU//2)
        pygame.draw.circle(ekran, (50, 200, 120), (px, py), 14) # Bilge NPC
        pygame.draw.circle(ekran, (255, 255, 255), (px, py - 4), 8, 1)
        
        # Başındaki Soru/Ünlem İşareti (RPG Klasiği!)
        if gorev_durum in ["TALK_TO_NPC", "ALL_DONE"]:
            pygame.draw.circle(ekran, RENK_ALTIN, (px, py - 26), 4)

class Sandik:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.acildi = False

    def ciz(self, ekran, k_x, k_y):
        px, py = int(self.grid_x * HUCRE_BOYUTU - k_x + 6), int(self.grid_y * HUCRE_BOYUTU - k_y + 10)
        w, h = HUCRE_BOYUTU - 12, HUCRE_BOYUTU - 16
        if not self.acildi:
            pygame.draw.rect(ekran, (180, 110, 40), (px, py, w, h), border_radius=4)
            pygame.draw.rect(ekran, RENK_ALTIN, (px + w//2 - 3, py + h - 10, 6, 6))
        else:
            pygame.draw.rect(ekran, (120, 70, 20), (px, py, w, h), border_radius=4)
            pygame.draw.rect(ekran, RENK_ALTIN, (px + 4, py + 2, w - 8, 8))