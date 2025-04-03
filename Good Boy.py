import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create the game window
Win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hehe haha")

# Initialize the font
Font = pygame.font.SysFont('comicsans', 30)
    
def draw_start_screen():
    """Display the starting screen."""
    Win.fill((0, 0, 0))  # Black background
    title_text = Font.render("Welcome to a good game!", 1, (255, 255, 255))
    instruction_text = Font.render("Press ENTER to Start", 1, (255, 255, 255))
    Win.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 2 - 50))
    Win.blit(instruction_text, (WIDTH / 2 - instruction_text.get_width() / 2, HEIGHT / 2 + 10))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter key
                waiting = False

def display_good_boy():
    """Display 'Good Boy!!' on the screen."""
    Win.fill((0, 0, 0))  # Black background
    good_boy_text = Font.render("Good Boy!!", 1, (255, 255, 255))
    Win.blit(good_boy_text, (WIDTH / 2 - good_boy_text.get_width() / 2, HEIGHT / 2))
    pygame.display.update()
    pygame.time.delay(2000)  # Display the message for 2 seconds

# Main function to run the game
def main():
    draw_start_screen()  # Show the starting screen
    display_good_boy()  # Show "Good Boy!!" after the starting scree        n
    print("Game Started!")  # Placeholder for the game logic

# Run the game
if __name__ == "__main__":
    main()