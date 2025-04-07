import pygame
import sys
import os

pygame.init()

WIDTH, HEIGHT = 500, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Clicker Game")
font = pygame.font.SysFont("Arial", 24)

coins = 0
auto_clickers = 0
auto_clicker_cost = 10

# Load background image if available
background_img = None
if os.path.exists("background.png"):
    background_img = pygame.image.load("background.png").convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Try loading buy button image
buy_img = None
if os.path.exists("buy_button.png"):
    buy_img = pygame.image.load("buy_button.png").convert_alpha()
    buy_img = pygame.transform.scale(buy_img, (300, 50))

# Try loading clicker image with transparency support
click_img = None
if os.path.exists("clicker.png"):
    click_img = pygame.image.load("clicker.png").convert_alpha()
    click_img = pygame.transform.scale(click_img, (100, 100))

# Try loading coin image
coin_img = None
if os.path.exists("coin.png"):
    coin_img = pygame.image.load("coin.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (24, 24))

# Button rectangles
click_button = pygame.Rect(WIDTH // 2 - 50, 100, 100, 100)
buy_button = pygame.Rect(WIDTH // 2 - 150, 200, 300, 50)

clock = pygame.time.Clock()

# Passive income event
PASSIVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PASSIVE_EVENT, 1000)

running = True
while running:
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(WHITE)

    # Draw clicker image or fallback square
    if click_img:
        screen.blit(click_img, click_button)
    else:
        pygame.draw.rect(screen, (0, 100, 255), click_button)  # Blue box

    # Draw buy button (image or fallback rectangle)
    if buy_img:
        screen.blit(buy_img, buy_button)
    else:
        pygame.draw.rect(screen, (0, 100, 255), buy_button)  # Blue box

    # Draw coin image and value
    if coin_img:
        screen.blit(coin_img, (20, 20))
        coin_text = font.render(f"x {coins}", True, BLACK)
        screen.blit(coin_text, (50, 20))
    else:
        coin_text = font.render(f"Coins: {coins}", True, BLACK)
        screen.blit(coin_text, (20, 20))

    # Add text to blue boxes
    click_text = font.render("Click", True, WHITE)
    screen.blit(click_text, (click_button.centerx - click_text.get_width() // 2, click_button.centery - click_text.get_height() // 2))

    buy_text = font.render("Buy Auto Clicker", True, WHITE)
    screen.blit(buy_text, (buy_button.centerx - buy_text.get_width() // 2, buy_button.centery - buy_text.get_height() // 2))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if click_button.collidepoint(event.pos):
                coins += 1
            elif buy_button.collidepoint(event.pos):
                if coins >= auto_clicker_cost:
                    coins -= auto_clicker_cost
                    auto_clickers += 1
                    auto_clicker_cost = int(auto_clicker_cost * 1.5)

        elif event.type == PASSIVE_EVENT:
            coins += auto_clickers

    clock.tick(60)

pygame.quit()
sys.exit()