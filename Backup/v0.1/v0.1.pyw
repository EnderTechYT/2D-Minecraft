# Import Libraries
from contextlib import redirect_stdout
import sys, time
with redirect_stdout(None):
    import pygame

pygame.init()

def resource_path(relative_path): # For fixing PyInstaller shit
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Define variabes
background_colour = (88, 174, 245)
dt = 0
grav = 3.6
ply = 0
row = 3
col = 20
fpst = 0
walk = 1

# Load
icon = pygame.image.load("Resources\\icon.png")
dirt_image = pygame.image.load("Resources\\dirt.png")
grass_image = pygame.image.load("Resources\\grass.png")
player_image = pygame.image.load("Resources\\player.png")
player_image2 = pygame.image.load("Resources\\playerright.png")
font = pygame.font.Font("Resources/MC.otf", 32)

# Make Window
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1180, 650))
pygame.display.set_icon(icon)

# Create Characters
player_pos = pygame.Rect(screen.get_width() / 2, screen.get_height() / 2, 60, 60)
ground = pygame.Rect(0, screen.get_height() - 60*row, 12000, 60)
pygame.display.set_caption("2D Minecraft")
screen.fill(background_colour) 
pygame.display.flip() 

# Program running
running = True

# Define functions

def checkx():
    if player_pos.x < -60:
        player_pos.x = screen.get_width()
    elif player_pos.x > screen.get_width():
        player_pos.x = -60

def render():
    screen.fill(background_colour)
    # Draw stuff
    x,y = list(player_image.get_rect())[2],list(player_image.get_rect())[3]
    pygame.draw.rect(screen, "#62ff3b", ground)
    player = pygame.sprite.Sprite()
    if walk == 0:
        player.image = player_image2
    else:
        player.image = player_image
    player.rect = [player_pos.x,player_pos.y-60,x,y]
    screen.blit(player.image, player.rect)
    startx = 1
    starty = 1
    for j in range(row):
        for i in range(col):
            if j+1 != row:
                exec(f"dirt{i} = pygame.sprite.Sprite()")
                exec(f"dirt{i}.image = dirt_image")
                exec(f"dirt{i}.rect = [startx*(i*60),screen.get_height() - 60*(j+1),60,60]")
                exec(f"screen.blit(dirt_image, dirt{i}.rect)")
            elif j+1 == row:
                exec(f"dirt{i} = pygame.sprite.Sprite()")
                exec(f"dirt{i}.image = grass_image")
                exec(f"dirt{i}.rect = [startx*(i*60),screen.get_height() - 60*(j+1),60,60]")
                exec(f"screen.blit(grass_image, dirt{i}.rect)")
        startx = 1
        
def jump():
    global ply
    if player_pos.y == ground.y-60:
        ply = 0 - grav

def gravity(obj):
    global ply
    player_pos.y += ply
    if player_pos.y > obj.y-60:
        ply = 0
        while player_pos.y > obj.y-60:
            player_pos.y -= 1
    else:
        ply += grav * dt

    
    if player_pos.y < 0:
        ply = 0
        while player_pos.y < 0:
            player_pos.y += 1

def showfps():
    if fpst == 1:
        text = font.render(f"FPS: {fps}", True, "black")
        textRect = text.get_rect()
        textRect.center = (70,30)
        screen.blit(text, textRect)

# Game Loop
while running:   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            sys.exit()
    
    pygame.draw.rect(screen, "white", player_pos)
    render()
    showfps()
    gravity(ground)
    checkx()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        running = False
        sys.exit()
    
    if keys[pygame.K_UP]:
        jump()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
        walk = 1
    if keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt
        walk = 0
    if keys[pygame.K_q]:
        if fpst == 0:
            fpst = 1
        elif fpst == 1:
            fpst = 0

    dt = clock.tick() / 1000
    fps = round(clock.get_fps())
    
    pygame.display.flip() # Update screen
