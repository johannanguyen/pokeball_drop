import pygame
import sys

# === Constants ===
WIDTH = 800
HEIGHT = 550

# === Pygame Setup ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drop the Pokeball")
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)

# === Load PNGs ===
background_image = pygame.image.load("./assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pokeball = pygame.image.load("./assets/pokeball.png").convert_alpha()
pokeball = pygame.transform.scale(pokeball, (64, 64))

ditch_image = pygame.image.load("./assets/ditch.png").convert_alpha()
ditch_width, ditch_height = 100, 80
ditch_image = pygame.transform.scale(ditch_image, (ditch_width, ditch_height))

# === Ditch Layout ===
ditch_gap = 20
ditch_count = 5
total_width = (ditch_count * ditch_width) + ((ditch_count - 1) * ditch_gap)
ditch_start_x = (WIDTH - total_width) // 2
ditch_y_pos = HEIGHT - ditch_height

# === Game State Reset Function ===
def reset_game():
    return {
        "pokeball_x": 0,
        "pokeball_y": 10,
        "horizontal_speed": 4,
        "vertical_speed": 5,
        "direction": 1,
        "is_dropping": False,
        "game_over": False,
        "lost": False,
        "won": False
    }

state = reset_game()
clock = pygame.time.Clock()

# === Retry Button Rect ===
retry_button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50)

# === Main Game Loop ===
running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state["game_over"]:
            if event.type == pygame.MOUSEBUTTONDOWN and retry_button_rect.collidepoint(event.pos):
                state = reset_game()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state["is_dropping"] = True

    # Draw ditches and calculate perfect zones
    ditch_rects = []
    perfect_zones = []

    for i in range(ditch_count):
        ditch_x = ditch_start_x + i * (ditch_width + ditch_gap)
        ditch_rect = pygame.Rect(ditch_x, ditch_y_pos, ditch_width, ditch_height)
        ditch_rects.append(ditch_rect)

        # Middle 50% zone
        zone_margin = ditch_width * 0.25
        perfect_zone = pygame.Rect(
            ditch_x + zone_margin,
            ditch_y_pos,
            ditch_width * 0.50,
            ditch_height
        )
        perfect_zones.append(perfect_zone)

        screen.blit(ditch_image, (ditch_x, ditch_y_pos))

    # Update Pokeball position
    if not state["game_over"]:
        if not state["is_dropping"]:
            state["pokeball_x"] += state["horizontal_speed"] * state["direction"]
            if state["pokeball_x"] <= 0 or state["pokeball_x"] + pokeball.get_width() >= WIDTH:
                state["direction"] *= -1
        else:
            state["pokeball_y"] += state["vertical_speed"]
            if state["pokeball_y"] + pokeball.get_height() >= ditch_y_pos:
                # Check landing accuracy
                pokeball_center = state["pokeball_x"] + pokeball.get_width() // 2
                landed_perfectly = any(
                    zone.left <= pokeball_center <= zone.right for zone in perfect_zones
                )

                state["game_over"] = True
                state["won"] = landed_perfectly
                state["lost"] = not landed_perfectly

    # Draw Pokeball
    screen.blit(pokeball, (state["pokeball_x"], state["pokeball_y"]))

    # Game Over Screen
    if state["game_over"]:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if state["won"]:
            result_text = font.render("You Win!", True, (0, 255, 0))
        else:
            result_text = font.render("You Lose!", True, (255, 0, 0))

        retry_text = small_font.render("Retry", True, (255, 255, 255))

        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 60))
        pygame.draw.rect(screen, (50, 50, 200), retry_button_rect, border_radius=10)
        screen.blit(retry_text, (retry_button_rect.centerx - retry_text.get_width() // 2,
                                 retry_button_rect.centery - retry_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()