# Ninja, by Mr. Graham

import pgzrun

# Set window size
WIDTH = 1200
HEIGHT = 800

# Constants for player positions
NINJA_X = 80
NINJA_START_Y = 50
ENEMY_X = 900
ENEMY_START_Y = HEIGHT / 2

# Constant for collision detection
COLLISION_DISTANCE = 51

# Global variables
bob = Actor("ninja", (NINJA_X, NINJA_START_Y))
enemy = Actor("enemy")
enemy.x = ENEMY_X
enemy.y = ENEMY_START_Y
enemy_speed = 5
shurikens = []
screen_num = 1

# Pygame Zero hooks

def update():
    """Update the actors."""

    global shurikens, enemy_speed, screen_num

    if screen_num == 2:
        # Move shurikens
        new_shurikens = []  # Temporary list
        for s in shurikens:
            s.x += 15
            s.angle += 10

            # Only put a shuriken in the temporary list
            # if it is still on the screen.
            if s.x < WIDTH:
                new_shurikens.append(s)

        # Move the temporary list into the permanent list.
        shurikens = new_shurikens

        # Move enemy
        enemy.y += enemy_speed
        if enemy.top < 0 or enemy.bottom > HEIGHT:
            enemy_speed = -enemy_speed

        # Check for collisions
        for s in shurikens:
            if s.distance_to(enemy) < COLLISION_DISTANCE:
                screen_num = 3
                shurikens = []


def draw():
    """Draw the game screen."""

    # Draw background
    screen.blit("fuji", (0, 0))

    if screen_num == 1:
        screen.draw.text("Ninja!", center=(WIDTH/2, HEIGHT/2 - 70), color="yellow", fontsize=150)
        screen.draw.text("Click the mouse to begin.", center=(WIDTH/2, HEIGHT/2 + 100), color="green", fontsize=50)

    elif screen_num == 2:
        # Draw player
        bob.draw()

        # Draw shurikens
        for s in shurikens:
            s.draw()

        # Draw enemy
        enemy.draw()

    elif screen_num == 3:
        screen.draw.text("Game over!", center=(WIDTH/2, HEIGHT/2 - 70), color="yellow", fontsize=150)
        screen.draw.text("Click the mouse to play again.", center=(WIDTH/2, HEIGHT/2 + 100), color="green", fontsize=50)


def on_mouse_move(pos):
    """Respond to mouse movement by moving the player to follow the mouse, but only in the Y direction."""
    
    if screen_num == 2:
        x, y = pos
        bob.y = y
        bob.x = NINJA_X


def on_mouse_down(pos):
    """Respond to mouse press by throwing a shuriken."""
    
    global screen_num

    if screen_num == 1 or screen_num == 3:
        screen_num = 2

    # Throw a shuriken, but only 3 can be in flight at a time.
    elif len(shurikens) < 3:
        s = Actor("shuriken")
        x, y = pos
        s.x = NINJA_X + 10
        s.y = y
        shurikens.append(s)


# Start the Pygame Zero engine
pgzrun.go() 
