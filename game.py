import pygame
import sys

WIDTH = 800
HEIGHT = 550


# === Setup ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drop the Pokeball")

# === Load PNG Background ===
background_image = pygame.image.load("./assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pokeball = pygame.image.load("./assets/pokeball.png").convert_alpha()
pokeball = pygame.transform.scale(pokeball, (64, 64))  # Resize if needed

# === Initial Position & Speed ===
pokeball_x = 0
pokeball_y = 10  # Top of the screen
speed = 4
direction = 1  # 1 = right, -1 = left


# Load and scale ditch image
ditch_image = pygame.image.load("./assets/ditch.png").convert_alpha()
ditch_width, ditch_height = 100, 80  # Adjust based on image or target size
ditch_image = pygame.transform.scale(ditch_image, (ditch_width, ditch_height))

# Compute spacing
ditch_gap = 20
ditch_count = 5
total_width = (ditch_count * ditch_width) + ((ditch_count - 1) * ditch_gap)
ditch_start_x = (WIDTH - total_width) // 2
ditch_y_pos = HEIGHT - ditch_height


clock = pygame.time.Clock()
running = True

# === Main Loop ===
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background first
    screen.blit(background_image, (0, 0))

    # Draw the ditches
    for i in range(ditch_count):
        ditch_x = ditch_start_x + i * (ditch_width + ditch_gap)
        screen.blit(ditch_image, (ditch_x, ditch_y_pos))

    # Update Pokéball position and draw it
    pokeball_x += speed * direction
    if pokeball_x + pokeball.get_width() >= WIDTH or pokeball_x <= 0:
        direction *= -1
    screen.blit(pokeball, (pokeball_x, pokeball_y))

    pygame.display.flip()
    clock.tick(60)

# === Cleanup ===
pygame.quit()
sys.exit()
