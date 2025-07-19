import pygame

WIDTH = 800
HEIGHT = 550

ditch_width, ditch_height = 100, 80

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


class Ditch:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(x, y, ditch_width, ditch_height)

        margin = ditch_width * 0.20
        zone_width = ditch_width * 0.60
        self.perfect_zone = pygame.Rect(x + margin, y, zone_width, ditch_height)

    def draw(self, surface, debug=False):
        surface.blit(self.image, (self.x, self.y))
        if debug:
            overlay = pygame.Surface((self.perfect_zone.width, self.perfect_zone.height), pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 100))
            surface.blit(overlay, (self.perfect_zone.x, self.perfect_zone.y))

    def is_perfect_landing(self, pokeball_rect):
        return self.perfect_zone.contains(pokeball_rect)
