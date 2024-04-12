import pgzrun
from random import randint

WIDTH = 639
HEIGHT = 426

ship_speed = 2
plasma_speed = 3
saucer_speed = 1
num_saucers = 5

invasions = 0
ship = Actor('ship', (WIDTH / 2, HEIGHT - 80))
plasma = Actor('plasma', (-10, -10))
saucers = []

saucer_y = -10
for i in range(num_saucers):
    saucers.append(Actor('saucer', (randint(0, WIDTH), saucer_y)))
    saucer_y -= 80


def draw():
    """Draw the game screen."""
    screen.blit('stars', (0, 0))
    ship.draw()
    plasma.draw()
    for s in saucers:
        s.draw()

    
def update():
    """Update the actors."""
    global invasions
    
    if keyboard.left and ship.right > 0:
        ship.x -= ship_speed
    elif keyboard.right and ship.left < WIDTH:
        ship.x += ship_speed
    if keyboard.space:
        plasma.midtop = ship.midtop

    if plasma.y > -10:
        plasma.y -= plasma_speed

    for s in saucers:
        s.y += saucer_speed
        if randint(0, 1) == 1:
            s.x += saucer_speed
            if s.x > WIDTH:
                s.x = WIDTH
        else:
            s.x -= saucer_speed
            if s.x < 0:
                s.x = 0
        if s.top > HEIGHT:
            invasions += 1
            reset_saucer(s)


def reset_saucer(s):
    """Reset the saucer to a random position above the top of the screen."""
    s.y = randint(-100, -10)
    s.x = randint(0, WIDTH)


pgzrun.go()