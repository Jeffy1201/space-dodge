# Space Game - Main Code

# Import necessary libraries
import pygame
import sys
import time
import random

# Initialize Pygame
pygame.font.init()
pygame.init()

# Game Window Setup
WIDTH, HEIGHT = 1000, 800
Win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space")

# Load Background Image
try:
    image = pygame.image.load("AdobeStock_81556974.webp")
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
except pygame.error:
    print("Background image not found. Using a solid color instead.")
    image = pygame.Surface((WIDTH, HEIGHT))
    image.fill((0, 0, 0))  # Black background

# Background scrolling variables
background_y = 0  # Initial vertical position of the background
background_scroll_speed = 2  # Speed of the background scrolling

# Game Constants
PLAYER_WIDTH, PLAYER_HEIGHT = 70, 120  # Adjusted for spaceship size
SHIELD_WIDTH, SHIELD_HEIGHT = 100, 20
PLAYER_VEL = 5
STAR_WIDTH, STAR_HEIGHT = 10, 20
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
BULLET_VEL = 7
BASE_STAR_VEL = 5  # Base velocity, will increase with levels
BASE_STAR_ADD_INTERVAL = 2000  # Base interval, decreases with levels

# Colors and Fonts
Font = pygame.font.SysFont('comicsans', 30)
PLAYER_COLOR, STAR_COLOR, PLAYER_SHIELD, BULLET_COLOR = (255, 0, 0), (255, 255, 255), (0, 0, 255), (255, 0, 0)

# Player and Shield Initial Positions
player_x, player_y = WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 10
shield_x, shield_y = player_x, player_y - SHIELD_HEIGHT - 10

# Game Variables
high_score = 0
score = 0  # Global score
level = 1  # Track level
lives = 3  # Player lives
difficulty = "Medium"  # Default difficulty

# Double Damage Variables
double_damage_active = False
double_damage_timer = 0  # Timer for how long the power-up lasts

# Load Sounds
pygame.mixer.init()
try:
    pygame.mixer.music.load("retro-gaming-271301.mp3")  # Use music.load for MP3
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Loop indefinitely
    collision_sound = pygame.mixer.Sound("ouchmp3-14591.mp3")
    power_up_sound = pygame.mixer.Sound("power-up-type-1-230548.mp3")
    shoot_sound = pygame.mixer.Sound("shooting-star-2-104073.mp3")
except pygame.error as e:
    print(f"Error loading sounds: {e}")

# High Score Persistence
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Enemy Class
class Enemy:
    def __init__(self, x, y, width, height, speed, shoots=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.shoots = shoots
        self.bullets = []  # Bullets shot by this enemy

    def move(self):
        """Move the enemy down the screen."""
        self.rect.y += self.speed

    def shoot(self):
        """Shoot bullets if the enemy can shoot."""
        if self.shoots and random.random() < 0.02:  # 2% chance to shoot per frame
            bullet = pygame.Rect(self.rect.centerx - BULLET_WIDTH // 2, self.rect.bottom, BULLET_WIDTH, BULLET_HEIGHT)
            self.bullets.append(bullet)

    def update_bullets(self):
        """Update the position of bullets shot by this enemy."""
        for bullet in self.bullets[:]:
            bullet.y += BULLET_VEL  # Enemy bullets move downward
            if bullet.y > HEIGHT:
                self.bullets.remove(bullet)

# Starting Screen
def draw_start_screen():
    """Display the starting screen."""
    global high_score, difficulty
    Win.fill((0, 0, 0))
    texts = [
        "Welcome to Space Doge!",
        "Press SPACE to Start",
        f"High Score: {high_score}",
        "Press 1 for Easy, 2 for Medium, 3 for Hard"
    ]
    for i, text in enumerate(texts):
        rendered = Font.render(text, 1, (255, 255, 255))
        Win.blit(rendered, (WIDTH / 2 - rendered.get_width() / 2, HEIGHT / 2 - 50 + i * 50))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_1:
                    difficulty = "Easy"
                    return
                if event.key == pygame.K_2:
                    difficulty = "Medium"
                    return
                if event.key == pygame.K_3:
                    difficulty = "Hard"
                    return

# Game Over Screen
def game_over_screen():
    """Display the game over screen."""
    global high_score, score, level
    if score > high_score:
        high_score = score
        # Save the new high score to a file
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

    # Fill the screen with a black background
    Win.fill((0, 0, 0))

    # Display Game Over text and stats
    texts = [
        "Game Over!",
        f"Final Score: {score}",
        f"High Score: {high_score}",
        f"Level Reached: {level}",
        "Press R to Restart or Q to Quit"
    ]
    for i, text in enumerate(texts):
        rendered_text = Font.render(text, 1, (255, 255, 255))
        Win.blit(rendered_text, (WIDTH / 2 - rendered_text.get_width() / 2, HEIGHT / 2 - 50 + i * 50))

    pygame.display.update()

    # Wait for user input to restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()

# Load Player Image
try:
    player_image = pygame.image.load("game1201.png")  # Replace with your image file
    player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))  # Scale to player size
except pygame.error:
    print("Player image not found. Using a red rectangle instead.")
    player_image = None  # Fallback to rectangle if image is not found

# Game Drawing Function
def draw(player_rect, elapsed_time, stars, shield_rect, shield_visible, score, level, lives, power_ups, enemies, bullets, boss_rect=None, boss_stars=None, boss_health=None):
    """Draw all game elements."""
    # Draw scrolling background
    Win.blit(image, (0, background_y))  # Draw the main background
    Win.blit(image, (0, background_y - HEIGHT))  # Draw the background above it for seamless scrolling

    stats = [f"Time: {round(elapsed_time)}s", f"Score: {score}", f"Level: {level}", f"Lives: {lives}"]
    for i, stat in enumerate(stats):
        Win.blit(Font.render(stat, 1, (255, 255, 255)), (10, 10 + i * 30))

    # Draw the player (use image if available, otherwise draw a rectangle)
    if player_image:
        Win.blit(player_image, (player_rect.x, player_rect.y))
    else:
        pygame.draw.rect(Win, PLAYER_COLOR, player_rect)

    # Draw the shield if visible
    if shield_visible:
        pygame.draw.rect(Win, PLAYER_SHIELD, shield_rect)

    # Draw stars
    for star in stars:
        pygame.draw.rect(Win, STAR_COLOR, star)

    # Draw power-ups
    for power_up in power_ups:
        pygame.draw.rect(Win, (0, 255, 0), power_up)  # Green for power-ups

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(Win, (255, 0, 0), enemy.rect)  # Red for enemies
        for bullet in enemy.bullets:
            pygame.draw.rect(Win, (255, 255, 0), bullet)  # Yellow for enemy bullets

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(Win, BULLET_COLOR, bullet)  # Yellow for bullets

    # Draw the boss and its stars if active
    if boss_rect:
        pygame.draw.rect(Win, (255, 0, 255), boss_rect)  # Purple for the boss
        if boss_health is not None:
            health_text = Font.render(f"Boss Health: {boss_health}", 1, (255, 255, 255))
            Win.blit(health_text, (WIDTH / 2 - health_text.get_width() / 2, 10))  # Display boss health at the top center
    if boss_stars:
        for boss_star in boss_stars:
            pygame.draw.rect(Win, STAR_COLOR, boss_star)

    # Display double damage indicator
    if double_damage_active:
        double_damage_text = Font.render("DOUBLE DAMAGE ACTIVE!", 1, (255, 255, 0))
        Win.blit(double_damage_text, (WIDTH / 2 - double_damage_text.get_width() / 2, HEIGHT - 50))

    pygame.display.update()

# Main Game Loop
def run_game():
    """Run the main game loop."""
    global high_score, score, level, lives, difficulty, double_damage_active, double_damage_timer, background_y
    score, level = 0, 1  # Reset score & level

    # Set starting lives and adjust difficulty settings
    if difficulty == "Easy":
        lives = 3
        star_vel = BASE_STAR_VEL - 2
        star_add_interval = BASE_STAR_ADD_INTERVAL + 500
        enemy_spawn_chance = 0.2  # 20% chance to spawn an enemy
        max_enemies = 2  # Maximum 1–2 enemies
    elif difficulty == "Medium":
        lives = 2
        star_vel = BASE_STAR_VEL
        star_add_interval = BASE_STAR_ADD_INTERVAL
        enemy_spawn_chance = 0.4  # 40% chance to spawn an enemy
        max_enemies = 3  # Maximum 3 enemies
    elif difficulty == "Hard":
        lives = 1
        star_vel = BASE_STAR_VEL + 2
        star_add_interval = BASE_STAR_ADD_INTERVAL - 500
        enemy_spawn_chance = 0.6  # 60% chance to spawn an enemy
        max_enemies = 4  # Maximum 4 enemies

    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    shield_rect = pygame.Rect(shield_x, shield_y, SHIELD_WIDTH, SHIELD_HEIGHT)
    clock, start_time, star_timer, stars, shield_visible = pygame.time.Clock(), time.time(), 0, [], True
    power_ups = []  # List of power-ups
    enemies = []  # List of enemies
    bullets = []  # List of bullets
    boss_active = False  # Flag to track if the boss is active
    boss_rect = None  # Boss rectangle
    boss_health = 0  # Boss health
    boss_stars = []  # Stars shot by the boss

    while lives > 0:
        elapsed_time = time.time() - start_time
        star_timer += clock.tick(60)

        # Update background position
        background_y += background_scroll_speed
        if background_y >= HEIGHT:  # Reset background when it moves off the screen
            background_y = 0

        # Handle double-damage power-up timer
        if double_damage_active:
            double_damage_timer -= 1
            if double_damage_timer <= 0:
                double_damage_active = False  # Deactivate double damage

        # Leveling up every 100 points
        level = max(1, score // 100 + 1)
        star_vel = BASE_STAR_VEL + (level - 1) * 1  # Increase star speed per level
        star_add_interval = max(500, BASE_STAR_ADD_INTERVAL - (level - 1) * 200)  # Reduce spawn interval

        # Spawn stars
        if star_timer > star_add_interval:
            num_stars = min(5 + level, 15)
            stars.extend([pygame.Rect(random.randint(0, WIDTH - STAR_WIDTH), -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT) for _ in range(num_stars)])
            star_timer = 0

        # Update stars
        for star in stars[:]:
            star.y += star_vel  # Increase falling speed with level
            if star.y > HEIGHT:
                stars.remove(star)
                score += 1
            elif star.colliderect(player_rect):
                stars.remove(star)
                lives -= 1
                if 'collision_sound' in locals():
                    collision_sound.play()
                break
            elif shield_visible and star.colliderect(shield_rect):
                stars.remove(star)
                break

        # Spawn enemies
        if len(enemies) < max_enemies and random.random() < enemy_spawn_chance:  # Check spawn chance and max enemies
            enemy_type = random.choice(["fast", "shooter"])
            if enemy_type == "fast":
                enemies.append(Enemy(random.randint(0, WIDTH - 30), -30, 30, 30, speed=6))  # Fast enemy
            elif enemy_type == "shooter":
                enemies.append(Enemy(random.randint(0, WIDTH - 30), -30, 30, 30, speed=3, shoots=True))  # Shooting enemy

        # Update enemies
        for enemy in enemies[:]:
            enemy.move()
            enemy.shoot()
            enemy.update_bullets()

            # Check if enemy collides with the player
            if enemy.rect.colliderect(player_rect):
                enemies.remove(enemy)
                lives -= 1
                if 'collision_sound' in locals():
                    collision_sound.play()

            # Remove enemy if it goes off-screen
            elif enemy.rect.y > HEIGHT:
                enemies.remove(enemy)

            # Check if enemy bullets hit the player
            for bullet in enemy.bullets[:]:
                if bullet.colliderect(player_rect):
                    enemy.bullets.remove(bullet)
                    lives -= 1
                    if 'collision_sound' in locals():
                        collision_sound.play()

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:  # Move left
            player_rect.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:  # Move right
            player_rect.x += PLAYER_VEL
        if keys[pygame.K_UP] and player_rect.top > 0:  # Move up
            player_rect.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:  # Move down
            player_rect.y += PLAYER_VEL

        # Update shield position
        shield_rect.x = player_rect.x + (PLAYER_WIDTH - SHIELD_WIDTH) // 2
        shield_rect.y = player_rect.y - SHIELD_HEIGHT - 10

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Shoot bullets
                    bullet = pygame.Rect(player_rect.centerx - BULLET_WIDTH // 2, player_rect.top, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets.append(bullet)
                    if 'shoot_sound' in locals():
                        shoot_sound.play()
                if event.key == pygame.K_1:  # Toggle shield visibility
                    shield_visible = not shield_visible

        # Update bullets
        for bullet in bullets[:]:
            bullet.y -= BULLET_VEL
            if bullet.y < 0:
                bullets.remove(bullet)
                continue

            # Check for collision with enemies
            for enemy in enemies[:]:
                if bullet.colliderect(enemy.rect):  # If bullet hits an enemy
                    enemies.remove(enemy)  # Remove the enemy
                    bullets.remove(bullet)  # Remove the bullet
                    score += 20  # Increase the score
                    break  # Exit the loop to avoid modifying the list during iteration

        # Draw everything
        draw(player_rect, elapsed_time, stars, shield_rect, shield_visible, score, level, lives, power_ups, enemies, bullets, boss_rect, boss_stars, boss_health)

        # If player runs out of lives, show game over screen
        if lives <= 0:
            game_over_screen()
            return  # Exit run_game() to restart from main()

# Main Function
def main():
    """Main function to run the game."""
    while True:
        draw_start_screen()
        run_game()
        game_over_screen()

# Run the Game
if __name__ == "__main__":
    main()

    
    