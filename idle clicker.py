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

# Try loading buy button image
buy_img = None
if os.path.exists("buy_button.png"):
    buy_img = pygame.image.load("buy_button.png")
    buy_img = pygame.transform.scale(buy_img, (300, 50))

# Use a square for the click button
click_button = pygame.Rect(WIDTH // 2 - 50, 100, 100, 100)  # 100x100 square
if buy_img:
    buy_button = buy_img.get_rect(center=(WIDTH // 2, 225))
else:
    buy_button = pygame.Rect(WIDTH // 2 - 150, 200, 300, 50)

clock = pygame.time.Clock()

# Passive income event
PASSIVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PASSIVE_EVENT, 1000)

running = True
while running:
    screen.fill(WHITE)

    # Draw click square
    pygame.draw.rect(screen, (200, 100, 100), click_button)  # Reddish square

    # Draw buy button (image or fallback rectangle)
    if buy_img:
        screen.blit(buy_img, buy_button)
    else:
        pygame.draw.rect(screen, (100, 150, 255), buy_button)

    # Draw text
    coin_text = font.render(f"Coins: {coins}", True, BLACK)
    screen.blit(coin_text, (20, 20))

    auto_text = font.render(f"Auto Clickers: {auto_clickers}", True, BLACK)
    screen.blit(auto_text, (20, 60))

    click_text = font.render("Click Me!", True, BLACK)
    screen.blit(click_text, (click_button.x + 10, click_button.y + 35))

    buy_text = font.render(f"Buy Auto Clicker ({auto_clicker_cost})", True, BLACK)
    screen.blit(buy_text, (buy_button.x + 30, buy_button.y + 10))

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
