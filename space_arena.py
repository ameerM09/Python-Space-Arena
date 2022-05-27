# Module imports
import turtle
import math
import random 
import sys

# Constant variables
SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 620

# Screen setup
win = turtle.Screen()
win.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
win.bgcolor('black')
win.tracer(0)

turtle.register_shape('shooter.gif')
turtle.register_shape('overview.gif')
turtle.register_shape('standby.gif')

pen = turtle.Turtle()
pen.shape('square')
pen.color('white')
pen.speed(0)
pen.penup()
pen.hideturtle()

# Class to create border around the screen which is larger than the window dimensions
class Parameters():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.level = 1

    def level_one(self):
        sprites.clear()

# Retrieve default game objects
        sprites.append(player)
        sprites.append(bullet)

        for level in range(self.level):
            x = random.randint(-self.width / 2, self.width / 2)
            y = random.randint(-self.height / 2, self.height / 2)
            dx = random.randint(-2, 2) / 10
            dy = random.randint(-2, 2) / 10
            sprites.append(Enemy(x, y, 'square', 'red'))
            sprites[-1].dx = dx
            sprites[-1].dy = dy

    def draw_border(self, pen, change_x, change_y):
        pen.color('white')
        pen.width(3.25)
        pen.penup()

        win_left = -self.width / 2 - change_x
        win_right = self.width / 2 - change_x
        win_top = self.height / 2 - change_y
        win_bottom = -self.height / 2 - change_y

        pen.goto(win_left, win_top)
        pen.pendown()
        pen.goto(win_right, win_top)
        pen.goto(win_right, win_bottom)
        pen.goto(win_left, win_bottom)
        pen.goto(win_left, win_top)
        pen.penup()

    def draw_game_info(self, pen, score, active_enemies = 0):
        pen.color('#372255')
        pen.penup()
        pen.goto(400, 0)
        pen.shape('square')
        pen.setheading(90)
        pen.shapesize(stretch_wid = 10, stretch_len = 32)
        pen.stamp()

# Draws a slim border around the game information section
# Uses a turtle module pen to go down the length of the game information section
        pen.color('white')
        pen.width(3)
        pen.goto(300, 400)
        pen.pendown()
        pen.goto(300, -400)

        pen.penup()

# Draws necessary game information here such as number of lives, number of enemies, etc
        character_pen.scale = 1
        character_pen.draw_string(pen, 'SPACE ARENA', 400, 270)
        character_pen.draw_string(pen, 'SCORE {}'.format(score), 400, 220)
        character_pen.draw_string(pen, 'LEVEL {}'.format(run.level), 400, 190)
        character_pen.draw_string(pen, 'LIVES {}'.format(player.lives), 400, 160)

        character_pen.draw_string(pen, 'RADAR', 400, -75)

# Class for all game sprites, objects, etc
class Sprite():
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = 0
        self.dy = 0
        self.da = 0
        self.heading = 0
        self.thrust = 0
        self.acceleration = 0.002
        self.max_health = 100
        self.health = self.max_health
        self.width = 20
        self.height = 20
        self.state = 'active'
        self.view = 200

    def collision_detection(self, other_object):
        if self.x < other_object.x + other_object.width and\
            self.x + self.width > other_object.x and\
            self.y < other_object.y + other_object.height and\
            self.y + self.height > other_object.y:
                return True
        else:
            return False

# Method between different sprites to show the effect of the two hitting one another with force
# Delivers the change in x and y motion between the two sprites
    def sprite_collision(self, other_object):
        change_dx = self.dx
        change_dy = self.dy

        self.dx = other_object.dx
        self.dy = other_object.dy

        other_object.dx = change_dx
        other_object.dy = change_dy

    def update(self):
        self.heading = self.heading + self.da
        self.heading = self.heading % 360

# Application of unit circle to implement game physics
        self.dx = self.dx + math.cos(math.radians(self.heading)) * self.thrust
        self.dy = self.dy + math.sin(math.radians(self.heading)) * self.thrust

        self.x = self.x + self.dx
        self.y = self.y + self.dy

        self.border_collision()

# Method to check for sprite collisions with the screen border
    def border_collision(self):
        if self.x > run.width / 2 - 10:
            self.x = run.width / 2 - 10
            self.dx = self.dx * -1

        elif self.x < run.width / -2 + 10:
            self.x = run.width / -2  + 10
            self.dx = self.dx * -1

        elif self.y > run.height / 2 - 10:
            self.y = run.height / 2 - 10
            self.dy = self.dy * -1

        elif self.y < run.height / -2 + 10:
            self.y = run.height / -2 + 10
            self.dy = self.dy * -1

    def get_sprite(self, pen, change_x, change_y):
        if self.state == 'active':
            pen.goto(self.x - change_x, self.y - change_y)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            self.get_health_meter(pen, change_x, change_y)

# Method to draw health meter below sprites on screen
    def get_health_meter(self, pen, change_x, change_y):
        pen.goto(self.x - change_x - 10, self.y - change_y + 20)
        pen.width(3.25)
        pen.pendown()
        pen.setheading(0)

# Different health meter color based on lower or higher health levels
        if self.health / self.max_health <= 0.35:
            pen.color('red')
        elif self.health / self.max_health <= 0.7:
            pen.color('yellow')
        else:
            pen.color('green')

        pen.fd(20 * (self.health / self.max_health))

# Creates parameters for health meter to show if health ir low or high on bar
        if self.health != self.max_health:
            pen.color('gray')
            pen.fd(20 * ((self.max_health - self.health) / self.max_health))

        pen.penup()

# Uses inheritance of sprite class to bring in all previous methods
# We can add to this subclass with the player's own methods 
class Player(Sprite):
    def __init__(self, x, y, shape = 'triangle', color = 'blue'):
        Sprite.__init__(self, 0, 0, shape, color)
        self.lives = 3
        self.score = 0
        self.heading = 90
        self.da = 0

# Adds realism to game with inertia, change in speed, etc
    def accelerate(self):
        self.thrust = self.thrust + self.acceleration

    def stop_acceleration(self):
        self.thrust = 0

    def left_rotate(self):
        self.da = 2

    def right_rotate(self):
        self.da = -2

    def stop_rotation(self):
        self.da = 0

    def fire_bullet(self):
        bullet.fire_bullet(self.x, self.y, self.heading, self.dx, self.dy)

    def reset(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.heading = 90
        self.health = self.max_health
        self.lives = self.lives - 1

    def update(self):
        if self.state == 'active':
            self.heading = self.heading + self.da
            self.heading = self.heading % 360

            self.dx = self.dx + math.cos(math.radians(self.heading)) * self.thrust
            self.dy = self.dy + math.sin(math.radians(self.heading)) * self.thrust

            self.x = self.x + self.dx
            self.y = self.y + self.dy

            self.border_collision()

            if self.health <= 0:
                self.reset()                

    def get_sprite(self, pen, change_x, change_y):
        pen.goto(self.x - change_x, self.y - change_y)
        pen.shapesize(stretch_wid = 0.5, stretch_len = 1.25)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

        pen.shapesize(stretch_wid = 1, stretch_len = 1)

        self.get_health_meter(pen, change_x, change_y)

# Separate enemy class to make the iteration of other methods easier
class Enemy(Sprite):
    def __init__(self, x, y, shape = 'square', color = 'red'):
        Sprite.__init__(self, x, y, shape, color)
        self.max_health = 20
        self.health = self.max_health
        self.type = random.choice(['shooter', 'overview', 'standby'])

        if self.type == 'shooter':
            self.color = 'red'
            self.shape = 'shooter.gif'
        
        elif self.type == 'overview':
            self.color = 'orange'
            self.shape = 'overview.gif'

        elif self.type == 'standby':
            self.color = 'pink'
            self.shape = 'standby.gif'

    def reset(self):
        self.state = 'inactive'

    def update(self):
        if self.state == 'active':
            self.heading = self.heading + self.da
            self.heading = self.heading % 360

            self.dx = self.dx + math.cos(math.radians(self.heading)) * self.thrust
            self.dy = self.dy + math.sin(math.radians(self.heading)) * self.thrust

            self.x = self.x + self.dx
            self.y = self.y + self.dy

            self.border_collision()

            if self.health <= 0:
                self.reset()

            if self.type == 'shooter':
                if self.x < player.x:
                    self.dx = self.dx + 0.01 
                elif self.x > player.x:
                    self.dx = self.dx - 0.01 
                elif self.y < player.y:
                    self.dy = self.dy + 0.01 
                else:
                    self.dy = self.dy - 0.01 

            elif self.type == 'overview':
                if self.x < player.x:
                    self.dx = self.dx - 0.01 
                elif self.x > player.x:
                    self.dx = self.dx + 0.01 
                elif self.y < player.y:
                    self.dy = self.dy - 0.01 
                else:
                    self.dy = selfdy + 0.01 

            else:
                self.dx = 0
                self.dy = 0

# Subclass of the sprite class through inheritance
# Needs different methods without health meter, etc
class Bullet(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)
        self.state = 'ready'
        self.thrust = 2.5
        self.max_fuel = 200
        self.fuel = self.max_fuel
        self.width = 4
        self.height = 4

    def fire_bullet(self, x, y, heading, dx, dy):
        if self.state == 'ready':
            self.state = 'active'
            self.x = x
            self.y = y
            self.heading = heading
            self.dx = dx
            self.dy = dy

            self.dx = self.dx + math.cos(math.radians(self.heading)) * self.thrust
            self.dy = self.dy + math.sin(math.radians(self.heading)) * self.thrust

    def update(self):
        if self.state == 'active':
            self.fuel = self.fuel - self.thrust
            if self.fuel <= 0:
                self.reset()

            self.heading = self.heading + self.da
            self.heading = self.heading % 360

            self.x = self.x + self.dx
            self.y = self.y + self.dy

            self.border_collision()

    def reset(self):
        self.fuel = self.max_fuel
        self.dx = 0
        self.dy = 0
        self.state = 'ready'

    def get_sprite(self, pen, change_x, change_y):
        if self.state == 'active':
            pen.goto(self.x - change_x, self.y - change_y)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.shapesize(stretch_wid = 0.2, stretch_len = 0.2)
            pen.color(self.color)
            pen.stamp()

            pen.shapesize(stretch_wid = 1, stretch_len = 1)

# Makes game objects move relative to player
# Adds realism for game POV from above
class Movement():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y

class Radar():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height

    def get_radar(self, pen, sprites):
# Draw the circle on the screen for the radar
        pen.color('white')
        pen.setheading(90)
        pen.goto(self.x + self.width / 2, self.y)
        pen.pendown()
        pen.circle(self.width / 2)
        pen.penup()

# Draw scaled version of sprites in radar
        for sprite in sprites:
            if sprite.state == 'active':
                radar_xcor = self.x + (sprite.x - player.x) * (self.width / run.width)
                radar_ycor = self.y + (sprite.y - player.y) * (self.height / run.height)
                pen.goto(radar_xcor, radar_ycor)
                pen.setheading(sprite.heading)
                pen.color(sprite.color)
                pen.shape(sprite.shape)
                pen.shapesize(stretch_wid = 0.25, stretch_len = 0.25)

# Formula to make sure that sprites are within the radar view
                distance = ((player.x - sprite.x) ** 2 + (player.y - sprite.y) ** 2) ** 0.5

                if distance <= player.view:
                    pen.stamp()

class Text():
    def __init__(self, color, scale):
        self.color = color 
        self.scale = scale 

# Getting character dictionary
# Uses screen coordinates to draw customizable letters
        self.characters = {}

        self.characters['1'] = ((-5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters['2'] = ((-5, 10), (5, 10), (5, 0), (-5, -10), (5, -10))
        self.characters['3'] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (5, -10), (5, 0), (-5, 0))
        self.characters['4'] = ((-5, 10), (-5, 0), (5, 0), (5, 10), (5, -10))
        self.characters['5'] = ((5, 10), (-5, 10), (-5, 0), (5, 0), (5, -10), (-5, -10))
        self.characters['6'] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (-5, 0))
        self.characters['7'] = ((-5, 10), (5, 10), (0, -10))
        self.characters['8'] = ((-5, 10), (-5, -10), (5, -10), (5, 10), (-5, 10), (-5, 0), (5, 0))
        self.characters['9'] = ((5, -10), (5, 10), (-5, 10), (-5, 0), (5, 0))
        self.characters['0'] = ((-5, 10), (-5, -10), (5, -10), (5, 10), (-5, 10))

        self.characters['A'] = ((-5, -10), (-5, 10), (5, 10), (5, -10), (5, 0), (-5, 0))
        self.characters['B'] = ((-5, -10), (-5, 10), (3, 10), (3, 3), (-5, 3), (5, 3), (5, -10), (-5, -10))
        self.characters['C'] = ((5, 10), (-5, 10), (-5, -10), (5, -10))
        self.characters['D'] = ((-5, 10), (-5, -10), (5, -8), (5, 8), (-5, 10))
        self.characters["E"] = ((5, 10), (-5, 10), (-5, 0), (0, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["F"] = ((5, 10), (-5, 10), (-5, 0), (5, 0), (-5, 0), (-5, -10))
        self.characters["G"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (0, 0))
        self.characters["H"] = ((-5, 10), (-5, -10), (-5, 0), (5, 0), (5, 10), (5, -10))
        self.characters["I"] = ((-5, 10), (5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters["J"] = ((5, 10), (5, -10), (-5, -10), (-5, 0))   
        self.characters["K"] = ((-5, 10), (-5, -10), (-5, 0), (5, 10), (-5, 0), (5, -10))
        self.characters["L"] = ((-5, 10), (-5, -10), (5, -10))
        self.characters["M"] = ((-5, -10), (-3, 10), (0, 0), (3, 10), (5, -10))
        self.characters["N"] = ((-5, -10), (-5, 10), (5, -10), (5, 10))
        self.characters["O"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))
        self.characters["P"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0))
        self.characters["Q"] = ((5, -10), (-5, -10), (-5, 10), (5, 10), (5, -10), (2, -7), (6, -11))
        self.characters["R"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0), (5, -10))
        self.characters["S"] = ((5, 8), (5, 10), (-5, 10), (-5, 0), (5, 0), (5, -10), (-5, -10), (-5, -8))
        self.characters["T"] = ((-5, 10), (5, 10), (0, 10), (0, -10)) 
        self.characters["V"] = ((-5, 10), (0, -10), (5, 10)) 
        self.characters["U"] = ((-5, 10), (-5, -10), (5, -10), (5, 10)) 
        self.characters["W"] = ((-5, 10), (-3, -10), (0, 0), (3, -10), (5, 10))   
        self.characters["X"] = ((-5, 10), (5, -10), (0, 0), (-5, -10), (5, 10))   
        self.characters["Y"] = ((-5, 10), (0, 0), (5, 10), (0,0), (0, -10))   
        self.characters["Z"] = ((-5, 10), (5, 10), (-5, -10), (5, -10))   

        self.characters['-'] = ((-5, 0), (5, 0))

    def draw_string(self, pen, str, x, y):
        pen.width(2)
        pen.color(self.color)
        
# Center the text depending on the length of the string
# Also looks at the number of characters and adds space between them 
        x = x - 15 * self.scale * ((len(str) - 1) / 2)
        for character in str:
            self.draw_text(pen, character, x, y)
            x = x + 15 * self.scale

    def draw_text(self, pen, character, x, y):
        scale = self.scale
        character = character.upper()

# Check if character being drawn on the screen is in character dictionary 
        if character in self.characters:
            pen.penup()
            xy_cor = self.characters[character][0]
            pen.goto(x + xy_cor[0] * scale, y + xy_cor[1] * scale)
            pen.pendown()

            for index in range(1, len(self.characters[character])):
                xy_cor = self.characters[character][index]
                pen.goto(x + xy_cor[0] * scale, y + xy_cor[1] * scale)
            pen.penup()

# Object to draw text on screen
character_pen = Text('red', 1)

run = Parameters(700, 500)

# Creating game sprites using methods from given class
player = Player(0, 0)

# Creating loop to generate multiple battle bullets
bullet = Bullet(0, 100, 'circle', 'yellow')

# Creating variable for the player movement POV class
movement = Movement(player.x, player.y)

# Create object for the radar
radar = Radar(400, -200, 200, 200)

# List of sprites used in game to keep program more concise
sprites = []

# Sets up first level for player
run.level_one()

# Keyboard bindings to gather user input
win.listen()
win.onkeypress(player.left_rotate, 'Left')
win.onkeypress(player.left_rotate, 'a')
win.onkeypress(player.right_rotate, 'Right')
win.onkeypress(player.right_rotate, 'd')

win.onkeypress(player.accelerate, 'Up')
win.onkeypress(player.accelerate, 'w')
win.onkeyrelease(player.stop_acceleration, 'Up')
win.onkeyrelease(player.stop_acceleration, 'w')

# Stops change in angle of player on screen when key is released
win.onkeyrelease(player.stop_rotation, 'Left')
win.onkeyrelease(player.stop_rotation, 'a')
win.onkeyrelease(player.stop_rotation, 'Right')
win.onkeyrelease(player.stop_rotation, 'd')

# Keyboard binding to shoot missiles
win.onkeypress(player.fire_bullet, 'space')

# Update movements and animations on screen
# Main game loop with continuous actions
while True:
    pen.clear()

    for sprite in sprites:
        sprite.update()

# Update the screen with game actions
# Updates the relative coordinates of game objects
    for sprite in sprites:
        sprite.get_sprite(pen, movement.x + 100, movement.y)

# Using collision checking class to check if objects collide
# Checks if bullet hits the enemy object
    for sprite in sprites:
        if isinstance(sprite, Enemy) and sprite.state == 'active':
            if player.collision_detection(sprite):
                sprite.health = sprite.health - 10
                player.health = player.health - 10
                player.sprite_collision(sprite)

            if bullet.state == 'active' and bullet.collision_detection(sprite):
                sprite.health = sprite.health - 15
                bullet.reset()

            if bullet.state == 'active' and bullet.collision_detection(sprite):
                sprite.x = 100
                sprite.y = -100
                bullet.reset()

    if player.lives <= 0:
        sys.exit()
        print('GAME OVER')

    run.draw_border(pen, movement.x + 100, movement.y)

# Update view throughout the game
    movement.update(player.x, player.y)

# Create game information section on screen
    run.draw_game_info(pen, 0, 0)

# Render the radar on the screen
    radar.get_radar(pen, sprites)

# Checking if level is beat by player
    level_end = True

    for sprite in sprites:
        if isinstance(sprite, Enemy) and sprite.state == 'active':
            level_end = False

    if level_end:
        run.level = run.level + 2 
        run.level_one()

    win.update()