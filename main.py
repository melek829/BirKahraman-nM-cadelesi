#pgzero
import random

WIDTH = 1024
HEIGHT = 576
TITLE = "BİR SAVAŞÇININ MÜCADELESİ"

arkaplan = Actor("arkaplan", (512, 288))
karakter = Actor("karakter", (50, 366), size=(90, 120)) 
zombi = Actor("zombi", (932, 510), size=(180, 180))
ufo = Actor("ufo", (1050, 120), size=(180, 180))
goo = Actor("GOO", (512, 288))
play = Actor("play", (512, 288))
win = Actor("win",(512,288))

mermiler = []
count = 0
mode = "menu"
hiz = 10
level = 1   # oyuna Level 1’den başla

def draw():
    if mode == "menu":
        arkaplan.draw()
        play.draw()
    
    elif mode == "game":
        arkaplan.draw()
        karakter.draw()
        zombi.draw()
        ufo.draw()
        for i in range(len(mermiler)):
            mermiler[i].draw()
        screen.draw.text("Skor: " + str(count), pos=(20, 20), color="white", fontsize=30)
        screen.draw.text("Level: " + str(level), pos=(20, 50), color="yellow", fontsize=30)

    elif mode == "end":
        arkaplan.draw()
        goo.draw()
        screen.draw.text("Final Skoru: " + str(count), center=(512, 400), color="red", fontsize=50)
        screen.draw.text("Yeniden baslamak icin ENTER'a bas", center=(512, 450), color="white", fontsize=30)

    elif mode == "win":
        arkaplan.draw()
        win.draw()
        screen.draw.text("KAZANDIN!", center=(512, 400), color="green", fontsize=50)
        screen.draw.text("Yeniden baslamak icin ENTER'a bas", center=(512, 450), color="white", fontsize=30)

def update(dt):
    global count, mode, hiz, level, mermiler

    if mode == "game":
        if keyboard.left and karakter.x > 50:
            karakter.x -= 7
        elif keyboard.right and karakter.x < WIDTH - 50:
            karakter.x += 7
        if keyboard.up: karakter.y -= 7
        if keyboard.down: karakter.y += 7

        # LEVEL 1: Engellerden Kaçış
        if level == 1:
            zombi.x -= hiz
            ufo.x -= hiz + 2

            if zombi.x < -50:
                zombi.x = WIDTH + random.randint(10, 100)
                zombi.y = random.randint(460, 510)
                count += 1
            if ufo.x < -50:
                ufo.x = WIDTH + random.randint(10, 100)
                ufo.y = random.randint(80, 280)
                count += 1

            if karakter.colliderect(zombi) or karakter.colliderect(ufo):
                mode = "end"

            if count >= 6:   # Engellerden Kaçış ile aynı eşik
                level = 2
                

        # LEVEL 2: Mermiyle saldırma
        elif level == 2:
            zombi.x -= hiz
            ufo.x -= hiz + 2

            if zombi.x < -50:
                zombi.x = WIDTH + random.randint(10, 100)
                zombi.y = random.randint(460, 510)
            if ufo.x < -50:
                ufo.x = WIDTH + random.randint(10, 100)
                ufo.y = random.randint(80, 280)

            
            for i in range(len(mermiler)):
                mermiler[i].x += 10
                if mermiler[i].colliderect(zombi):
                    count += 1
                    zombi.pos = (WIDTH + random.randint(10, 100), random.randint(460, 510))
                elif mermiler[i].colliderect(ufo):
                    count += 1
                    ufo.pos = (WIDTH + random.randint(10, 100), random.randint(80, 280))
                elif mermiler[i].x < WIDTH:
                    mermiler.pop(i)
                    break

            if karakter.colliderect(zombi) or karakter.colliderect(ufo):
                mode = "end"

            if count >= 30:
                mode = "win"

    if (mode == "end" or mode == "win") and keyboard.enter:
        count = 0
        hiz = 10
        level = 1
        karakter.pos = (50, 366)
        zombi.pos = (932, 510)
        ufo.pos = (1070, 120)
        mermiler = []
        mode = "game"

def on_key_down(key):
    global mermiler
    if mode == "game" and level == 2:
        if keyboard.space:
            mermiler += [Actor("mermi", (karakter.x + 40, karakter.y), size=(32, 32))]

def on_mouse_down(button, pos):
    global mode,level
    if mode == "menu" and button == mouse.left:
        if play.collidepoint(pos):
            mode = "game"
    elif mode == "game" and level == 2 and button == mouse.left:
            mermi = Actor("mermi", (karakter.x+40, karakter.y), size=(32,32)) 
            mermi.pos = pos 
            mermiler.append(mermi)
