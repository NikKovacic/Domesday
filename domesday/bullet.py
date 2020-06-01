import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the spaceship."""

    def __init__(self, settings, screen, spaceship):
        """Create a bullet object at the spaceship's current position."""
        # super().__init__() -> works with python3
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = spaceship.rect.centerx
        self.rect.top = spaceship.rect.top

        # Store the bullet's position as decimal value.
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
