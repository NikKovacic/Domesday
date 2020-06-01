
class GameStats():
    """Track stats for Domesday."""

    def __init__(self, settings):
        """Initialize statistics."""
        self.settings = settings
        self.reset_stats()
        # High score should never be reset.
        self.high_score = self.read_high_score_file()
        # Start Domesday in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.spaceships_left = self.settings.spaceship_limit
        self.score = 0
        self.level = 1

    def read_high_score_file(self):
        """Read high score from the file score.txt"""
        with open('score.txt') as file_obj:
            high_score = int(file_obj.read())
        return high_score


