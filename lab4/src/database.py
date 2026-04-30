from src.orders import Order
from src.observers import OrderObserver

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