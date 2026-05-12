"""Review model definition."""
from dataclasses import dataclass


@dataclass
class Review:
    """Represents a user review for a specific game."""
    user_id: int
    game_id: int
    rating: int
    text: str
