"""Store service implementation for business logic."""
from src.models.review import Review
from src.repositories.game_repository import GameRepository
from src.repositories.user_repository import UserRepository

# pylint: disable=too-few-public-methods

class StoreService:
    """Contains business logic for store operations."""

    def __init__(self, game_repo: GameRepository, user_repo: UserRepository):
        """Initializes the store service with required repositories."""
        self.game_repo = game_repo
        self.user_repo = user_repo
        self.reviews = []

    def add_to_library(self, user_id: int, game_id: int) -> bool:
        """Adds a game to the user's library and removes it from the wishlist if present."""
        user = self.user_repo.find_by_id(user_id)
        game = self.game_repo.find_by_id(game_id)

        if not user or not game:
            raise ValueError("User or game not found.")
        if game_id in user.library:
            raise ValueError("The game is already in your library.")

        user.library.append(game_id)

        if game_id in user.wishlist:
            user.wishlist.remove(game_id)
        return True

    def refund_game(self, user_id: int, game_id: int) -> bool:
        """Removes a game from the user's library."""
        user = self.user_repo.find_by_id(user_id)
        if not user or game_id not in user.library:
            raise ValueError("This game is not in your library.")

        user.library.remove(game_id)
        return True

    def add_to_wishlist(self, user_id: int, game_id: int) -> bool:
        """Adds a game to the user's wishlist."""
        user = self.user_repo.find_by_id(user_id)
        game = self.game_repo.find_by_id(game_id)

        if not user or not game:
            raise ValueError("User or game not found.")
        if game_id in user.library:
            raise ValueError("The game is already in your library.")
        if game_id in user.wishlist:
            raise ValueError("The game is already in your wishlist.")

        user.wishlist.append(game_id)
        return True

    def leave_review(self, user_id: int, game_id: int, rating: int, text: str) -> Review:
        """Allows a user to leave a review for a purchased game."""
        user = self.user_repo.find_by_id(user_id)

        if not user or game_id not in user.library:
            raise ValueError("Reviews can only be left for purchased games.")
        if not 1 <= rating <= 10:
            raise ValueError("Rating must be between 1 and 10.")

        review = Review(user_id, game_id, rating, text)
        self.reviews.append(review)
        return review

    def search_games(self, query: str):
        """Searches for games by title, returning all games if the query is empty."""
        if not query.strip():
            return self.game_repo.games
        return self.game_repo.search_by_title(query)
