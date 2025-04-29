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
    
    pygame.mixer.music.load("background_music_2.mp3")
    pygame.mixer.music.play(-1)

# ---------- GLOBAL STATE ----------

score = 0
enemyspeed = 2
speed_increase_threshold = 100
bulletstate = "ready"
game_running = True
enemies_respawned = False

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
    enemies = []
    for _ in range(5):
        enemy = turtle.Turtle()
        enemy.color("red")
        enemy.shape("invaders.gif")
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

# ---------- CONTROLS ----------
def move_left():
    if game_running:
        player.move_speed = -15

def move_right():
    if game_running:
        player.move_speed = 15

def move_player():
    x = player.xcor() + player.move_speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    global bulletstate
    if bulletstate == "ready" and game_running:
        bulletstate = "fire"
        laser_sound = pygame.mixer.Sound("kick.wav")
        laser_sound.play()
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

# ---------- COLLISIONS ----------
def isCollision(t1, t2):
    distance = math.sqrt((t1.xcor()-t2.xcor())**2 + (t1.ycor()-t2.ycor())**2)
    return distance < 15

# ---------- GAME END ----------
def end_game_and_show_restart():
    global game_running
    game_running = False
    player.hideturtle()
    for enemy in enemies:
        enemy.hideturtle()

    pygame.mixer.music.stop()

    hila = pygame.mixer.Sound("hila.wav")
    hila.play()
    while pygame.mixer.get_busy():
        pygame.time.wait(100)

    mass = pygame.mixer.Sound("mass.wav")
    mass.play()
    while pygame.mixer.get_busy():
        pygame.time.wait(100)

    final_pen = turtle.Turtle()
    final_pen.speed(0)
    final_pen.color("white")
    final_pen.penup()
    final_pen.setposition(0, 0)
    final_pen.write(f"Game Over\nFinal Score: {score}", align="center", font=("Arial", 20, "bold"))
    final_pen.hideturtle()

    # Add Restart Button
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
    global score, bulletstate, enemyspeed, speed_increase_threshold, enemies, enemies_respawned

    wn.update()
    move_player()

    all_enemies_off_screen = True

    for enemy in enemies:
        if enemy.ycor() > -300:  # Checking if any enemy is still above the bottom of the screen
            all_enemies_off_screen = False

        x = enemy.xcor() + enemyspeed
        enemy.setx(x)

        if enemy.xcor() > 280 or enemy.xcor() < -280:
            enemyspeed *= -1
            for e in enemies:
                e.sety(e.ycor() - 40)

        if isCollision(bullet, enemy):
            explosion_sound = pygame.mixer.Sound("goat.wav")
            explosion_sound.play()

            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)

            score += 10
            score_pen.clear()
            score_pen.write(f"Score: {score}", False, align="left", font=("Arial", 14, "normal"))

            if score >= speed_increase_threshold:
                enemyspeed += 1 if enemyspeed > 0 else -1
                speed_increase_threshold += 100

            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)

        if isCollision(player, enemy):
            end_game_and_show_restart()
            return


    # Ensure new enemies are only respawned once when all enemies are off-screen
    if all_enemies_off_screen and not enemies_respawned:
        enemies_respawned = True  # Set the flag to avoid respawning again before time
        for enemy in enemies:
            enemy.hideturtle()
        enemies = create_enemies()

    if all_enemies_off_screen and enemies_respawned:  # Reset the flag when new enemies have been spawned
        enemies_respawned = False

    if bulletstate == "fire":
        y = bullet.ycor() + 20
        bullet.sety(y)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

    if game_running:
        wn.ontimer(game_loop, 20)


# ---------- RESTART ----------
def restart_game():
    global score, enemyspeed, speed_increase_threshold, bulletstate, game_running, player, enemies, bullet, score_pen, enemies_respawned

    score = 0
    enemyspeed = 2
    speed_increase_threshold = 100
    bulletstate = "ready"
    game_running = True
    enemies_respawned = False

    pygame.mixer.music.load("background_music_2.mp3")
    pygame.mixer.music.play(-1)

    score_pen.clear()
    score_pen.setposition(-290, 260)
    score_pen.write(f"Score: {score}", False, align="left", font=("Arial", 14, "normal"))

    player.showturtle()
    player.setposition(0, -250)

    for enemy in enemies:
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.setposition(x, y)
        enemy.showturtle()

    bullet.hideturtle()

    game_loop()


# ---------- MAIN ----------
# Setup
wn = setup_screen()
setup_audio()
turtle.register_shape("invaders.gif")
turtle.register_shape("player.gif")

draw_border()
score_pen = create_score_pen()
score_pen.write(f"Score: {score}", False, align="left", font=("Arial", 14, "normal"))

player = create_player()
enemies = create_enemies()
bullet = create_bullet()

# Controls
wn.listen()
wn.onkeypress(move_left, "a")
wn.onkeypress(move_right, "d")
wn.onkeypress(fire_bullet, "space")




# Start Game
game_loop()
wn.mainloop()




