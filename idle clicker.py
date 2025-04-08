import pygame
import sys
import os
import json
import random

pygame.init()

WIDTH, HEIGHT = 500, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Clicker Game")
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

coins = 0
auto_clickers = [0, 0, 0]  # Three levels of auto-clickers
auto_clicker_base_costs = [10, 100, 1000]  # Base costs for each level
auto_clicker_costs = auto_clicker_base_costs.copy()
auto_clicker_efficiencies = [1, 5, 20]  # Efficiency for each level
auto_clicker_upgrades = [0, 0, 0]  # Upgrade levels for each auto-clicker type
fullscreen = False

# Load background image if available
background_img = None
if os.path.exists("ChatGPT Image Apr 7, 2025, 04_43_50 PM.png"):
    background_img = pygame.image.load("ChatGPT Image Apr 7, 2025, 04_43_50 PM.png").convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Try loading buy button image
buy_img = None
if os.path.exists("buy_button.png"):
    buy_img = pygame.image.load("buy_button.png").convert_alpha()
    buy_img = pygame.transform.scale(buy_img, (300, 50))

# Try loading menu image
menu_img = None
if os.path.exists("28d551717ba939a65dbc6946b50da3f5.png"):
    menu_img = pygame.image.load("28d551717ba939a65dbc6946b50da3f5.png").convert_alpha()
    menu_img = pygame.transform.scale(menu_img, (40, 40))

# Load clicker icon image
clicker_icon = None
if os.path.exists("cursor.png"):
    clicker_icon = pygame.image.load("cursor.png").convert_alpha()
    clicker_icon = pygame.transform.scale(clicker_icon, (24, 24))

# Load auto-clicker icon image
auto_clicker_icon = None
if os.path.exists("left-click.png"):
    auto_clicker_icon = pygame.image.load("left-click.png").convert_alpha()
    auto_clicker_icon = pygame.transform.scale(auto_clicker_icon, (24, 24))

# Try loading clicker image with transparency support
click_img = None
if os.path.exists("clicker.png"):
    click_img = pygame.image.load("clicker.png").convert_alpha()
    click_img = pygame.transform.scale(click_img, (100, 100))

# Try loading coin image
coin_img = None
if os.path.exists("pngimg.com - coin_PNG36871.png"):
    coin_img = pygame.image.load("pngimg.com - coin_PNG36871.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (24, 24))

# Load background music if available
if os.path.exists("Sweet(chosic.com).mp3"):
    pygame.mixer.music.load("Sweet(chosic.com).mp3")
    pygame.mixer.music.play(-1)  # Play the music in a loop

# Button rectangles (positioning buttons at the bottom)
click_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 180, 100, 50)  # Proper height for click button
buy_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)    # Proper height for buy button
sell_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 50)    # Button for selling auto-clickers
menu_button = pygame.Rect(WIDTH - 50, 10, 40, 40)                   # Menu button in the top right corner
restart_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 240, 100, 50) # Restart button just above the click button

# Buttons for buying different amounts and levels of auto-clickers
buy_1_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 100, 100, 50)
buy_5_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 160, 100, 50)
buy_10_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 220, 100, 50)
buy_max_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 280, 100, 50)
upgrade_button = pygame.Rect(WIDTH // 2 + 60, HEIGHT - 180, 100, 50)  # Button for upgrading auto-clickers

show_buy_options = False
show_menu = False
menu_width = WIDTH // 2  # Set menu width to half of the screen width
menu_x = WIDTH

# Achievements
achievements = []
all_achievements = ["Rich Player", "Auto Clicker Master"]

# Save and load functionality
def save_game():
    game_state = {
        "coins": coins,
        "auto_clickers": auto_clickers,
        "auto_clicker_costs": auto_clicker_costs,
        "auto_clicker_upgrades": auto_clicker_upgrades,
        "achievements": achievements
    }
    with open("save_game.json", "w") as save_file:
        json.dump(game_state, save_file)

def load_game():
    global coins, auto_clickers, auto_clicker_costs, auto_clicker_upgrades, achievements
    if os.path.exists("save_game.json"):
        with open("save_game.json", "r") as save_file:
            game_state = json.load(save_file)
            coins = game_state.get("coins", 0)
            auto_clickers = game_state.get("auto_clickers", [0, 0, 0])
            auto_clicker_costs = game_state.get("auto_clicker_costs", auto_clicker_base_costs.copy())
            auto_clicker_upgrades = game_state.get("auto_clicker_upgrades", [0, 0, 0])
            achievements = game_state.get("achievements", [])

load_game()

def reset_game():
    global coins, auto_clickers, auto_clicker_costs, auto_clicker_upgrades, achievements
    coins = 0
    auto_clickers = [0, 0, 0]
    auto_clicker_costs = auto_clicker_base_costs.copy()
    auto_clicker_upgrades = [0, 0, 0]
    achievements = []

clock = pygame.time.Clock()

# Passive income event
PASSIVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PASSIVE_EVENT, 1000)

def calculate_cost(level, quantity):
    total_cost = 0
    cost = auto_clicker_costs[level]
    for _ in range(quantity):
        total_cost += cost
        cost = int(cost * 1.1)  # Reduced cost increment factor
    return total_cost

def calculate_sell_price(level):
    return auto_clicker_costs[level] // 2  # Selling auto-clickers at half the current purchase cost

def check_achievements():
    global achievements
    if coins >= 1000 and "Rich Player" not in achievements:
        achievements.append("Rich Player")
    if sum(auto_clickers) >= 50 and "Auto Clicker Master" not in achievements:
        achievements.append("Auto Clicker Master")

def upgrade_auto_clickers():
    global coins
    for level in range(3):
        upgrade_cost = auto_clicker_base_costs[level] * (auto_clicker_upgrades[level] + 1)
        print(f"Level {level}, Upgrade Cost: {upgrade_cost}, Coins: {coins}, Upgrades: {auto_clicker_upgrades[level]}")  # Debug print
        if coins >= upgrade_cost:
            coins -= upgrade_cost
            auto_clicker_upgrades[level] += 1
            print(f"Upgraded Level {level} Auto-Clicker to {auto_clicker_upgrades[level]}")  # Debug print

def special_ability():
    global coins
    if random.random() < 0.01:  # 1% chance
        coins += random.randint(10, 100)  # Bonus coins

running = True
while running:
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(WHITE)

    # Draw the top right menu image (or a red square if the image is not available)
    if menu_img:
        screen.blit(menu_img, (WIDTH - 50, 10))  # Position it in the top right corner
    else:
        pygame.draw.rect(screen, RED, pygame.Rect(WIDTH - 50, 10, 40, 40))  # Red square fallback

    # Draw coin image and value
    if coin_img:
        screen.blit(coin_img, (20, 20))
        coin_text = font.render(f"x {coins}", True, BLACK)
        screen.blit(coin_text, (50, 20))
    else:
        coin_text = font.render(f"Coins: {coins}", True, BLACK)
        screen.blit(coin_text, (20, 20))

    # Draw the auto-clicker price and count
    for level in range(3):
        auto_clicker_text = font.render(f"Auto Clickers L{level+1}: {auto_clickers[level]}", True, BLACK)
        screen.blit(auto_clicker_text, (20, HEIGHT - 333 + level * 20))
        auto_clicker_cost_text = font.render(f"Cost: {auto_clicker_costs[level]}", True, BLACK)
        screen.blit(auto_clicker_cost_text, (20, HEIGHT - 313 + level * 20))
        upgrade_text = font.render(f"Upgrade L{level+1}: {auto_clicker_upgrades[level]}", True, BLACK)
        screen.blit(upgrade_text, (20, HEIGHT - 293 + level * 20))

    # Draw text for click button (invisible box)
    click_text = font.render("Click", True, BLACK)
    screen.blit(click_text, (click_button.centerx - click_text.get_width() // 2, click_button.centery - click_text.get_height() // 2))

    # Draw main buy button
    buy_text = font.render("Buy", True, BLACK)
    screen.blit(buy_text, (buy_button.centerx - buy_text.get_width() // 2, buy_button.centery - buy_text.get_height() // 2))

    # Draw sell button
    sell_text = font.render("Sell", True, BLACK)
    screen.blit(sell_text, (sell_button.centerx - sell_text.get_width() // 2, sell_button.centery - sell_text.get_height() // 2))

    # Draw restart button
    restart_text = font.render("Restart", True, BLACK)
    screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))

    # Draw upgrade button
    upgrade_button_text = font.render("Upgrade", True, BLACK)
    screen.blit(upgrade_button_text, (upgrade_button.centerx - upgrade_button_text.get_width() // 2, upgrade_button.centery - upgrade_button_text.get_height() // 2))

    # Draw clicker icon
    if clicker_icon:
        screen.blit(clicker_icon, (click_button.right + 10, click_button.centery - clicker_icon.get_height() // 2))

    # Draw auto-clicker icon
    if auto_clicker_icon:
        screen.blit(auto_clicker_icon, (buy_button.right + 10, buy_button.centery - auto_clicker_icon.get_height() // 2))

    if show_buy_options:
        # Draw text for buying different amounts and their costs
        buy_1_text = small_font.render(f"1 ({calculate_cost(0, 1)} coins)", True, BLACK)
        screen.blit(buy_1_text, (buy_1_button.centerx - buy_1_text.get_width() // 2, buy_1_button.centery - buy_1_text.get_height() // 2))

        buy_5_text = small_font.render(f"5 ({calculate_cost(0, 5)} coins)", True, BLACK)
        screen.blit(buy_5_text, (buy_5_button.centerx - buy_5_text.get_width() // 2, buy_5_button.centery - buy_5_text.get_height() // 2))

        buy_10_text = small_font.render(f"10 ({calculate_cost(0, 10)} coins)", True, BLACK)
        screen.blit(buy_10_text, (buy_10_button.centerx - buy_10_text.get_width() // 2, buy_10_button.centery - buy_10_text.get_height() // 2))

        buy_max_cost = calculate_cost(0, auto_clickers[0] + (coins // auto_clicker_costs[0]))  # Calculate max cost based on available coins
        buy_max_text = small_font.render(f"Max ({buy_max_cost} coins)", True, BLACK)
        screen.blit(buy_max_text, (buy_max_button.centerx - buy_max_text.get_width() // 2, buy_max_button.centery - buy_max_text.get_height() // 2))

    if show_menu:
        menu_x -= 10  # Slide the menu from right to left
        if menu_x < WIDTH - menu_width:
            menu_x = WIDTH - menu_width
        
        pygame.draw.rect(screen, WHITE, pygame.Rect(menu_x, 0, menu_width, HEIGHT))  # Draw the menu

        # Display achievements
        achievement_y = 50
        for achievement in all_achievements:
            if achievement in achievements:
                achievement_text = small_font.render(f"{achievement} - Achieved", True, BLACK)
            else:
                achievement_text = small_font.render(f"{achievement} - Not Achieved", True, BLACK)
            screen.blit(achievement_text, (menu_x + 10, achievement_y))
            achievement_y += 30

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
            elif sell_button.collidepoint(event.pos):
                for level in range(3):
                    if auto_clickers[level] > 0:
                        auto_clickers[level] -= 1
                        coins += calculate_sell_price(level)
            elif menu_button.collidepoint(event.pos):
                show_menu = not show_menu  # Toggle the menu
                if not show_menu:
                    menu_x = WIDTH  # Reset menu position if closed
            elif restart_button.collidepoint(event.pos):
                reset_game()
            elif upgrade_button.collidepoint(event.pos):
                upgrade_auto_clickers()
            elif show_buy_options:
                for level in range(3):
                    if buy_1_button.collidepoint(event.pos):
                        if coins >= calculate_cost(level, 1):
                            coins -= calculate_cost(level, 1)
                            auto_clickers[level] += 1
                            auto_clicker_costs[level] = int(auto_clicker_costs[level] * 1.2)  # Reduced cost increment factor
                    elif buy_5_button.collidepoint(event.pos):
                        if coins >= calculate_cost(level, 5):
                            coins -= calculate_cost(level, 5)
                            auto_clickers[level] += 5
                            for _ in range(5):
                                auto_clicker_costs[level] = int(auto_clicker_costs[level] * 1.2)  # Reduced cost increment factor
                    elif buy_10_button.collidepoint(event.pos):
                        if coins >= calculate_cost(level, 10):
                            coins -= calculate_cost(level, 10)
                            auto_clickers[level] += 10
                            for _ in range(10):
                                auto_clicker_costs[level] = int(auto_clicker_costs[level] * 1.2)  # Reduced cost increment factor
                    elif buy_max_button.collidepoint(event.pos):
                        max_clickers = 0
                        while coins >= auto_clicker_costs[level]:
                            coins -= auto_clicker_costs[level]
                            auto_clickers[level] += 1
                            max_clickers += 1
                            auto_clicker_costs[level] = int(auto_clicker_costs[level] * 1.2)  # Reduced cost increment factor
                        buy_max_cost = calculate_cost(level, max_clickers)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

        elif event.type == PASSIVE_EVENT:
            for level in range(3):
                coins += auto_clickers[level] * auto_clicker_efficiencies[level] * (auto_clicker_upgrades[level] + 1)  # Add coins based on the number of auto-clickers and their efficiency
            check_achievements()  # Check for achievements
            special_ability()  # Trigger special ability

    clock.tick(60)

pygame.quit()
sys.exit()

# Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): 2025-04-08 10:33:31
# Current User's Login: Jeffy1201
# Current User's Computer Name: Jeffy1201