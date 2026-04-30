"""User repository implementation."""
from src.models.user import User


class UserRepository:
    """Handles data operations for the User entity."""

    def __init__(self):
        """Initializes an empty user repository."""
        self.users = []

    def save(self, user: User) -> User:
        """Saves a new user to the repository."""
        self.users.append(user)
        return user

    def find_by_id(self, user_id: int) -> User | None:
        """Finds a user by their unique ID."""
        return next((u for u in self.users if u.user_id == user_id), None)

    def find_by_email(self, email: str) -> User | None:
        """Finds a user by their email address."""
        return next((u for u in self.users if u.email == email), None)
