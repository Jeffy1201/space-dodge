import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create the game window
Win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hehe haha: The Gameening")

# Font
Font = pygame.font.SysFont('comicsans', 30)
BigFont = pygame.font.SysFont('comicsans', 50)

# Funny colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255)]

def draw_start_screen():
    Win.fill((0, 0, 0))
    title = BigFont.render("Welcome to: hehe haha", True, random.choice(COLORS))
    instruction = Font.render("Press ENTER to yeet into the game", True, (255, 255, 255))
    Win.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 50))
    Win.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2 + 20))
    pygame.display.update()
    wait_for_enter()

def dramatic_loading_screen():
    Win.fill((0, 0, 0))
    loading = Font.render("Loading... probably...", True, random.choice(COLORS))
    Win.blit(loading, (WIDTH//2 - loading.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(1500)

def random_fact_screen():
    facts = [
        "Did you know? Ducks have regional accents.",
        "Fun Fact: Bananas are berries, but strawberries aren't.",
        "This game was made by a committee of raccoons.",
        "You're doing amazing, sweetie.",
        "Fact: This is the best game ever. No bias."
    ]
    Win.fill((0, 0, 0))
    fact = random.choice(facts)
    fact_text = Font.render(fact, True, (255, 255, 255))
    Win.blit(fact_text, (WIDTH//2 - fact_text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(2500)

def display_good_boy():
    Win.fill((0, 0, 0))
    msg = BigFont.render("Good Boy!!", True, random.choice(COLORS))
    Win.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(2000)

def end_screen():
    Win.fill((0, 0, 0))
    msg = Font.render("Game Over... or is it?", True, (255, 255, 255))
    prompt = Font.render("Press ESC to quit, or ENTER to do it all again.", True, (200, 200, 200))
    Win.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 20))
    Win.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 20))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_RETURN:
                    main()

def wait_for_enter():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def main():
    draw_start_screen()
    dramatic_loading_screen()
    random_fact_screen()
    display_good_boy()
    end_screen()

if __name__ == "__main__":
    main()