from src.models import Client
from src.orders import Order, RegularOrder, BulkOrder


class OrderFactory:
    """Factory pattern for creating different types of orders."""

    @staticmethod
    def create_order(order_type: str, client: Client) -> Order:
        """Creates an order based on the specified type."""
        if order_type == "Bulk":
            return BulkOrder(client)
        return RegularOrder(client)