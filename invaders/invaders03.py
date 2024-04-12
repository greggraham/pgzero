import pgzrun

WIDTH = 639
HEIGHT = 426

ship_speed = 2
plasma_speed = 3

ship = Actor('ship', (WIDTH / 2, HEIGHT - 80))
plasma = Actor('plasma', (-10, -10))

def draw():
    """Draw the game screen."""
    screen.blit('stars', (0, 0))
    ship.draw()
    plasma.draw()

    
def update():
    """Update the actors."""
    if keyboard.left and ship.right > 0:
        ship.x -= ship_speed
    elif keyboard.right and ship.left < WIDTH:
        ship.x += ship_speed
    if keyboard.space:
        plasma.midtop = ship.midtop

    if plasma.y > -10:
        plasma.y -= plasma_speed


pgzrun.go()