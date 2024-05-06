# Ninja, by Mr. Graham

import pgzrun
from random import randint

# Set window size
WIDTH = 1200
HEIGHT = 800

# Constants for player positions
NINJA_START_X = 80
NINJA_START_Y = 50
NINJA_MAX_X = 500
ENEMY_MIN_X = 700
ENEMY_START_X = 900
ENEMY_START_Y = HEIGHT / 2
START_SCREEN = 1
WAVE_SCREEN = 2
PLAY_SCREEN = 3
DEAD_SCREEN = 4
END_SCREEN = 5


# Constant for collision detection
COLLISION_DISTANCE = 51

# Global variables
bob = Actor("ninja", (NINJA_START_X, NINJA_START_Y))
health = 3
score = 0
shurikens = []
knives = []
enemies = []
screen_num = START_SCREEN
wave_num = 0

# Class definitions

class Enemy(Actor):

    def __init__(self):
        Actor.__init__(self, "enemy")
        self.x = ENEMY_START_X
        self.y = ENEMY_START_Y
        self.v_speed = randint(-5, 5)
        self.h_speed = randint(-3, 3)

    def update(self):
        self.x += self.h_speed
        self.y += self.v_speed
        if self.right > WIDTH or self.left < ENEMY_MIN_X:
            self.h_speed = -self.h_speed
        if self.top < 0 or self.bottom > HEIGHT:
            self.v_speed = -self.v_speed
        if randint(1, 50) == 1:
            self.throw()

    def throw(self):
        global knives

        if screen_num == PLAY_SCREEN:
            sounds.knife.play()
            knife = Actor("knife", (self.x - 10, self.y))
            knives.append(knife)


# Function definitions

def restart():
    global health, score, shurikens, knives, enemies, screen_num, wave_num
    health = 3
    score = 0
    shurikens = []
    knives = []
    enemies = []
    screen_num = START_SCREEN
    wave_num = 0
    change_image(bob, health)

def make_wave(size):
    wave = []
    for i in range(size):
        wave.append(Enemy())
    return wave

def new_wave():
    global wave_num, enemies, screen_num, shurikens

    shurikens = []
    screen_num = WAVE_SCREEN
    wave_num += 1
    clock.schedule(play_game, 2.0)
    enemies = make_wave(wave_num)

def play_game():
    global screen_num

    print("Let's play!")
    screen_num = PLAY_SCREEN

def change_image(p, h):
    if h == 3:
        p.image = "ninja"
    elif h == 2:
        p.image = "ninja2"
    elif h == 1:
        p.image = "ninja3"
    else:
        p.image = "ninja4"

def end_game():
    global screen_num
    screen_num = END_SCREEN

# Pygame Zero hooks

def update():
    """Update the actors."""

    global shurikens, enemy_speed, screen_num, enemies, score, health, knives

    if screen_num == PLAY_SCREEN or screen_num == DEAD_SCREEN:

        # Move enemies
        for enemy in enemies:
            enemy.update()
 
        # Move shurikens
        new_shurikens = []  # Temporary list
        for s in shurikens:
            s.x += 15
            s.angle += 10

            hit = False
            for enemy in enemies:
                if s.distance_to(enemy) < COLLISION_DISTANCE:
                    enemies.remove(enemy)
                    hit = True
                    score += 1
                    break

            # Only put a shuriken in the temporary list
            # if it is still on the screen.
            if s.x < WIDTH and not hit:
                new_shurikens.append(s)

        # Move the temporary list into the permanent list.
        shurikens = new_shurikens

        # Move knives and check for hits
        new_knives = []
        for k in knives:
            k.x -= 15
            if k.colliderect(bob):
                health -= 1
                change_image(bob, health)
                sounds.eep.play()
                if health <= 0:
                    screen_num = DEAD_SCREEN
                    clock.schedule(end_game, 5.0)
            else:
                new_knives.append(k)
        knives = new_knives

        if len(enemies) == 0:
            new_wave()      



def draw():
    """Draw the game screen."""

    # Draw background
    screen.blit("fuji", (0, 0))

    screen.draw.text(f"Score: {score}", bottomright=(WIDTH - 30, HEIGHT - 30), color="yellow", fontsize=50)

    if screen_num == START_SCREEN:
        screen.draw.text("Ninja!", center=(WIDTH/2, HEIGHT/2 - 70), color="yellow", fontsize=150)
        screen.draw.text("Click the mouse to begin.", center=(WIDTH/2, HEIGHT/2 + 100), color="green", fontsize=50)

    elif screen_num == END_SCREEN:
        screen.draw.text("Game over!", center=(WIDTH/2, HEIGHT/2 - 70), color="yellow", fontsize=150)
        screen.draw.text("Click the mouse to play again.", center=(WIDTH/2, HEIGHT/2 + 100), color="green", fontsize=50)

    elif screen_num == WAVE_SCREEN:
        screen.draw.text(f"Get ready for wave #{wave_num}.", center=(WIDTH/2, HEIGHT/2 - 70), color="yellow", fontsize=50)

    else:
        # Draw player
        bob.draw()

        # Draw shurikens
        for s in shurikens:
            s.draw()

        # Draw enemy
        for enemy in enemies:
            enemy.draw()

        # Draw knives
        for k in knives:
            k.draw()


def on_mouse_move(pos):
    """Respond to mouse movement by moving the player to follow the mouse, but only in the Y direction."""
    
    if screen_num == PLAY_SCREEN:
        x, y = pos
        if x > NINJA_MAX_X:
            x = NINJA_MAX_X
        bob.x = x
        bob.y = y


def on_mouse_down(pos):
    """Respond to mouse press by throwing a shuriken."""
    
    global screen_num

    if screen_num == START_SCREEN:
        new_wave()

    elif screen_num == END_SCREEN:
        restart()
        new_wave()

    # Throw a shuriken, but only 3 can be in flight at a time.
    elif screen_num == PLAY_SCREEN and len(shurikens) < 3:
        sounds.shuriken.play()
        s = Actor("shuriken")
        x, y = pos
        if x > NINJA_MAX_X:
            x = NINJA_MAX_X
        s.x = x + 10
        s.y = y
        shurikens.append(s)


# Start the Pygame Zero engine
pgzrun.go() 
