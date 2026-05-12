"""Game model definition."""
from dataclasses import dataclass


@dataclass
class Game:
    """Represents a video game in the store catalog."""
    game_id: int
    title: str
