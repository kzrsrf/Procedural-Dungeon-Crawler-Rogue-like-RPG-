import pygame
import sys
import random
import math
from rpgsistemleri import HaritaUretici, Oyuncu, Dusman, QuestGiver, Sandik, HUCRE_BOYUTU, GRID_EN, GRID_BOY

PENCERE_EN, PENCERE_BOY = 800, 600
FPS = 60

# Renkler
RENK_ARKA_PLAN = (8, 7, 11)
RENK_DUVAR_ON = (54, 50, 64)
RENK_DUVAR_UST = (87, 82, 102)
RENK_ZEMIN = (28, 26, 33)
RENK_ZEMIN_CIZGI = (34, 31, 41)
RENK_GOLGE = (16, 15, 20)
RENK_MEŞALE = (255, 180, 70, 10)

def ana_dongu():
    pygame.init()
    ekran = pygame.display.set_mode((PENCERE_EN, PENCERE_BOY))
    pygame.display.set_caption("Zindan Savaşçısı - Itch.io Edition")
    saat = pygame.time.Clock()
    font_ui = pygame.font.SysFont("Arial", 16, bold=True)
    font_dialog = pygame.font.SysFont("Georgia", 18, italic=True)

    harita = HaritaUretici()
    harita.harita_olustur()

    # Kamera & Ekran Sallantı Verileri
    kam_x, kam_y = 0, 0
    sallanti_gucu = 0

    # Nesneleri Doğurma
    ox, oy = harita.odalar[0].center
    oyuncu = Oyuncu(ox, oy)
    
    # Tutorial NPC'sini oyuncunun hemen yanına koy
    npc = QuestGiver(ox + 2, oy)

    dusmanlar = []
    sandiklar = []
    for oda in harita.odalar[1:]:
        dusmanlar.append(Dusman(oda.center[0], oda.center[1]))
        sx, sy = random.randint(oda.x + 1, oda.x + oda.width - 2), random.randint(oda.y + 1, oda.y + oda.height - 2)
        sandiklar.append(Sandik(sx, sy))

    # Çoklu Görev Zinciri Durumları:
    # "TUTORIAL" -> "TALK_TO_NPC" -> "KILL_ENEMIES" -> "LOOT_CHESTS" -> "ALL_DONE"
    gorev_durumu = "TUTORIAL"
    diyalog_metni = "Welcome! Use WASD to move. Walk to the Wizard NPC and press E to get your quest!"

    isik_maskesi = pygame.Surface((PENCERE_EN, PENCERE_BOY))

    while True:
        # Ekran Sallantısı Azaltma
        if sallanti_gucu > 0: sallanti_gucu -= 1

        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if olay.type == pygame.KEYDOWN:
                if oyuncu.can > 0:
                    if olay.key in [pygame.K_LEFT, pygame.K_a]: oyuncu.hareket_et(-1, 0, harita.grid)
                    if olay.key in [pygame.K_RIGHT, pygame.K_d]: oyuncu.hareket_et(1, 0, harita.grid)
                    if olay.key in [pygame.K_UP, pygame.K_w]: oyuncu.hareket_et(0, -1, harita.grid)
                    if olay.key in [pygame.K_DOWN, pygame.K_s]: oyuncu.hareket_et(0, 1, harita.grid)
                    
                    # KTuşu: Kılıç Saldırısı
                    if olay.key == pygame.K_k:
                        if oyuncu.saldiri_kalan_sure == 0:
                            oyuncu.saldiri_kalan_sure = 12
                            # Saldırı Menzili Kontrolü (Önündeki hücre)
                            s_hx = oyuncu.grid_x + oyuncu.yon[0]
                            s_hy = oyuncu.grid_y + oyuncu.yon[1]
                            for d in dusmanlar:
                                if d.grid_x == s_hx and d.grid_y == s_hy:
                                    d.can -= 15
                                    d.hasar_parlama = 8
                                    sallanti_gucu = 6 # Ekran sarsılsın
                    
                    # E Tuşu: NPC ile Konuşma
                    if olay.key in [pygame.K_e, pygame.K_e]:
                        dist = math.hypot(oyuncu.grid_x - npc.grid_x, oyuncu.grid_y - npc.grid_y)
                        if dist <= 2:
                            if gorev_durumu == "TUTORIAL" or gorev_durumu == "TALK_TO_NPC":
                                gorev_durumu = "KILL_ENEMIES"
                                diyalog_metni = "Wizard: 'Monsters have taken over! Press K to swing your sword. Purge them all!'"
                            elif gorev_durumu == "ALL_DONE":
                                diyalog_metni = "Wizard: 'Incredible! You are the true hero. Press SPACE to enter a new dungeon!'"

                # Space: Haritayı Yenile
                if olay.key == pygame.K_SPACE and (gorev_durumu == "ALL_DONE" or oyuncu.can <= 0):
                    harita.harita_olustur()
                    ox, oy = harita.odalar[0].center
                    oyuncu = Oyuncu(ox, oy)
                    npc = QuestGiver(ox + 2, oy)
                    dusmanlar = [Dusman(o.center[0], o.center[1]) for o in harita.odalar[1:]]
                    sandiklar = []
                    for o in harita.odalar[1:]:
                        sx, sy = random.randint(o.x + 1, o.x + o.width - 2), random.randint(o.y + 1, o.y + o.height - 2)
                        sandiklar.append(Sandik(sx, sy))
                    gorev_durumu = "TUTORIAL"
                    diyalog_metni = "A new zindan awaits! Go speak to the Wizard."

        # Sistem Güncellemeleri
        oyuncu.guncelle()
        
        # Görev Durum Kontrolleri (Quest Logic)
        if gorev_durumu == "KILL_ENEMIES":
            # Ölen canavarları listeden uçur
            dusmanlar = [d for d in dusmanlar if d.can > 0]
            if not dusmanlar:
                gorev_durumu = "LOOT_CHESTS"
                diyalog_metni = "Quest Update: 'All monsters purged! Now open all chestna hidden in rooms!'"
        
        for d in dusmanlar:
            eski_can = oyuncu.can
            d.guncelle((oyuncu.grid_x, oyuncu.grid_y), harita.grid, oyuncu)
            if oyuncu.can < eski_can: sallanti_gucu = 12 # Hasar alınca güçlü sarsıntı

        # Sandık Açma Kontrolü
        for s in sandiklar:
            if oyuncu.grid_x == s.grid_x and oyuncu.grid_y == s.grid_y and not s.acildi:
                if gorev_durumu == "LOOT_CHESTS":
                    s.acildi = True
                    if all(chest.acildi for chest in sandiklar):
                        gorev_durumu = "ALL_DONE"
                        diyalog_metni = "Quest Update: 'Success! Return to the Wizard NPC to claim victory!'"

        # Akıcı Kamera + Ekran Sallantısı (Juice)
        hedef_k_x = oyuncu.px - PENCERE_EN // 2
        hedef_k_y = oyuncu.py - PENCERE_BOY // 2
        kam_x += (hedef_k_x - kam_x) * 0.08
        kam_y += (hedef_k_y - kam_y) * 0.08

        render_x = kam_x + (random.randint(-sallanti_gucu, sallanti_gucu) if sallanti_gucu > 0 else 0)
        render_y = kam_y + (random.randint(-sallanti_gucu, sallanti_gucu) if sallanti_gucu > 0 else 0)

        # Çizim Dünyası
        ekran.fill(RENK_ARKA_PLAN)
        
        for y in range(GRID_BOY):
            for x in range(GRID_EN):
                px, py = int(x * HUCRE_BOYUTU - render_x), int(y * HUCRE_BOYUTU - render_y)
                if -HUCRE_BOYUTU <= px < PENCERE_EN and -HUCRE_BOYUTU <= py < PENCERE_BOY:
                    if harita.grid[y][x] == 1:
                        pygame.draw.rect(ekran, RENK_DUVAR_ON, (px, py + 10, HUCRE_BOYUTU, HUCRE_BOYUTU - 10))
                        pygame.draw.rect(ekran, RENK_DUVAR_UST, (px, py, HUCRE_BOYUTU, 10))
                    else:
                        pygame.draw.rect(ekran, RENK_ZEMIN, (px, py, HUCRE_BOYUTU, HUCRE_BOYUTU))
                        pygame.draw.rect(ekran, RENK_ZEMIN_CIZGI, (px, py, HUCRE_BOYUTU, HUCRE_BOYUTU), 1)
                        if y > 0 and harita.grid[y-1][x] == 1:
                            pygame.draw.rect(ekran, RENK_GOLGE, (px, py, HUCRE_BOYUTU, 12))

        # Nesneleri Çiz
        npc.ciz(ekran, render_x, render_y, gorev_durumu)
        for s in sandiklar: s.ciz(ekran, render_x, render_y)
        for d in dusmanlar: d.ciz(ekran, render_x, render_y)
        if oyuncu.can > 0: oyuncu.ciz(ekran, render_x, render_y)

        # Meşale Maskesi
        isik_maskesi.fill((10, 8, 15))
        if oyuncu.can > 0:
            om_x = int(oyuncu.px - render_x + HUCRE_BOYUTU // 2)
            om_y = int(oyuncu.py - render_y + HUCRE_BOYUTU // 2)
            for r in range(240, 60, -30):
                pygame.draw.circle(isik_maskesi, RENK_MEŞALE, (om_x, om_y), r)
            pygame.draw.circle(isik_maskesi, (255, 255, 255), (om_x, om_y), 60)
        ekran.blit(isik_maskesi, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # ==================== HUD / UI ARAYÜZÜ ====================
        # 1. Diyalog / Bilgi Kutusu (Ekranın Altı)
        pygame.draw.rect(ekran, (24, 22, 31), (30, PENCERE_BOY - 85, PENCERE_EN - 60, 65), border_radius=8)
        pygame.draw.rect(ekran, RENK_DUVAR_ON, (30, PENCERE_BOY - 85, PENCERE_EN - 60, 65), 2, border_radius=8)
        txt_diag = font_dialog.render(diyalog_metni, True, (230, 225, 240))
        ekran.blit(txt_diag, (45, PENCERE_BOY - 65))

        # 2. Görev Durum Paneli (Sol Üst)
        pygame.draw.rect(ekran, (20, 18, 26), (20, 20, 260, 50), border_radius=6)
        txt_g_title = font_ui.render(f"QUEST: {gorev_durumu}", True, (255, 215, 0))
        ekran.blit(txt_g_title, (35, 35))

        # 3. Oyuncu Can Barı (Sağ Üst - Kalp Hissiyatı)
        pygame.draw.rect(ekran, (30, 10, 15), (PENCERE_EN - 220, 20, 200, 20), border_radius=4)
        if oyuncu.can > 0:
            pygame.draw.rect(ekran, (230, 50, 70), (PENCERE_EN - 220, 20, int(200 * (oyuncu.can / oyuncu.max_can)), 20), border_radius=4)
        txt_hp = font_ui.render(f"HP: {oyuncu.can}/100", True, (255, 255, 255))
        ekran.blit(txt_hp, (PENCERE_EN - 150, 22))

        # Game Over Ekranı
        if oyuncu.can <= 0:
            s = pygame.Surface((PENCERE_EN, PENCERE_BOY), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            ekran.blit(s, (0, 0))
            txt_lose = font_dialog.render("YOU DIED. Press SPACE to restart your journey.", True, (255, 50, 50))
            ekran.blit(txt_lose, (PENCERE_EN//2 - 180, PENCERE_BOY//2))

        pygame.display.flip()
        saat.tick(FPS)

if __name__ == "__main__":
    ana_dongu()