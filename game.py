import pygame
import sys
import requests
from io import BytesIO
from main import read_dataset, pokemon_picker
from objects import Pokeball, Ditch

# === Constants ===
WIDTH = 800
HEIGHT = 550
FPS = 60

# === Pygame Setup ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drop the Pokeball")
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)
clock = pygame.time.Clock()

# === Load Images ===
background_image = pygame.image.load("./assets/background.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pokeball_img = pygame.image.load("./assets/pokeball.png").convert_alpha()
pokeball_img = pygame.transform.scale(pokeball_img, (45, 45))

ditch_img = pygame.image.load("./assets/ditch.png").convert_alpha()
ditch_width, ditch_height = 100, 80
ditch_img = pygame.transform.scale(ditch_img, (ditch_width, ditch_height))


# Create ditches
ditch_gap = 20
ditch_count = 5
total_width = (ditch_count * ditch_width) + ((ditch_count - 1) * ditch_gap)
ditch_start_x = (WIDTH - total_width) // 2
ditch_y_pos = HEIGHT - ditch_height

ditches = []
for i in range(ditch_count):
    ditch_x = ditch_start_x + i * (ditch_width + ditch_gap)
    ditches.append(Ditch(ditch_x, ditch_y_pos, ditch_img))


# Game state
pokeball = Pokeball(pokeball_img)
game_over = False
won = False
retry_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 150, 150, 50)
reward_pokemon = None
reward_image = None

df = read_dataset()


running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and retry_button.collidepoint(event.pos):
                pokeball = Pokeball(pokeball_img)
                game_over = False
                won = False
                reward_pokemon = None
                reward_image = None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pokeball = Pokeball(pokeball_img)
                game_over = False
                won = False
                reward_pokemon = None
                reward_image = None

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pokeball.drop()

    if not game_over:
        pokeball.update()

        if pokeball.dropped:
            for ditch in ditches:
                if ditch.is_perfect_landing(pokeball.get_rect()):
                    won = True
                    reward_pokemon = pokemon_picker(df)

                    if reward_pokemon and reward_pokemon[1]:
                        try:
                            response = requests.get(reward_pokemon[1])
                            image_data = BytesIO(response.content)
                            reward_image = pygame.image.load(image_data).convert_alpha()
                            reward_image = pygame.transform.scale(reward_image, (250, 250))
                        except Exception as e:
                            print("Error loading sprite:", e)
                            reward_image = None
                    else:
                        reward_image = None
                    break
            game_over = True

    for ditch in ditches:
        ditch.draw(screen)

    pokeball.draw(screen)

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if won:
            if reward_pokemon:
                name_text = small_font.render(f"You got {reward_pokemon[0]}!", True, (255, 255, 255))
                screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 + 100))

            if reward_image:
                screen.blit(reward_image, (WIDTH // 2 - reward_image.get_width() // 2, HEIGHT // 2 - 100))
        else:
            lose_text = font.render("You Lose!", True, (255, 0, 0))
            screen.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT // 2 - 60))

        pygame.draw.rect(screen, (50, 50, 200), retry_button, border_radius=10)
        retry_text = small_font.render("Retry", True, (255, 255, 255))
        screen.blit(retry_text, (retry_button.centerx - retry_text.get_width() // 2,
                                 retry_button.centery - retry_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
