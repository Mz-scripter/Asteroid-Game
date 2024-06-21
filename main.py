import pygame, sys, os, random, math, pygame_gui
from pygame.locals import *
import pygame.locals
import time

#sounds
pygame.mixer.pre_init()
pygame.init()

pygame.init()                      
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 800
HEIGHT = 600      
TIME = 0

#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Asteroids')
        
#load images
bg = pygame.image.load('./images/bg.jpg')
debris = pygame.image.load('./images/debris2_brown.png')
ship = pygame.image.load('./images/ship.png')
ship_thrusted = pygame.image.load('./images/ship_thrusted.png')
asteroid = pygame.image.load('./images/asteroid.png')
shot = pygame.image.load('./images/shot2.png')

#load sounds

#missile sound
missile_sound = pygame.mixer.Sound('./sounds/missile.ogg')
missile_sound.set_volume(1)

#thrust sound
thruster_sound = pygame.mixer.Sound('./sounds/thrust.ogg')
thruster_sound.set_volume(1)

#explosion sound
explosion_sound = pygame.mixer.Sound('./sounds/explosion.ogg')
explosion_sound.set_volume(1)

#background sound
def play_music():
    pygame.mixer.music.load('./sounds/game.ogg')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

play_music()

ship_x = WIDTH/2 - 50
ship_y = HEIGHT/2 - 50
ship_angle = 0
ship_is_rotating = False
ship_is_forward = False
ship_direction = 0
ship_speed = 0
no_asteroids = 5
asteroid_x = [random.randint(90,WIDTH-90) for i in range(no_asteroids)]
asteroid_y = [random.randint(90,HEIGHT-90) for i in range(no_asteroids)]
asteroid_angle = [random.randint(0,360) for i in range(no_asteroids)]
asteroid_speed = 2
bullet_x = []
bullet_y = []
bullet_angle = []
no_bullets = 0
score = 0
with open('data.txt') as data:
    high_score = int(data.read())
game_over = False

def rot_center(image, angle):
    """rotate a Surface, maintaining position."""

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

# draw game function
def draw(canvas):
    global TIME, ship_is_forward, bullet_x
    global ship_is_forward, bullet_y, score, high_score
    canvas.fill(BLACK)
    canvas.blit(bg,(0,0))
    canvas.blit(debris, (TIME*.3,0))
    canvas.blit(debris,(TIME*.3-WIDTH,0))
    TIME = TIME + 1

    for i in range(no_bullets):
        canvas.blit(shot, (bullet_x[i], bullet_y[i]))

    for x,y in zip(asteroid_x, asteroid_y):
        canvas.blit(rot_center(asteroid, TIME), (x,y))

    if ship_is_forward:
        canvas.blit( rot_center(ship_thrusted,ship_angle) , (ship_x, ship_y))
    else:
        canvas.blit( rot_center(ship,ship_angle) , (ship_x, ship_y))
    #draw score
    myfont1 = pygame.font.SysFont('Comic Sans MS', 40)
    label1 = myfont1.render(f"Score: {score} High Score: {high_score}", 1, (255,255,0))
    canvas.blit(label1, (50,20))

    if game_over:
        myfont2 = pygame.font.SysFont("Comic Sans MS", 40)
        label2 = myfont2.render("GAME OVER", 1, (255,255,255))
        canvas.blit(label2, (WIDTH/2 - 150, HEIGHT/2 - 40))


# handle input function
def handle_input():
    global ship_angle, ship_is_rotating, ship_direction, bullet_angle, no_bullets
    global ship_x, ship_y, ship_speed, ship_is_forward, bullet_x, bullet_y
    global thruster_sound, missile_sound

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()   
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                ship_is_rotating = True
                ship_direction = 0
            elif event.key == K_LEFT:
                ship_is_rotating = True
                ship_direction = 1
            elif event.key == K_UP:
                ship_is_forward = True
                ship_speed = 5
                thruster_sound.play()
            elif event.key == K_SPACE:
                bullet_x.append(ship_x + 50)
                bullet_y.append(ship_y + 50)
                bullet_angle.append(ship_angle)
                no_bullets += 1
                missile_sound.play()

        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                ship_is_rotating = False
            else:
                ship_is_forward = False
                thruster_sound.stop()

        

    if ship_is_rotating:
        if ship_direction == 0:
            ship_angle = ship_angle - 10    
        else:
            ship_angle = ship_angle + 10        

    if ship_is_forward or ship_speed > 0:
        ship_x = (ship_x + math.cos(math.radians(ship_angle))*ship_speed )
        ship_y = (ship_y + -math.sin(math.radians(ship_angle))*ship_speed )
        if ship_is_forward == False:
            ship_speed = ship_speed - 0.2

# update the screen
def update_screen():
    pygame.display.update()
    fps.tick(60)

def isCollision(enemyX, enemyY, bulletX, bulletY, num):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < num:
        return True
    else:
        return False

def game_logic():
    global bullet_y, bullet_x, bullet_angle, no_bullets
    global asteroid_x, asteroid_y, score , game_over, high_score
    for i in range(no_bullets):
        bullet_x[i] = (bullet_x[i] + math.cos(math.radians(bullet_angle[i])) * 10)
        bullet_y[i] = (bullet_y[i] + -math.sin(math.radians(bullet_angle[i])) * 10)
    for i in range(no_asteroids):
        asteroid_x[i] = asteroid_x[i] + math.cos(math.radians(asteroid_angle[i])*asteroid_speed) 
        asteroid_y[i] = asteroid_y[i] + -math.sin(math.radians(asteroid_angle[i])*asteroid_speed)
        if asteroid_y[i] < 0:
            asteroid_y[i] = HEIGHT
        if asteroid_y[i] > HEIGHT:
            asteroid_y[i] = 0
        if asteroid_x[i] < 0:
            asteroid_x[i] = WIDTH
        if asteroid_x[i] > WIDTH:
            asteroid_x[i] = 0
        if isCollision(asteroid_x[i], asteroid_y[i], ship_x, ship_y, 45):
            game_over = True
            if score > high_score:
                high_score = score
                with open('data.txt', mode='w') as data:
                    data.write(f"{high_score}")
    for i in range(no_bullets) :
        for j in range(no_asteroids):
            if isCollision(asteroid_x[j], asteroid_y[j], bullet_x[i], bullet_y[i], 60):
                asteroid_x[j] = random.randint(0, WIDTH)
                asteroid_y[j] = random.randint(0, HEIGHT)
                asteroid_angle[j] = random.randint(0, 360)
                explosion_sound.play()
                score += 1


# asteroids game loop
def play_game():
    global game_over, score, no_asteroids
    while True:
        draw(window)
        handle_input()
        if not game_over:
            game_logic()
        if game_over:
            game_over = False
            score = 0
            play_music()
            play_game()
        update_screen()

play_game()