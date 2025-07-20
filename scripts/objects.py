import pygame

GAME_WIDTH = 800
GAME_HEIGHT = 550


class Pokeball:
    def __init__(self, image):
        """
        Sets up a Pokeball with its image, position, size, speed, and drop status
        """
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
        """
        Moves side to side until dropped, then falls down and stops at the bottom
        """
        if not self.dropping:
            self.x += self.h_speed * self.direction
            if self.x <= 0 or self.x + self.w >= GAME_WIDTH:
                self.direction *= -1
        else:
            self.y += self.v_speed
            if self.y + self.h >= GAME_HEIGHT:
                self.y = GAME_HEIGHT - self.h
                self.dropped = True

    def draw(self, surface):
        """
        Move ball to current position
        """
        surface.blit(self.image, (self.x, self.y))

    def drop(self):
        """
        Drop the pokeball when called
        """
        self.dropping = True

    def get_rect(self):
        """
        Return the rectangle
        """
        return pygame.Rect(self.x, self.y, self.w, self.h)


class Ditch:
    def __init__(self, x, y, image):
        """
        Creates a Ditch at (x, y) with an image and defines a smaller perfect landing area inside it.
        """
        self.x = x
        self.y = y
        self.image = image
        self.ditch_width = 100
        self.ditch_height = 80
        self.rect = pygame.Rect(x, y, self.ditch_width, self.ditch_height)

        margin = self.ditch_width * 0.20
        zone_width = self.ditch_width * 0.60
        self.perfect_zone = pygame.Rect(x + margin, y, zone_width, self.ditch_height)

    def draw(self, surface):
        """
        Draw the ditch
        """
        surface.blit(self.image, (self.x, self.y))

    def is_perfect_landing(self, pokeball_rect):
        """
        Checks if the pokeball’s rectangle is fully inside the perfect landing zone
        """
        return self.perfect_zone.contains(pokeball_rect)
