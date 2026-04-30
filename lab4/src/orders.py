from abc import ABC, abstractmethod
from src.models import Client, Dish

class Order(ABC):
    """Abstract base class for all types of orders."""
    def __init__(self, client: Client):
        """Initializes order. Raises ValueError if client is None."""
        if client is None:
            raise ValueError("Order must have a valid client")
        self.client = client
        self.dishes = []

    def add_dish(self, dish: Dish):
        """Adds a selected dish to the order."""
        self.dishes.append(dish)

    @abstractmethod
    def get_type(self) -> str:
        """Returns the type of the order."""

class RegularOrder(Order):
    """Represents a standard order."""
    def get_type(self) -> str:
        """Returns the string 'Regular'."""
        return "Regular"

class BulkOrder(Order):
    """Represents a large-scale (bulk) order."""
    def get_type(self) -> str:
        """Returns the string 'Bulk'."""
        return "Bulk"