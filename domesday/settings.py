# Settings for Domesday


class Settings():
    """A class to store all settings for Domesday game."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1100
        self.screen_height = 850
        self.bg_color = (255, 255, 255)  # ali 230x3(sivo)

        # spaceShip settings
        # self.spaceship_speed_factor = 1.5  delete?
        self.spaceship_limit = 3

        # Bullet settings
        # self.bullet_speed_factor = 3   delete?q
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Alien settings
        # self.alien_speed_factor = 1   delete?
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 left.
        # self.fleet_direction = 1   delete?

        # How quickly the game speeds up.
        self.speedup_scale = 1.2

        # How quickly the alien point value increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.spaceship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction of 1 represents right; -1 left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.spaceship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        # increase points each level
        self.alien_points = int(self.alien_points * self.score_scale)
        # self.alien_points *= self.score_scale -> weird numbers on scoreboard because doesnt round numbers
        # print(self.alien_points)
