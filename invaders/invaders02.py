import pgzrun

WIDTH = 639
HEIGHT = 426

ship_speed = 2

ship = Actor('ship', (WIDTH / 2, HEIGHT - 80))

def draw():
    """Draw the game screen."""
    screen.blit('stars', (0, 0))
    ship.draw()

    
def update():
    """Update the actors."""
    if keyboard.left and ship.right > 0:
        ship.x -= ship_speed
    elif keyboard.right and ship.left < WIDTH:
        ship.x += ship_speed


pgzrun.go()