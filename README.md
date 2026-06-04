Itch.io'da yayınlarken ya da projenin GitHub sayfasına yüklediğinde insanların (ve mülakattaki jürinin) ilk bakacağı yer burasıdır. Profesyonel bir Indie RPG projesine yakışacak, temiz ve dikkat çekici bir **`README.md`** dosyası hazırladım.

Proje klasörünün içinde **`README.md`** adında yeni bir dosya oluştur ve aşağıdaki metni aynen içine yapıştır:

```markdown
# ⚔️ Procedural Dungeon Crawler RPG

A highly polished, 2D top-down Roguelike-RPG prototype built from scratch using **Python** and **Pygame**. This project features entirely procedural dungeon generation, autonomous multi-enemy AI using advanced pathfinding, reactive camera mechanics, dynamic atmospheric lighting, and a linear quest system.

Designed with **Clean Code** principles and a component-based design pattern, this prototype is fully optimized and production-ready for indie game platforms like **Itch.io**.

---

## 🌟 Key Features

* **Procedural Level Generation:** Fully randomized dungeon layouts with uniquely shaped rooms and corridors connected seamlessly on every reset.
* **A\* (A-Star) Pathfinding AI:** Multiple enemy entities calculating optimal, wall-avoiding movement vectors to hunt down the player dynamically.
* **Dynamic Visual "Juice":**
    * **Screen Shake:** Immersive screen rattling triggered upon dealing or receiving damage to enhance impact feedback.
    * **Flash-on-Hit:** Visual color manipulation alerting players when enemies sustain damage.
* **Atmospheric Raycast-Style Lighting:** A persistent "Fog of War" mask tracking the player's position, mimicking an active, realistic torchlight effect.
* **Isometric Depth Trick:** Wall textures fitted with distinct face and top highlights layered with automated ceiling shadow drops onto floor tiles.
* **Quest & Tutorial Flow:** An integrated linear quest chain managed via runtime conditions, guided by an interactive Wizard NPC.

---

## 🎮 How to Play & Controls

| Input | Action |
| :--- | :--- |
| **`W`, `A`, `S`, `D`** | Move the Hero through the dungeon |
| **`E`** | Interact with the Wizard NPC / Advance Dialogues |
| **`K`** | Slash your Sword in your current facing direction |
| **`Space`** | Re-roll & Generate a brand new procedural dungeon |

### 📜 Game Loop & Objectives:
1. Wake up in the dark dungeon and locate the **Wizard NPC** (Green Circle).
2. Press `E` to talk, learn your tutorial basics, and initiate the **Monster Hunt**.
3. Hunt down the aggressive abominations using your sword (`K`). Watch out for your **HP Bar**!
4. Once cleared, scour the rooms for hidden **Treasure Chests** to secure the loot.
5. Return safely to the Wizard to claim absolute victory!

---

## 🛠️ Technical Stack & Architecture

* **Language:** Python 3.13+
* **Engine/Framework:** Pygame 2.6.1
* **Architecture:** Modular/Component-Based (`main.py` driving runtime scenes, while data models, map logic, and entity rendering handle components in `rpg_sistemleri.py`).
* **Algorithms:** Heuristic-driven $A^*$ Pathfinding optimized with Python's native binary heap manager (`heapq`).

---

## 🚀 Installation & Local Execution

### Prerequisites
Ensure you have Python 3 and the Pygame dependency installed on your local environment:
```bash
pip install pygame

```

### Running the Game

Navigate to your project root folder and execute the controller runtime:

```bash
python main.py

```

*(Windows Users alternative fallback launch option if system variables are not configured: `& "C:\Users\user\AppData\Local\Microsoft\WindowsApps\python3.13.exe" main.py`)*

---

```

### 💡 Neden Bu Şekilde Hazırladık?
* **Profesyonel Dil:** Uluslararası oyun geliştirme standartlarına uygun olarak tamamen **İngilizce** yazdım. Itch.io'da global oyuncu kitlesinin ve akademik jürilerin en çok dikkat ettiği şey budur.
* **Algoritma Vurgusu:** A* ve `heapq` optimizasyonlarını özellikle belirttim ki kod kaliteni ön plana çıkarsın.
* **Kontrol Tablosu:** Markdown tablo yapısıyla oyuncular için son derece okunaklı bir kılavuz oluşturduk.

Her şey hazır! Proje hem kod yapısıyla hem de sunumuyla tam bir "Indie" ürünü oldu. Sırada Itch.io için kapak görseli planlamak mı var, yoksa kod içinde değiştirmek istediğin başka bir mekanik var mı?

```
