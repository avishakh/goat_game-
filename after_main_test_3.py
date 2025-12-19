import turtle
import os
import math
import random
import pygame

# ---------- SETUP ----------
def setup_screen():
    wn = turtle.Screen()
    wn.bgcolor("black")
    wn.title("Space Invaders")
    wn.bgpic("space_invaders_background.gif")
    wn.tracer(0)
    return wn

def setup_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)


# ---------- GLOBAL STATE ----------
score = 0
enemyspeed = 2
bulletstate = "ready"
game_running = True
ramos_active = False
ramos_speed = 4
speed_increase_threshold = 100

# ---------- DRAWING OBJECTS ----------
def draw_border():
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.color("white")
    border_pen.penup()
    border_pen.setposition(-300, -300)
    border_pen.pendown()
    border_pen.pensize(3)
    for _ in range(4):
        border_pen.forward(600)
        border_pen.left(90)
    border_pen.hideturtle()

def create_score_pen():
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.setposition(-290, 260)
    pen.hideturtle()
    return pen

# ---------- ENTITIES ----------
def create_player():
    player = turtle.Turtle()
    player.color("green")
    player.shape("player.gif")
    player.penup()
    player.speed(0)
    player.setposition(0, -250)
    player.setheading(90)
    player.move_speed = 0
    return player

def create_enemies():
    shapes = ["invaders_1.gif", "invaders_2.gif", "invaders_3.gif", "invaders_4.gif", "invaders_5.gif"]
    enemies = []
    for i in range(5):
        enemy = turtle.Turtle()
        enemy.shape(shapes[i % len(shapes)])
        enemy.color("red")
        enemy.penup()
        enemy.speed(0)
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.setposition(x, y)
        enemies.append(enemy)
    return enemies

def create_bullet():
    bullet = turtle.Turtle()
    bullet.color("yellow")
    bullet.shape("triangle")
    bullet.penup()
    bullet.speed(0)
    bullet.setheading(90)
    bullet.shapesize(0.5, 0.5)
    bullet.hideturtle()
    return bullet

def create_ramos():
    ramos = turtle.Turtle()
    ramos.shape("invaders.gif")  # Boss
    ramos.penup()
    ramos.speed(0)
    ramos.setposition(random.randint(-200, 200), 250)
    ramos.direction = 1
    return ramos

def respawn_enemies():
    for enemy in enemies:
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.setposition(x, y)
        enemy.showturtle()

# ---------- CONTROLS ----------
def move_left():
    if game_running:
        player.move_speed = -15

def move_right():
    if game_running:
        player.move_speed = 15

def move_player():
    x = player.xcor() + player.move_speed
    x = max(min(x, 280), -280)
    player.setx(x)

def fire_bullet():
    global bulletstate
    if bulletstate == "ready" and game_running:
        bulletstate = "fire"
        pygame.mixer.Sound("kick.wav").play()
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

# ---------- COLLISIONS ----------
def isCollision(t1, t2):
    distance = math.sqrt((t1.xcor()-t2.xcor())**2 + (t1.ycor()-t2.ycor())**2)
    return distance < 20

# ---------- GAME END ----------
def end_game_and_show_restart():
    global game_running
    game_running = False
    player.hideturtle()
    for enemy in enemies:
        enemy.hideturtle()
    ramos.hideturtle()

    pygame.mixer.music.stop()
    pygame.mixer.Sound("hila.wav").play()
    pygame.time.wait(1000)
    pygame.mixer.Sound("mass.wav").play()
    pygame.time.wait(1000)

    final_pen = turtle.Turtle()
    final_pen.speed(0)
    final_pen.color("white")
    final_pen.penup()
    final_pen.setposition(0, 0)
    final_pen.write(f"Game Over\nFinal Score: {score}", align="center", font=("Arial", 20, "bold"))
    final_pen.hideturtle()

    restart_btn = turtle.Turtle()
    restart_btn.speed(0)
    restart_btn.shape("square")
    restart_btn.color("white")
    restart_btn.penup()
    restart_btn.setposition(0, -50)
    restart_btn.write("Click to Restart", align="center", font=("Arial", 14, "normal"))

    def on_click(x, y):
        restart_btn.clear()
        restart_btn.hideturtle()
        final_pen.clear()
        restart_game()

    turtle.onscreenclick(on_click)

# ---------- GAME LOOP ----------
def game_loop():
    global score, bulletstate, enemyspeed, ramos_speed, ramos_active

    wn.update()
    move_player()

    if score > 100:
        if enemyspeed > 0:
            enemyspeed *= 1.001
        else:
            enemyspeed *= 1.001

    if not ramos_active:
        for enemy in enemies:
            x = enemy.xcor() + enemyspeed
            enemy.setx(x)

            if enemy.xcor() > 280 or enemy.xcor() < -280:
                enemyspeed *= -1
                for e in enemies:
                    e.sety(e.ycor() - 40)

            if isCollision(bullet, enemy):
                pygame.mixer.Sound("goat.wav").play()
                bullet.hideturtle()
                bulletstate = "ready"
                bullet.setposition(0, -400)
                score += 10
                score_pen.clear()
                score_pen.write(f"Score: {score}", False, align="left", font=("Arial", 14, "normal"))
                x = random.randint(-200, 200)
                y = random.randint(100, 250)
                enemy.setposition(x, y)

            if isCollision(player, enemy):
                end_game_and_show_restart()
                return

        # ✅ CHECK if all enemies have moved off-screen
        if all(enemy.ycor() < -280 for enemy in enemies):
            respawn_enemies()

        if score >= 100:
            for enemy in enemies:
                enemy.hideturtle()
            ramos_active = True
            ramos.showturtle()
    else:
        x = ramos.xcor() + ramos_speed * ramos.direction
        ramos.setx(x)

        if x > 280 or x < -280:
            ramos.direction *= -1
            ramos.sety(ramos.ycor() - 40)
            ramos_speed += 0.5

        if isCollision(bullet, ramos):
            pygame.mixer.Sound("goat.wav").play()
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            score += 25
            score_pen.clear()
            score_pen.write(f"Score: {score}", False, align="left", font=("Arial", 14, "normal"))
            ramos.setposition(random.randint(-200, 200), random.randint(100, 250))

        if isCollision(player, ramos):
            end_game_and_show_restart()
            return

    if bulletstate == "fire":
        bullet.sety(bullet.ycor() + 20)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    if game_running:
        wn.ontimer(game_loop, 20)

# ---------- RESTART ----------
def restart_game():
    global score, enemyspeed, bulletstate, game_running, ramos_active, ramos_speed

    score = 0
    enemyspeed = 2
    bulletstate = "ready"
    game_running = True
    ramos_active = False
    ramos_speed = 4

    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)

    score_pen.clear()
    score_pen.write(f"Score: {score}", False, align="left", font=("Arial", 14, "normal"))

    player.showturtle()
    player.setposition(0, -250)

    for enemy in enemies:
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.setposition(x, y)
        enemy.showturtle()

    ramos.hideturtle()
    ramos.setposition(random.randint(-200, 200), 250)

    bullet.hideturtle()
    game_loop()

# ---------- MAIN ----------
wn = setup_screen()
setup_audio()

gif_names = ["invaders_1.gif", "invaders_2.gif", "invaders_3.gif", "invaders_4.gif", "invaders_5.gif", "player.gif", "invaders.gif"]
for gif in gif_names:
    turtle.register_shape(gif)

draw_border()
score_pen = create_score_pen()
score_pen.write(f"Score: {score}", False, align="left", font=("Arial", 14, "normal"))

player = create_player()
enemies = create_enemies()
bullet = create_bullet()
ramos = create_ramos()
ramos.hideturtle()

wn.listen()
wn.onkeypress(move_left, "a")
wn.onkeypress(move_left, "A")  # for Caps Lock

wn.onkeypress(move_right, "d")
wn.onkeypress(move_right, "D")  # for Caps Lock

wn.onkeypress(fire_bullet, "space")


game_loop()
wn.mainloop()


