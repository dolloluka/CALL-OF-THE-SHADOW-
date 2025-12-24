import pgzrun
import random
import math

WIDTH = 1000
HEIGHT = 600

mode = "menu"
show_credits = False

bg = Actor("background", (WIDTH//2, HEIGHT//2))
sf = Actor("sheriff", (100, 300))
npc = Actor("npc", (200, 250))
icon = Actor("icon", (npc.x, npc.y - 60))

start_button = Rect((WIDTH//2 - 150, HEIGHT//2 - 40), (300, 80))
ready_button = Rect((WIDTH - 170, 20), (150, 50))
credits_button = Rect((WIDTH - 200, HEIGHT - 70), (180, 50))
back_button = Rect((WIDTH//2 - 100, HEIGHT//2 + 80), (200, 50))

bullets = []
enemies = []
stars = []
snowflakes = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(60)]

wave = 0
waiting_wave = True
has_star = False
thank_you = False
exit_timer = 0

music.play("game")
music.set_volume(0.1)

def spawn_wave(w):
    enemies.clear()
    if w == 1:
        for _ in range(10):
            enemies.append({d"actor": Actor("enemy", (random.randint(650, 980), random.randint(80, 520))),"hp": 3,"boss": False})
    if w == 2:
        enemies.append({"actor": Actor("enemy", (850, 300)),"hp": 100,"boss": True})

def draw():
    screen.clear()

    if mode == "menu":
        bg.draw()
        screen.draw.filled_rect(start_button, "darkred")
        screen.draw.text("BASLA", center=start_button.center, fontsize=50, color="white")
        screen.draw.text("CALL OF THE SHADOW", center=(WIDTH//2, 150), fontsize=60, color="white")

        screen.draw.filled_rect(credits_button, "darkblue")
        screen.draw.text("Emeği Geçenler", center=credits_button.center, fontsize=28, color="white")

        if show_credits:
            screen.fill("black")
            screen.draw.text("Emeği Geçenler   BULUT HEPAĞLAR      SARI ALİ ŞABAN",center=(WIDTH//2, HEIGHT//2 - 20),fontsize=40,color="white" )
            screen.draw.filled_rect(back_button, "darkred")
            screen.draw.text("Oyuna Geri Don", center=back_button.center, fontsize=30, color="white")
        return

    bg.draw()
    sf.draw()
    npc.draw()

    for e in enemies:
        e["actor"].draw()
        screen.draw.text(str(e["hp"]), center=(e["actor"].x, e["actor"].y - 40), fontsize=24, color="red")

    for b in bullets:
        b["actor"].draw()

    for s in stars:
        s.draw()

    if sf.distance_to(npc) <= 75:
        icon.pos = (npc.x, npc.y - 60)
        icon.draw()

    if not has_star and sf.distance_to(npc) <= 80:
        screen.draw.text("Sheriff! Dusmanlari yen ve yilbasini kurtar",
                         center=(WIDTH//2, 100), fontsize=30, color="white")

    if has_star and not thank_you:
        screen.draw.text("Yildizi aldin, bana geri getir",
                         center=(WIDTH//2, 100), fontsize=30, color="yellow")

    if thank_you:
        screen.draw.text("Tesekkurler Sheriff",
                         center=(WIDTH//2, HEIGHT//2 - 20), fontsize=40, color="yellow")
        screen.draw.text("Oynadiginiz icin tesekkurler",
                         center=(WIDTH//2, HEIGHT//2 + 30), fontsize=30, color="white")

    if waiting_wave and wave < 3:
        screen.draw.filled_rect(ready_button, "green")
        screen.draw.text("HAZIR", center=ready_button.center, fontsize=32, color="black")

    screen.draw.text(f"DALGA: {wave}/2", topleft=(20, 20), fontsize=30, color="white")

    for snow in snowflakes:
        screen.draw.circle(snow, 2, "white")

def update(dt):
    global waiting_wave, has_star, thank_you, exit_timer

    if mode != "game":
        return

    if keyboard.a and sf.x > 40:
        sf.x -= 5
    if keyboard.d and sf.x < WIDTH - 40:
        sf.x += 5
    if keyboard.w and sf.y > 40:
        sf.y -= 5
    if keyboard.s and sf.y < HEIGHT - 40:
        sf.y += 5

    for b in bullets[:]:
        b["actor"].x += b["dx"]
        b["actor"].y += b["dy"]

        if b["actor"].x < -50 or b["actor"].x > WIDTH + 50 or b["actor"].y < -50 or b["actor"].y > HEIGHT + 50:
            bullets.remove(b)
            continue

        for e in enemies[:]:
            if b["actor"].colliderect(e["actor"]):
                e["hp"] -= 1
                bullets.remove(b)
                if e["hp"] <= 0:
                    if e["boss"]:
                        stars.append(Actor("star", e["actor"].pos))
                    enemies.remove(e)
                break

    for e in enemies:
        a = e["actor"]
        speed = 1 if not e["boss"] else 0.7
        a.x += speed if a.x < sf.x else -speed
        a.y += speed if a.y < sf.y else -speed

        if sf.colliderect(a):
            music.stop()
            pgzrun.quit()

    if enemies == [] and not waiting_wave and wave < 3:
        waiting_wave = True

    for s in stars[:]:
        if sf.colliderect(s):
            stars.remove(s)
            has_star = True

    if thank_you:
        exit_timer -= dt
        if exit_timer <= 0:
            pgzrun.quit()

    for snow in snowflakes:
        snow[1] += 2
        if snow[1] > HEIGHT:
            snow[1] = 0
            snow[0] = random.randint(0, WIDTH)

def on_mouse_down(pos):
    global mode, wave, waiting_wave, thank_you, exit_timer, show_credits

    if mode == "menu":
        if start_button.collidepoint(pos):
            mode = "game"
            show_credits = False
        elif credits_button.collidepoint(pos):
            show_credits = True
        elif show_credits and back_button.collidepoint(pos):
            show_credits = False
        return

    if waiting_wave and ready_button.collidepoint(pos):
        wave += 1
        waiting_wave = False
        spawn_wave(wave)
        return

    if has_star and npc.collidepoint(pos) and sf.distance_to(npc) <= 80:
        thank_you = True
        exit_timer = 3
        return

    dx = pos[0] - sf.x
    dy = pos[1] - sf.y
    length = math.hypot(dx, dy)
    if length == 0:
        return

    speed = 10
    bullets.append({"actor": Actor("bullet", (sf.x, sf.y)),"dx": dx / length * speed,"dy": dy / length * speed})

pgzrun.go()
