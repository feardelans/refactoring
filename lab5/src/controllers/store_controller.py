"""Store controller for handling incoming requests."""
from src.services.store_service import StoreService

# pylint: disable=too-few-public-methods


class StoreController:
    """Serves as the API entry point for store-related actions."""

    def __init__(self, store_service: StoreService):
        """Initializes the controller with the store service."""
        self.store_service = store_service

    def handle_add_to_library(self, user_id: int, game_id: int):
        """Handles request to add a game to a user's library."""
        try:
            self.store_service.add_to_library(user_id, game_id)
            print("Success: Game added to library.")
        except ValueError as e:
            print(f"Store Error: {e}")
