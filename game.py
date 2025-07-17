import pygame
import sys

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
background_image = pygame.image.load("./assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pokeball_img = pygame.image.load("./assets/pokeball.png").convert_alpha()
pokeball_img = pygame.transform.scale(pokeball_img, (45, 45))

ditch_img = pygame.image.load("./assets/ditch.png").convert_alpha()
ditch_width, ditch_height = 100, 80
ditch_img = pygame.transform.scale(ditch_img, (ditch_width, ditch_height))


# === Pokeball Class ===
class Pokeball:
    def __init__(self, image):
        self.image = image
        self.x = 0
        self.y = 10
        self.w = image.get_width()
        self.h = image.get_height()
        self.h_speed = 6
        self.v_speed = 7
        self.direction = 1
        self.dropping = False
        self.dropped = False

    def update(self):
        if not self.dropping:
            self.x += self.h_speed * self.direction
            if self.x <= 0 or self.x + self.w >= WIDTH:
                self.direction *= -1
        else:
            self.y += self.v_speed
            if self.y + self.h >= HEIGHT:
                self.y = HEIGHT - self.h
                self.dropped = True

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def drop(self):
        self.dropping = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


# === Ditch Class ===
class Ditch:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, ditch_width, ditch_height)

        margin = ditch_width * 0.25  # Middle 50%
        self.perfect_zone = pygame.Rect(
            x + margin, y, ditch_width * 0.5, ditch_height
        )

    def draw(self, surface, debug=False):
        surface.blit(self.image, (self.x, self.y))
        if debug:
            overlay = pygame.Surface((self.perfect_zone.width, self.perfect_zone.height), pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 100))  # Semi-transparent green
            surface.blit(overlay, (self.perfect_zone.x, self.perfect_zone.y))

    def is_perfect_landing(self, pokeball_rect):
        return self.perfect_zone.contains(pokeball_rect)


# === Create Ditches ===
ditch_gap = 20
ditch_count = 5
total_width = (ditch_count * ditch_width) + ((ditch_count - 1) * ditch_gap)
ditch_start_x = (WIDTH - total_width) // 2
ditch_y_pos = HEIGHT - ditch_height

ditches = []
for i in range(ditch_count):
    ditch_x = ditch_start_x + i * (ditch_width + ditch_gap)
    ditches.append(Ditch(ditch_x, ditch_y_pos, ditch_img))

# === Create Pokeball ===
pokeball = Pokeball(pokeball_img)

# === Game State ===
game_over = False
won = False
retry_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 40, 150, 50)

# === Main Game Loop ===
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
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pokeball.drop()

    # Update Pokeball
    if not game_over:
        pokeball.update()

        # Check win condition after drop
        if pokeball.dropped:
            for ditch in ditches:
                if ditch.is_perfect_landing(pokeball.get_rect()):
                    won = True
                    break
            game_over = True

    # Draw Ditches with debug zones
    for ditch in ditches:
        ditch.draw(screen, debug=True)

    # Draw Pokeball
    pokeball.draw(screen)

    # Game Over Screen
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        result_text = font.render("You Win!" if won else "You Lose!", True,
                                  (0, 255, 0) if won else (255, 0, 0))
        retry_text = small_font.render("Retry", True, (255, 255, 255))

        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 60))
        pygame.draw.rect(screen, (50, 50, 200), retry_button, border_radius=10)
        screen.blit(retry_text, (retry_button.centerx - retry_text.get_width() // 2,
                                 retry_button.centery - retry_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()