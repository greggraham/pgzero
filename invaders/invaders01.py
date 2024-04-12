import pgzrun

WIDTH = 639
HEIGHT = 426

ship = Actor('ship', (WIDTH / 2, HEIGHT - 80))

def draw():
    """Draw the game screen."""
    screen.blit('stars', (0, 0))
    ship.draw()

pgzrun.go()