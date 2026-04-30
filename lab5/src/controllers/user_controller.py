"""User controller for handling incoming requests."""
from src.services.user_service import UserService

# pylint: disable=too-few-public-methods

class UserController:
    """Serves as the API entry point for user-related actions."""

    def __init__(self, user_service: UserService):
        """Initializes the controller with the user service."""
        self.user_service = user_service

    def handle_registration(self, user_id: int, email: str, age: int):
        """Handles user registration request."""
        try:
            user = self.user_service.register_user(user_id, email, age)
            print(f"Success: User {user.email} has been registered.")
        except ValueError as e:
            print(f"Registration Error: {e}")
