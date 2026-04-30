

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