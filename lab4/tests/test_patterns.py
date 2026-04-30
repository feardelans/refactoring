"""
Tests for Design Patterns: Singleton, Factory, and Observer
"""
import unittest

from src.models import Dish, Menu, Client
from src.orders import Order, RegularOrder, BulkOrder
from src.factory import OrderFactory
from src.observers import OrderObserver, KitchenNotifier
from src.database import OrderDatabase

class TestDesignPatterns(unittest.TestCase):

    def setUp(self):
        OrderDatabase().clear()

    def test_singleton_same_instance(self):
        db1 = OrderDatabase()
        db2 = OrderDatabase()
        self.assertIs(db1, db2)

    def test_singleton_maintains_state(self):
        db1 = OrderDatabase()
        db1.save_order(RegularOrder(Client("Alice")))
        db2 = OrderDatabase()
        self.assertEqual(len(db2.orders), 1)

    def test_singleton_clear_state(self):
        db = OrderDatabase()
        db.save_order(RegularOrder(Client("Bob")))
        db.clear()
        self.assertEqual(len(db.orders), 0)

    def test_factory_creates_regular_order(self):
        order = OrderFactory.create_order("Regular", Client("Charlie"))
        self.assertIsInstance(order, RegularOrder)
        self.assertEqual(order.get_type(), "Regular")

    def test_factory_creates_bulk_order(self):
        order = OrderFactory.create_order("Bulk", Client("David"))
        self.assertIsInstance(order, BulkOrder)
        self.assertEqual(order.get_type(), "Bulk")

    def test_factory_default_to_regular(self):
        order = OrderFactory.create_order("Unknown", Client("Eve"))
        self.assertIsInstance(order, RegularOrder)

    def test_observer_notified_on_save(self):
        db = OrderDatabase()
        kitchen = KitchenNotifier()
        db.add_observer(kitchen)
        db.save_order(RegularOrder(Client("Frank")))
        self.assertTrue(kitchen.notified)

    def test_multiple_observers_notified(self):
        db = OrderDatabase()
        kitchen1 = KitchenNotifier()
        kitchen2 = KitchenNotifier()
        db.add_observer(kitchen1)
        db.add_observer(kitchen2)
        db.save_order(BulkOrder(Client("Grace")))
        self.assertTrue(kitchen1.notified and kitchen2.notified)

    def test_no_notification_without_save(self):
        db = OrderDatabase()
        kitchen = KitchenNotifier()
        db.add_observer(kitchen)
        self.assertFalse(kitchen.notified)

    def test_observer_reset_state(self):
        db = OrderDatabase()
        kitchen = KitchenNotifier()
        db.add_observer(kitchen)
        db.save_order(RegularOrder(Client("Henry")))
        kitchen.reset()
        self.assertFalse(kitchen.notified)


if __name__ == '__main__':
    unittest.main()