import pgzrun
from random import randint

WIDTH = 639
HEIGHT = 426

ship_speed = 2
plasma_speed = 3
saucer_speed = 1
num_saucers = 5

invasions = 0
score = 0
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
    global score
    
    if keyboard.left and ship.right > 0:
        ship.x -= ship_speed
    elif keyboard.right and ship.left < WIDTH:
        ship.x += ship_speed
    if keyboard.space:
        plasma.midtop = ship.midtop

    if plasma.y > -10:
        plasma.y -= plasma_speed
        for s in saucers:
            if collision(plasma, s):
                pass
                score += 1
                reset_saucer(s)
                reset_plasma()
                sounds.explosion.play()

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


def reset_plasma():
    """Hide the plasma bolt when not in use."""
    plasma.x = -10
    plasma.y = -10


def collision(actor1, actor2):
    """Return True if the two actors are in a collision; otherwise return False."""
    
    vertical1 = actor1.top < actor2.bottom and actor1.top > actor2.top
    vertical2 = actor2.top < actor1.bottom and actor2.top > actor1.top

    horizontal1 = actor1.left < actor2.right and actor1.left > actor2.left
    horizontal2 = actor2.left < actor1.right and actor2.left > actor1.left

    vertical_overlap = vertical1 or vertical2
    horizontal_overlap = horizontal1 or horizontal2

    return vertical_overlap and horizontal_overlap


pgzrun.go()
