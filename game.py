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

# === Main Game Loop ===
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # === Drawing ===
    screen.blit(background_image, (0, 0))

    # (Draw other game elements here...)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# === Clean Up ===
pygame.quit()
sys.exit()