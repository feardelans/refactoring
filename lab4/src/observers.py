from abc import ABC, abstractmethod
from src.orders import Order


class OrderObserver(ABC):
    """Interface for observers in the Observer Pattern."""

    @abstractmethod
    def update(self, order: Order):
        """Called to notify the observer of an event (e.g., a new order)."""


class KitchenNotifier(OrderObserver):
    """Responsible for notifying the kitchen about new orders."""

    def __init__(self):
        self.notified = False

    def update(self, order: Order):
        """Updates the notification status to True."""
        self.notified = True

    def reset(self):
        """Resets the notification status (useful for testing)."""
        self.notified = False