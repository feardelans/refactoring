"""Game repository implementation."""
from src.models.game import Game


class GameRepository:
    """Handles data operations for the Game entity."""

    def __init__(self):
        """Initializes the repository with a default catalog of games."""
        self.games = [
            Game(1, "The Witcher 3"),
            Game(2, "Cyberpunk 2077"),
            Game(3, "Minecraft"),
            Game(4, "The Elder Scrolls V: Skyrim"),
            Game(5, "Portal 2")
        ]

    def find_by_id(self, game_id: int) -> Game | None:
        """Finds a game by its unique ID."""
        return next((g for g in self.games if g.game_id == game_id), None)

    def search_by_title(self, query: str):
        """Searches for games containing the query string in their title."""
        return [g for g in self.games if query.lower() in g.title.lower()]
