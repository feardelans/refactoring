import unittest

from src.models import Dish, Menu, Client
from src.orders import Order, RegularOrder, BulkOrder
from src.factory import OrderFactory
from src.observers import OrderObserver, KitchenNotifier
from src.database import OrderDatabase

class TestBasicInteractions(unittest.TestCase):

    def test_dish_creation(self):
        dish = Dish("Pizza", 150)
        self.assertEqual("Pizza", dish.name)
        self.assertEqual(150, dish.price)

    def test_client_creation(self):
        client = Client("Vlad")
        self.assertEqual("Vlad", client.name)

    def test_menu_creation(self):
        menu = Menu()
        self.assertIsNotNone(menu)

    def test_menu_add_dish(self):
        menu = Menu()
        dish = Dish("Pasta", 120)
        menu.add_dish(dish)
        self.assertTrue(menu.contains_dish(dish))

    def test_order_creation(self):
        client = Client("Vlad")
        order = RegularOrder(client)
        self.assertIsNotNone(order)

    def test_order_client_association(self):
        client = Client("Vlad")
        order = RegularOrder(client)
        self.assertEqual(client, order.client)

    def test_kitchen_notifier_creation(self):
        notifier = KitchenNotifier()
        self.assertFalse(notifier.notified)

    def test_order_add_dish(self):
        order = RegularOrder(Client("Vlad"))
        order.add_dish(Dish("Salad", 80))
        self.assertEqual(1, len(order.dishes))

    def test_dish_equality(self):
        d1 = Dish("Soup", 50)
        d2 = Dish("Soup", 50)
        self.assertEqual(d1, d2)

    def test_menu_does_not_contain_unknown_dish(self):
        menu = Menu()
        self.assertFalse(menu.contains_dish(Dish("Steak", 300)))