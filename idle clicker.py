import pygame
import sys
import os
import json

pygame.init()

WIDTH, HEIGHT = 500, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Clicker Game")
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

# Game state
coins = 0
auto_clickers = 0
super_auto_clickers = 0
mega_auto_clickers = 0

# Costs
auto_clicker_cost = 10
super_auto_clicker_cost = 100
mega_auto_clicker_cost = 100

# Upgrade system
upgrade_level = 0

# Achievements
achievements = []
all_achievements = ["Rich Player", "Auto Clicker Master"]

# Flags
fullscreen = False
show_buy_options = False
show_menu = False
menu_width = WIDTH // 2
menu_x = WIDTH

# Load assets
background_img = pygame.image.load("background.png").convert() if os.path.exists("background.png") else None
click_img = pygame.image.load("clicker.png").convert_alpha() if os.path.exists("clicker.png") else None
coin_img = pygame.image.load("coin.png").convert_alpha() if os.path.exists("coin.png") else None
menu_img = pygame.image.load("28d551717ba939a65dbc6946b50da3f5.png").convert_alpha() if os.path.exists("28d551717ba939a65dbc6946b50da3f5.png") else None
clicker_icon = pygame.image.load("cursor.png").convert_alpha() if os.path.exists("cursor.png") else None
auto_clicker_icon = pygame.image.load("left-click.png").convert_alpha() if os.path.exists("left-click.png") else None

if background_img:
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
if menu_img:
    menu_img = pygame.transform.scale(menu_img, (40, 40))
if coin_img:
    coin_img = pygame.transform.scale(coin_img, (24, 24))
if clicker_icon:
    clicker_icon = pygame.transform.scale(clicker_icon, (24, 24))
if auto_clicker_icon:
    auto_clicker_icon = pygame.transform.scale(auto_clicker_icon, (24, 24))

# Music
if os.path.exists("Sweet(chosic.com).mp3"):
    pygame.mixer.music.load("Sweet(chosic.com).mp3")
    pygame.mixer.music.play(-1)

# Buttons
click_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 180, 100, 50)
buy_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)
sell_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 50)
restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 240, 100, 50)
menu_button = pygame.Rect(WIDTH - 50, 10, 40, 40)

buy_1_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 100, 100, 50)
buy_5_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 160, 100, 50)
buy_10_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 220, 100, 50)
buy_max_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 280, 100, 50)

super_auto_clicker_button = pygame.Rect(WIDTH // 4 - 50, HEIGHT - 130, 200, 50)
mega_auto_clicker_button = pygame.Rect(WIDTH // 4 - 50, HEIGHT - 60, 200, 50)

# Save/load

def save_game():
    game_state = {
        "coins": coins,
        "auto_clickers": auto_clickers,
        "super_auto_clickers": super_auto_clickers,
        "mega_auto_clickers": mega_auto_clickers,
        "auto_clicker_cost": auto_clicker_cost,
        "super_auto_clicker_cost": super_auto_clicker_cost,
        "mega_auto_clicker_cost": mega_auto_clicker_cost,
        "upgrade_level": upgrade_level,
        "achievements": achievements
    }
    with open("save_game.json", "w") as f:
        json.dump(game_state, f)

def load_game():
    global coins, auto_clickers, super_auto_clickers, mega_auto_clickers
    global auto_clicker_cost, super_auto_clicker_cost, mega_auto_clicker_cost
    global upgrade_level, achievements
    if os.path.exists("save_game.json"):
        with open("save_game.json", "r") as f:
            data = json.load(f)
            coins = data.get("coins", 0)
            auto_clickers = data.get("auto_clickers", 0)
            super_auto_clickers = data.get("super_auto_clickers", 0)
            mega_auto_clickers = data.get("mega_auto_clickers", 0)
            auto_clicker_cost = data.get("auto_clicker_cost", 10)
            super_auto_clicker_cost = data.get("super_auto_clicker_cost", 100)
            mega_auto_clicker_cost = data.get("mega_auto_clicker_cost", 100)
            upgrade_level = data.get("upgrade_level", 0)
            achievements = data.get("achievements", [])

def reset_game():
    global coins, auto_clickers, super_auto_clickers, mega_auto_clickers
    global auto_clicker_cost, super_auto_clicker_cost, mega_auto_clicker_cost
    global upgrade_level, achievements
    coins = 0
    auto_clickers = 0
    super_auto_clickers = 0
    mega_auto_clickers = 0
    auto_clicker_cost = 10
    super_auto_clicker_cost = 100
    mega_auto_clicker_cost = 100
    upgrade_level = 0
    achievements = []

# Utility
def calculate_cost(qty):
    cost = auto_clicker_cost
    total = 0
    for _ in range(qty):
        total += cost
        cost = int(cost * 1.2)
    return total

def calculate_sell_price():
    return auto_clicker_cost // 2

def check_achievements():
    if coins >= 1000 and "Rich Player" not in achievements:
        achievements.append("Rich Player")
    if auto_clickers >= 50 and "Auto Clicker Master" not in achievements:
        achievements.append("Auto Clicker Master")

# Events
PASSIVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PASSIVE_EVENT, 1000)
clock = pygame.time.Clock()
load_game()

running = True
while running:
    screen.blit(background_img, (0, 0)) if background_img else screen.fill(WHITE)
    
    # UI draw
    if menu_img:
        screen.blit(menu_img, menu_button)
    else:
        pygame.draw.rect(screen, RED, menu_button)

    if coin_img:
        screen.blit(coin_img, (20, 20))
        screen.blit(font.render(f"x {coins}", True, BLACK), (50, 20))
    else:
        screen.blit(font.render(f"Coins: {coins}", True, BLACK), (20, 20))

    screen.blit(font.render(f"Auto Clickers: {auto_clickers}", True, BLACK), (20, 60))
    screen.blit(font.render(f"Super Auto Clickers: {super_auto_clickers}", True, BLACK), (20, 100))
    screen.blit(font.render(f"Mega Auto Clickers: {mega_auto_clickers}", True, BLACK), (20, 140))

    screen.blit(font.render("Click", True, BLACK), click_button.topleft)
    screen.blit(font.render("Buy", True, BLACK), buy_button.topleft)
    screen.blit(font.render("Sell", True, BLACK), sell_button.topleft)
    screen.blit(font.render("Restart", True, BLACK), restart_button.topleft)

    if show_buy_options:
        screen.blit(small_font.render(f"1 ({calculate_cost(1)} coins)", True, BLACK), buy_1_button.topleft)
        screen.blit(small_font.render(f"5 ({calculate_cost(5)} coins)", True, BLACK), buy_5_button.topleft)
        screen.blit(small_font.render(f"10 ({calculate_cost(10)} coins)", True, BLACK), buy_10_button.topleft)
        screen.blit(small_font.render("Max", True, BLACK), buy_max_button.topleft)

    if show_menu:
        menu_x -= 10
        if menu_x < WIDTH - menu_width:
            menu_x = WIDTH - menu_width
        pygame.draw.rect(screen, WHITE, pygame.Rect(menu_x, 0, menu_width, HEIGHT))
        y = 50
        for ach in all_achievements:
            label = f"{ach} - {'Achieved' if ach in achievements else 'Not Achieved'}"
            screen.blit(small_font.render(label, True, BLACK), (menu_x + 10, y))
            y += 30

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click_button.collidepoint(event.pos):
                coins += 1
            elif buy_button.collidepoint(event.pos):
                show_buy_options = not show_buy_options
            elif sell_button.collidepoint(event.pos) and auto_clickers > 0:
                auto_clickers -= 1
                coins += calculate_sell_price()
            elif menu_button.collidepoint(event.pos):
                show_menu = not show_menu
                if not show_menu:
                    menu_x = WIDTH
            elif restart_button.collidepoint(event.pos):
                reset_game()
            elif show_buy_options:
                if buy_1_button.collidepoint(event.pos) and coins >= calculate_cost(1):
                    coins -= calculate_cost(1)
                    auto_clickers += 1
                    auto_clicker_cost = int(auto_clicker_cost * 1.2)
                elif buy_5_button.collidepoint(event.pos) and coins >= calculate_cost(5):
                    coins -= calculate_cost(5)
                    auto_clickers += 5
                    for _ in range(5): auto_clicker_cost = int(auto_clicker_cost * 1.2)
                elif buy_10_button.collidepoint(event.pos) and coins >= calculate_cost(10):
                    coins -= calculate_cost(10)
                    auto_clickers += 10
                    for _ in range(10): auto_clicker_cost = int(auto_clicker_cost * 1.2)
                elif buy_max_button.collidepoint(event.pos):
                    while coins >= auto_clicker_cost:
                        coins -= auto_clicker_cost
                        auto_clickers += 1
                        auto_clicker_cost = int(auto_clicker_cost * 1.2)
            elif show_menu:
                if super_auto_clicker_button.collidepoint(event.pos) and coins >= super_auto_clicker_cost:
                    coins -= super_auto_clicker_cost
                    super_auto_clickers += 1
                    super_auto_clicker_cost = int(super_auto_clicker_cost * 1.3)
                elif mega_auto_clicker_button.collidepoint(event.pos) and coins >= mega_auto_clicker_cost:
                    coins -= mega_auto_clicker_cost
                    mega_auto_clickers += 1
                    mega_auto_clicker_cost = int(mega_auto_clicker_cost * 1.3)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if fullscreen else 0)

        elif event.type == PASSIVE_EVENT:
            coins += auto_clickers + (super_auto_clickers * 5) + (mega_auto_clickers * 10)
            check_achievements()

    clock.tick(60)

pygame.quit()
sys.exit()
