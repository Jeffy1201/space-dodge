import pygame
import sys
import os

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
auto_clickers = 0
auto_clicker_cost = 10
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

# Button rectangles (positioning buttons at the bottom)
click_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 180, 100, 50)  # Proper height for click button
buy_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)    # Proper height for buy button
menu_button = pygame.Rect(WIDTH - 50, 10, 40, 40)                   # Menu button in the top right corner

# Buttons for buying different amounts
buy_1_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 100, 100, 50)
buy_5_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 160, 100, 50)
buy_10_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 220, 100, 50)
buy_max_button = pygame.Rect(WIDTH // 2 - 160, HEIGHT - 280, 100, 50)

show_buy_options = False
show_menu = False
menu_width = WIDTH // 3
menu_x = WIDTH

clock = pygame.time.Clock()

# Passive income event
PASSIVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PASSIVE_EVENT, 1000)

def calculate_cost(quantity):
    total_cost = 0
    cost = auto_clicker_cost
    for _ in range(quantity):
        total_cost += cost
        cost = int(cost * 1.5)
    return total_cost

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
    auto_clicker_text = font.render(f"Auto Clickers: {auto_clickers}", True, BLACK)
    screen.blit(auto_clicker_text, (20, HEIGHT - 333))

    auto_clicker_text = font.render(f"Cost: {auto_clicker_cost}", True, BLACK)
    screen.blit(auto_clicker_text, (20, HEIGHT - 313))

    # Draw text for click button (invisible box)
    click_text = font.render("Click", True, BLACK)
    screen.blit(click_text, (click_button.centerx - click_text.get_width() // 2, click_button.centery - click_text.get_height() // 2))

    # Draw main buy button
    buy_text = font.render("Buy", True, BLACK)
    screen.blit(buy_text, (buy_button.centerx - buy_text.get_width() // 2, buy_button.centery - buy_text.get_height() // 2))

    if show_buy_options:
        # Draw text for buying different amounts and their costs
        buy_1_text = small_font.render(f"1 ({calculate_cost(1)} coins)", True, BLACK)
        screen.blit(buy_1_text, (buy_1_button.centerx - buy_1_text.get_width() // 2, buy_1_button.centery - buy_1_text.get_height() // 2))

        buy_5_text = small_font.render(f"5 ({calculate_cost(5)} coins)", True, BLACK)
        screen.blit(buy_5_text, (buy_5_button.centerx - buy_5_text.get_width() // 2, buy_5_button.centery - buy_5_text.get_height() // 2))

        buy_10_text = small_font.render(f"10 ({calculate_cost(10)} coins)", True, BLACK)
        screen.blit(buy_10_text, (buy_10_button.centerx - buy_10_text.get_width() // 2, buy_10_button.centery - buy_10_text.get_height() // 2))

        buy_max_cost = calculate_cost(auto_clickers + (coins // auto_clicker_cost))  # Calculate max cost based on available coins
        buy_max_text = small_font.render(f"Max ({buy_max_cost} coins)", True, BLACK)
        screen.blit(buy_max_text, (buy_max_button.centerx - buy_max_text.get_width() // 2, buy_max_button.centery - buy_max_text.get_height() // 2))

    if show_menu:
        menu_x -= 10  # Slide the menu from right to left
        if menu_x < WIDTH - menu_width:
            menu_x = WIDTH - menu_width
        
        pygame.draw.rect(screen, WHITE, pygame.Rect(menu_x, 0, menu_width, HEIGHT))  # Draw the menu

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click_button.collidepoint(event.pos):
                coins += 1
            elif buy_button.collidepoint(event.pos):
                show_buy_options = not show_buy_options
            elif menu_button.collidepoint(event.pos):
                show_menu = not show_menu  # Toggle the menu
                if not show_menu:
                    menu_x = WIDTH  # Reset menu position if closed
            elif show_buy_options:
                if buy_1_button.collidepoint(event.pos):
                    if coins >= calculate_cost(1):
                        coins -= calculate_cost(1)
                        auto_clickers += 1
                        auto_clicker_cost = int(auto_clicker_cost * 1.5)
                elif buy_5_button.collidepoint(event.pos):
                    if coins >= calculate_cost(5):
                        coins -= calculate_cost(5)
                        auto_clickers += 5
                        for _ in range(5):
                            auto_clicker_cost = int(auto_clicker_cost * 1.5)
                elif buy_10_button.collidepoint(event.pos):
                    if coins >= calculate_cost(10):
                        coins -= calculate_cost(10)
                        auto_clickers += 10
                        for _ in range(10):
                            auto_clicker_cost = int(auto_clicker_cost * 1.5)
                elif buy_max_button.collidepoint(event.pos):
                    max_clickers = 0
                    while coins >= auto_clicker_cost:
                        coins -= auto_clicker_cost
                        auto_clickers += 1
                        max_clickers += 1
                        auto_clicker_cost = int(auto_clicker_cost * 1.5)
                    buy_max_cost = calculate_cost(max_clickers)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

        elif event.type == PASSIVE_EVENT:
            coins += auto_clickers  # Add coins based on the number of auto-clickers

    clock.tick(60)

pygame.quit()
sys.exit()