# import sys
import pygame
from settings import Settings
from spaceship import SpaceShip
from game_stats import GameStats
from play_button import PlayButton
from scoreboard import Scoreboard
from game_functions import GameFunctions
from pygame.sprite import Group


class Game():
    """Main class responsible for run the game"""

    def run_game():
        # Initialize game and create a screen object.
        pygame.init()
        settings = Settings()
        screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
        pygame.display.set_caption("Domesday")

        # Make the play button.
        play_button = PlayButton(screen, "PLAY")

        # Create an instance to store game statistics and create scoreboard.
        stats = GameStats(settings)
        sb = Scoreboard(settings, screen, stats)

        # Make a spaceship, a group of bullets and a group of aliens.
        spaceship = SpaceShip(settings, screen)
        bullets = Group()
        aliens = Group()

        # Create the fleet of aliens.
        gf = GameFunctions()
        gf.create_fleet(settings, screen, spaceship, aliens)

        # Start the main loop for the game.
        while True:
            gf.check_events(settings, screen, stats, sb, play_button, spaceship, aliens, bullets)

            if stats.game_active:
                spaceship.update()
                # bullets.update() -> to-do old version of updating bullets.
                # Get rid of bullets that have disappeared.
                gf.update_bullets(settings, screen, stats, sb, spaceship, aliens, bullets)
                gf.update_aliens(settings, screen, stats, sb, spaceship, aliens, bullets)

            gf.update_screen(settings, screen, stats, sb, spaceship, aliens, bullets, play_button)


# run_game()

Game.run_game()
