# Import Libraries
from contextlib import redirect_stdout
import sys, time, os, platform
with redirect_stdout(None):
    import pygame

pygame.init()
pygame.mixer.init()

# System functions

def resp(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def loadscr():
    font = pygame.font.Font(resp("Resources/MC.otf"), 80)
    text = font.render("Loading..", True, "black")
    textRect = text.get_rect()
    textRect.center = (screen.get_width() / 2, screen.get_height() / 2)
    screen.blit(text, textRect)
    pygame.display.flip()

# Define variabes
background_colour = (88, 174, 245)
dt = 0
grav = 5.6
ply = 0
row = 3
col = 25
fpst = 0
walk = 0
speedx = 0
invs = 0
fs = 0
coords = [1,row]

# Load
icon = pygame.image.load(resp("Resources/icon.png"))
dirt_image = pygame.image.load(resp("Resources/dirt.png"))
grass_image = pygame.image.load(resp("Resources/grass.png"))
player_image = pygame.image.load(resp("Resources/player.png"))
player_image2 = pygame.image.load(resp("Resources/playerright.png"))
hotbar_image = pygame.image.load(resp("Resources/hotbar.png"))
hbsel_image = pygame.image.load(resp("Resources/hbsel.png"))
pygame.mixer.music.load(resp("Resources/bg.mp3"))
pygame.mixer.music.set_volume(0.2)
font = pygame.font.Font(resp("Resources/MC.otf"), 32)

# Make Window
clock = pygame.time.Clock()
if fs == 1:
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((1180, 650))
pygame.display.set_icon(icon)
pygame.display.set_caption("2D Minecraft")
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

loadscr() # Loading Screen
pygame.time.delay(100)

# Create Characters
player_pos = pygame.Rect(30, screen.get_height() / 2, 60, 60)
ground = pygame.Rect(0, screen.get_height() - 60*row, 12000, 60)
pygame.display.flip() 

# Program running
running = True

# Define functions
def checkx():
    if player_pos.x < -60:
        player_pos.x = screen.get_width()
    elif player_pos.x > screen.get_width():
        player_pos.x = -60

def quit_():
    running = False
    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


def renderdirt():
    global coords
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
                exec(f"coords = ({i}, row)")
        startx = 1

def render():
    screen.fill(background_colour)
    # Draw stuff
    harea = list(hotbar_image.get_rect())[2:]
    hbsa = list(hbsel_image.get_rect())[2:]
    hotbar = pygame.sprite.Sprite()
    hotbar.image = hotbar_image
    hotbar.rect = [(screen.get_width() / 2) - harea[0] / 2, screen.get_height() - 80, harea[0], harea[1]]

    hbsel = pygame.sprite.Sprite()
    hbsel.image = hbsel_image
    hbsel.rect = [(screen.get_width() / 2) - harea[0] / 2 + 60 * invs, screen.get_height() - 80, hbsa[0], hbsa[1]]
    
    x,y = list(player_image.get_rect())[2],list(player_image.get_rect())[3]
    pygame.draw.rect(screen, "#62ff3b", ground)
    player = pygame.sprite.Sprite()
    if walk == 0:
        player.image = player_image2
    else:
        player.image = player_image
    player.rect = [player_pos.x,player_pos.y-60,x,y]

    # Render charactera
    screen.blit(player.image, player.rect)
    renderdirt()

    # Render GUI
    screen.blit(hotbar.image, hotbar.rect)
    screen.blit(hbsel.image, hbsel.rect)
    
def pause():
    global running
    running = False
    pygame.mixer.music.pause()
    

def jump():
    global ply
    if player_pos.y == ground.y-60:
        ply = 0 - grav

def gravity(obj):
    global ply
    player_pos.y += ply
    ply += 0.1
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

def momentum():
    global speedx
    player_pos.x += speedx
    if walk == 0:
        if speedx > 0:
            speedx += -1
            
    if walk == 1:
        if speedx < 0:
            speedx += 1

def showdets():
    text = font.render(f"FPS: {fps}", True, "black")
    textRect = text.get_rect()
    textRect.center = (70,30)
    screen.blit(text, textRect)

    text = font.render(platform.processor(), True, "black")
    textRect = text.get_rect()
    textRect.center = ((screen.get_width() - text.get_width() / 2) - 10,30)
    screen.blit(text, textRect)
    
    text = font.render(platform.platform(), True, "black")
    textRect = text.get_rect()
    textRect.center = ((screen.get_width() - text.get_width() / 2) - 10,70)
    screen.blit(text, textRect)

    text = font.render(f"{coords[0]}x{coords[1]}", True, "black")
    textRect = text.get_rect()
    textRect.center = (70,70)
    screen.blit(text, textRect)

# Game Loop
if running:
    pygame.mixer.music.play()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_()
    
    pygame.draw.rect(screen, "white", player_pos)
    render()
    gravity(ground)
    momentum()
    checkx()
    if fpst == 1:
        showdets()


    dt = clock.tick(60) / 1000
    fps = round(clock.get_fps())
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        quit_()
        #pause()
    
    if keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
        jump()
        
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        '''player_pos.x -= 300 * dt'''
        walk = 1
        speedx = -7
        
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        '''player_pos.x += 300 * dt'''
        walk = 0
        speedx = 7
        
    if keys[pygame.K_F3]:
        if fpst == 0:
            fpst = 1
            pygame.time.delay(10)
        elif fpst == 1:
            fpst = 0
            pygame.time.delay(10)
            
    for i in range(9): # Hotbar Item Selection
        exec(f"if keys[pygame.K_{i+1}]: invs = {i}")
    
    '''                                         FULL SCREEN TOGGLE FAILED      
    if keys[pygame.K_F11]:
        if fs == 0:
            fs = 1
            screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            ground = pygame.Rect(0, screen.get_height() - 60*row, 12000, 60)
            player_pos = pygame.Rect(player_pos.x, player_pos.y, 60, 60)
        elif fs == 1:
            fs = 0
            screen = pygame.display.set_mode((1180, 650))
            ground = pygame.Rect(0, screen.get_height() - 60*row, 12000, 60)
            player_pos = pygame.Rect(player_pos.x, player_pos.y, 60, 60)'''
        
    pygame.display.flip() # Update screen
