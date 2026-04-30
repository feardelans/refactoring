"""User service implementation for business logic."""
from src.models.user import User
from src.repositories.user_repository import UserRepository

# pylint: disable=too-few-public-methods

class UserService:
    """Contains business logic related to user management."""

    def __init__(self, user_repo: UserRepository):
        """Initializes the user service with a user repository."""
        self.user_repo = user_repo

    def register_user(self, user_id: int, email: str, age: int) -> User:
        """Registers a new user, validating age and email uniqueness."""
        if age < 13:
            raise ValueError("Registration is allowed only from 13 years old.")
        if self.user_repo.find_by_email(email):
            raise ValueError("User with this email already exists.")

        new_user = User(user_id, email, age)
        return self.user_repo.save(new_user)
