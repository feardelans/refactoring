"""
Module for managing an e-commerce store system.
Includes classes for handling users, products, and customer orders.
"""

class Product:
    """Represents a physical or digital product in the store."""
    def __init__(self, product_id: int, name: str, price: float):
        self.__product_id = product_id
        self.name = name
        self.price = price

    def __repr__(self):
        """Returns a string representation of the product."""
        return f"Product(ID: {self.__product_id}, Name: {self.name})"


class User:
    """Represents a registered user in the system."""
    def __init__(self, user_id: int, username: str, email: str):
        self.__user_id = user_id
        self.username = username
        self.email = email
        self.orders = []

    def register(self):
        """Handles user registration process."""
        return f"User {self.username} (ID: {self.__user_id}) registered successfully."

    def view_orders(self):
        """Returns the list of orders placed by the user."""
        return self.orders


class Order:
    """Manages a customer order and its associated products."""
    def __init__(self, order_id: int, user: User):
        self.__order_id = order_id
        self.user = user
        self.__products = []
        self.__status = "Pending"

    def add_product(self, product: Product):
        """Adds a product item to the order list."""
        self.__products.append(product)

    def remove_product(self, product: Product):
        """Removes a specific product item from the order."""
        if product in self.__products:
            self.__products.remove(product)

    def calculate_total(self):
        """Calculates the total price of all products in the order."""
        return sum(p.price for p in self.__products)

    def get_products(self):
        """Returns the list of products and prints order status information."""
        print(f"Order {self.__order_id} current status: {self.__status}")
        return self.__products