import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
Win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hehe haha: The Gameening")

# Fonts
Font = pygame.font.SysFont('comicsans', 30)
BigFont = pygame.font.SysFont('comicsans', 50)

# Colors
COLORS = [
    (255, 0, 0), (0, 255, 0),
    (0, 255, 255), (255, 255, 0),
    (255, 0, 255), (255, 255, 255)
]

class Game:
    def __init__(self):
        self.screen = "start"
        self.waiting_for_enter = False

    def wait_for_enter(self):
        """Set waiting state to True."""
        print(f"Waiting for ENTER. Current screen: {self.screen}")
        self.waiting_for_enter = True

    def draw_start_screen(self):
        Win.fill((0, 0, 0))
        title = BigFont.render("Welcome to: hehe haha", True, random.choice(COLORS))
        instruction = Font.render("Press ENTER to yeet into the game", True, (255, 255, 255))
        Win.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))
        Win.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 2 + 30))
        pygame.display.update()
        self.wait_for_enter()

    def dramatic_loading_screen(self):
        Win.fill((0, 0, 0))
        loading = Font.render("Loading... probably...", True, random.choice(COLORS))
        Win.blit(loading, (WIDTH // 2 - loading.get_width() // 2, HEIGHT // 2 - 20))
        prompt = Font.render("Press ENTER to continue", True, (200, 200, 200))
        Win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.update()
        self.wait_for_enter()

    def random_fact_screen(self):
        facts = [
            "Did you know? Ducks have regional accents.",
            "Bananas are berries. Strawberries are imposters.",
            "Game certified 100% bug-free (not legally binding).",
            "You're cooler than a polar bear's toenails.",
            "Raccoons helped make this game. Probably."
        ]
        fact = random.choice(facts)
        Win.fill((0, 0, 0))
        fact_text = Font.render(fact, True, (255, 255, 255))
        Win.blit(fact_text, (WIDTH // 2 - fact_text.get_width() // 2, HEIGHT // 2 - 20))
        prompt = Font.render("Press ENTER to continue", True, (200, 200, 200))
        Win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.update()
        self.wait_for_enter()

    def display_good_boy(self):
        Win.fill((0, 0, 0))
        msg = BigFont.render("GOOD BOY!! ", True, random.choice(COLORS))
        Win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
        prompt = Font.render("Press ENTER to continue", True, (200, 200, 200))
        Win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.update()
        self.wait_for_enter()

    def end_screen(self):
        Win.fill((0, 0, 0))
        msg = Font.render("Game Over... or is it?", True, (255, 255, 255))
        prompt = Font.render("Press ESC to quit, or ENTER to do it all again.", True, (200, 200, 200))
        Win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 20))
        Win.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.update()
        self.wait_for_enter()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                print(f"Key pressed: {event.key}, waiting_for_enter: {self.waiting_for_enter}, screen: {self.screen}")
                if event.key == pygame.K_RETURN and self.waiting_for_enter:
                    self.waiting_for_enter = False
                    print(f"ENTER pressed. waiting_for_enter set to {self.waiting_for_enter}")
                elif event.key == pygame.K_RETURN and not self.waiting_for_enter:
                    if self.screen == "start":
                        self.screen = "loading"
                    elif self.screen == "loading":
                        self.screen = "fact"
                    elif self.screen == "fact":
                        self.screen = "good_boy"
                    elif self.screen == "good_boy":
                        self.screen = "end"
                    elif self.screen == "end":
                        self.screen = "start"
                    print(f"Screen changed to {self.screen}")
                if event.key == pygame.K_ESCAPE and self.screen == "end":
                    pygame.quit(); sys.exit()

    def update(self):
        if not self.waiting_for_enter:
            print(f"Updating screen: {self.screen}")
            if self.screen == "start":
                self.draw_start_screen()
            elif self.screen == "loading":
                self.dramatic_loading_screen()
            elif self.screen == "fact":
                self.random_fact_screen()
            elif self.screen == "good_boy":
                self.display_good_boy()
            elif self.screen == "end":
                self.end_screen()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.update()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()