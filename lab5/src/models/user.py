"""User model definition."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    """Represents a user in the system."""
    user_id: int
    email: str
    age: int
    library: List[int] = field(default_factory=list)
    wishlist: List[int] = field(default_factory=list)
