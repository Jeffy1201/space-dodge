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

coins = 0
auto_clickers = 0
auto_clicker_cost = 10

# Load background image if available
background_img = None
if os.path.exists("ChatGPT Image Apr 7, 2025, 04_43_50 PM.png"):
    background_img = pygame.image.load("ChatGPT Image Apr 7, 2025, 04_43_50 PM.png").convert()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load top image if available (will use as top bar)
top_img = None
if os.path.exists("5f463070803a0d0004146b6e.png"):  # Replace with the actual image path
    top_img = pygame.image.load("5f463070803a0d0004146b6e.png").convert_alpha()
    top_img = pygame.transform.scale(top_img, (WIDTH - 300, 200))  # Resize to fit the top

# Position the image slightly below the top
top_x = (WIDTH - (WIDTH - 300)) // 2  # Center it horizontally
top_y = 20  # Move the image 20 pixels down from the top

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
if os.path.exists("pngimg.com - coin_PNG36871.png"):
    coin_img = pygame.image.load("pngimg.com - coin_PNG36871.png").convert_alpha()
    coin_img = pygame.transform.scale(coin_img, (24, 24))

# Button rectangles (positioning buttons at the bottom)
click_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 180, 100, 50)  # Proper height for click button
buy_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 100, 300, 50)    # Proper height for buy button

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

    # Draw the top image (or a red square if the image is not available)
    if top_img:
        screen.blit(top_img, (top_x, top_y))  # Position it slightly below the top
    else:
        pygame.draw.rect(screen, RED, pygame.Rect(0, 0, WIDTH, 50))  # Red square fallback

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

    auto_clicker_text = font.render (f"Cost: {auto_clicker_cost})", True, BLACK)
    screen.blit(auto_clicker_text, (20, HEIGHT - 313))

    # Draw text for click button (invisible box)
    click_text = font.render("Click", True, BLACK)
    screen.blit(click_text, (click_button.centerx - click_text.get_width() // 2, click_button.centery - click_text.get_height() // 2))

    # Draw text for buy button (invisible box)
    buy_text = font.render("Buy Auto Clicker", True, BLACK)
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
                    auto_clicker_cost = int(auto_clicker_cost * 1.5)  # Increase the cost for the next auto-clicker

        elif event.type == PASSIVE_EVENT:
            coins += auto_clickers  # Add coins based on the number of auto-clickers

    clock.tick(60)

pygame.quit()
sys.exit()
