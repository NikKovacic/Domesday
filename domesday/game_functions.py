import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


class GameFunctions():
    """Class that contain important game functions"""

    def get_number_rows(self, settings, spaceship_height, alien_height):
        """Determine the number of rows of aliens that fit on the screen."""
        available_space_y = (settings.screen_height - (3 * alien_height) - spaceship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows

    def get_number_aliens_x(self, settings, alien_width):
        """Determine the number of aliens that fit in a row."""
        available_space_x = settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def create_alien(self, settings, screen, aliens, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(settings, screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)

    def create_fleet(self, settings, screen, spaceship, aliens):
        """Create a full fleet of aliens."""
        # Create an alien and find a number of aliens in a row.
        alien = Alien(settings, screen)
        number_aliens_x = GameFunctions.get_number_aliens_x(self, settings, alien.rect.width)
        number_rows = GameFunctions.get_number_rows(self, settings, spaceship.rect.height, alien.rect.height)

        # Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                GameFunctions.create_alien(self, settings, screen, aliens, alien_number, row_number)

    def check_keydown_events(self, event, settings, screen, stats, spaceship, bullets):
        """Responds to keypress."""
        if event.key == pygame.K_RIGHT:
            spaceship.moving_right = True
        elif event.key == pygame.K_LEFT:
            spaceship.moving_left = True
        elif event.key == pygame.K_SPACE:
            GameFunctions.fire_bullet(self, settings, screen, spaceship, bullets)
        elif event.key == pygame.K_q:
            GameFunctions.write_high_score(self, stats)
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            GameFunctions.write_high_score(self, stats)
            sys.exit()

    def fire_bullet(self, settings, screen, spaceship, bullets):
        """Fire a bullet if limit not reached yet."""
        # Create a new bullet and add it to the bullets group.
        if len(bullets) < settings.bullets_allowed:
            new_bullet = Bullet(settings, screen, spaceship)
            bullets.add(new_bullet)

    def check_keyup_events(self, event, spaceship):
        """Responds to key releases."""
        if event.key == pygame.K_RIGHT:
            spaceship.moving_right = False
        elif event.key == pygame.K_LEFT:
            spaceship.moving_left = False

    def check_events(self, settings, screen, stats, sb, play_button, spaceship, aliens, bullets):
        """Responds to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameFunctions.write_high_score(self, stats)
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                GameFunctions.check_keydown_events(self, event, settings, screen, stats, spaceship, bullets)

            elif event.type == pygame.KEYUP:
                GameFunctions.check_keyup_events(self, event, spaceship)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                GameFunctions.check_play_button(self, settings, screen, stats, sb, play_button, spaceship, aliens, bullets, mouse_x, mouse_y)

    def check_play_button(self, settings, screen, stats, sb, play_button, spaceship, aliens, bullets, mouse_x, mouse_y):
        """Start a new game when the player clicks Play."""
        # Start only if the game_active = False
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            # Reset the game settings.
            settings.initialize_dynamic_settings()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

            # Reset the game statistics.
            stats.reset_stats()
            stats.game_active = True

            # Reset the scoreboard images.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_spaceships()

            # Empty the list of aliens and bullets.
            aliens.empty()
            bullets.empty()

            # Create a new fleet and center spaceship.
            GameFunctions.create_fleet(self, settings, screen, spaceship, aliens)
            spaceship.center_spaceship()

    def update_screen(self, settings, screen, stats, sb, spaceship, aliens, bullets, play_button):
        """Update images on the screen and flip to the new screen."""
        # Redraw the screen during each pass through the loop.
        screen.fill(settings.bg_color)
        # Redraw all bullets behind spaceship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        spaceship.draw_me()
        aliens.draw(screen)

        # Draw the score information.
        sb.show_score()

        # Draw the play button if the game is inactive.
        if not stats.game_active:
            play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def update_bullets(self, settings, screen, stats, sb, spaceship, aliens, bullets):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        bullets.update()

        # Get rid of bullets that have disappered.
        """to-do: for bullet in bullets.copy(): -> old version"""
        for bullet in bullets:
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        # Check for any bullets that hit aliens.
        GameFunctions.check_bullet_alien_collisions(self, settings, screen, stats, sb, spaceship, aliens, bullets)

    def check_bullet_alien_collisions(self, settings, screen, stats, sb, spaceship, aliens, bullets):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
        if collisions:
            # Make sure to award points for each hit with for and len(aliens)
            # the bullet that collides with alien become a key in dict!
            for aliens in collisions.values():
                stats.score += settings.alien_points * len(aliens)
                sb.prep_score()
            GameFunctions.check_high_score(self, stats, sb)

        if len(aliens) == 0:
            # Destroy existing bullets, speed up the game, and create new fleet.
            bullets.empty()
            settings.increase_speed()
            # Increase level
            stats.level += 1
            sb.prep_level()

            GameFunctions.create_fleet(self, settings, screen, spaceship, aliens)

    def check_fleet_edges(self, settings, aliens):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in aliens.sprites():
            if alien.check_edges():
                GameFunctions.change_fleet_direction(self, settings, aliens)
                break

    def change_fleet_direction(self, settings, aliens):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in aliens.sprites():
            alien.rect.y += settings.fleet_drop_speed
        settings.fleet_direction *= -1

    def spaceship_hit(self, settings, screen, stats, sb, spaceship, aliens, bullets):
        """Respond to ship being hit by alien."""
        if stats.spaceships_left > 1:
            # Decrement spaceships_left.
            stats.spaceships_left -= 1

            # Update scoreboard.
            sb.prep_spaceships()

            # Empty the list of aliens and bullets.
            aliens.empty()
            bullets.empty()

            # Create a new fleet and center the spaceship.
            GameFunctions.create_fleet(self, settings, screen, spaceship, aliens)
            spaceship.center_spaceship()

            # Pause.
            sleep(0.5)
        else:
            stats.spaceships_left -= 1
            sb.prep_spaceships()
            stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_aliens_bottom(self, settings, screen, stats, sb, spaceship, aliens, bullets):
        """Check if any aliens have reachedthe bottom of the screen."""
        screen_rect = screen.get_rect()
        for alien in aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the spaceship got hit.
                GameFunctions.spaceship_hit(self, settings, screen, stats, sb, spaceship, aliens, bullets)

    def update_aliens(self, settings, screen, stats, sb, spaceship, aliens, bullets):
        """Check if the fleet is at an edge, and then update the position of all aliens in the fleet."""
        GameFunctions.check_fleet_edges(self, settings, aliens)
        aliens.update()

        # Look for alien-spaceship collisions.
        if pygame.sprite.spritecollideany(spaceship, aliens):
            GameFunctions.spaceship_hit(self, settings, screen, stats, sb, spaceship, aliens, bullets)

        # Kook for aliens hitting the bottom of the screen.
        GameFunctions.check_aliens_bottom(self, settings, screen, stats, sb, spaceship, aliens, bullets)

    def check_high_score(self, stats, sb):
        """Check to see if there's new high score."""
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            sb.prep_high_score()

    def write_high_score(self, stats):
        """Write high score to a file score.txt"""
        with open('score.txt', 'w') as hi_score:
            hi_score.write(str(stats.high_score))
