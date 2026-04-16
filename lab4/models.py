"""
This module contains the core classes for the order management system.
It includes models for Dish, Menu, Client, Orders, KitchenNotifier,
and design patterns: Factory and Singleton.
"""

# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod


class Dish:
    """Represents a single dish item in the menu."""

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Dish):
            return False
        return self.name == other.name and self.price == other.price


class Menu:
    """Manages the collection of available dishes."""

    def __init__(self):
        self.dishes = []

    def add_dish(self, dish: Dish):
        """Adds a new dish to the menu. Raises ValueError if dish is None."""
        if dish is None:
            raise ValueError("Dish cannot be None")
        self.dishes.append(dish)

    def contains_dish(self, dish: Dish) -> bool:
        """Checks if a specific dish exists in the menu."""
        return dish in self.dishes

    def is_empty(self) -> bool:
        """Returns True if the menu has no dishes."""
        return len(self.dishes) == 0


class Client:
    """Represents a customer placing an order."""

    def __init__(self, name: str):
        self.name = name


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


class OrderFactory:
    """Factory pattern for creating different types of orders."""

    @staticmethod
    def create_order(order_type: str, client: Client) -> Order:
        """Creates an order based on the specified type."""
        if order_type == "Bulk":
            return BulkOrder(client)
        return RegularOrder(client)


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


class OrderDatabase:
    """Singleton pattern managing the shared database of orders."""
    _instance = None

    def __new__(cls):
        """Ensures only one instance of the database exists."""
        if cls._instance is None:
            cls._instance = super(OrderDatabase, cls).__new__(cls)
            cls._instance.orders = []
            cls._instance.observers = []
        return cls._instance

    def add_observer(self, observer: OrderObserver):
        """Registers a new observer to the database."""
        self.observers.append(observer)

    def save_order(self, order: Order):
        """Saves an order to the database and notifies all observers."""
        self.orders.append(order)
        self.notify_observers(order)

    def notify_observers(self, order: Order):
        """Notifies all registered observers about a new order."""
        for obs in self.observers:
            obs.update(order)

    def clear(self):
        """Clears the database state (useful for test isolation)."""
        self.orders.clear()
        self.observers.clear()