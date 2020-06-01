import pygame
from pygame.sprite import Sprite


class SpaceShip(Sprite):
    """A class that draw(blit) a spaceship to the screen and move its position"""

    def __init__(self, settings, screen):
        """Initialize the spaceship."""
        super(SpaceShip, self).__init__()

        self.screen = screen
        self.settings = settings

        # Load the spaceship image and get its rect.
        self.image = pygame.image.load('images/ship1.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new spaceship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the spaceship's center.
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the spaceship's position based on movement flag."""
        # Update the spaceship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.spaceship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.spaceship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def draw_me(self):
        """Draw(blit) the spaceship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_spaceship(self):
        """Center the spaceship on the screen."""
        self.center = self.screen_rect.centerx
