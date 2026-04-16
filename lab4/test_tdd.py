"""
TDD Tests: Checking business logic and edge cases.
"""

import unittest
from models import Dish, Menu, Client, RegularOrder, KitchenNotifier

class TestTDDScenarios(unittest.TestCase):

    def test_add_dish_to_menu_success(self):
        menu = Menu()
        dish = Dish("Salad", 100)
        menu.add_dish(dish)
        self.assertTrue(menu.contains_dish(dish))

    def test_add_dish_to_menu_failure(self):
        menu = Menu()
        # Очікуємо помилку при додаванні None
        with self.assertRaises(ValueError):
            menu.add_dish(None)

    def test_create_order_success(self):
        order = RegularOrder(Client("Alice"))
        self.assertEqual(order.get_type(), "Regular")

    def test_create_order_missing_client(self):
        # Очікуємо помилку при створенні замовлення без клієнта
        with self.assertRaises(ValueError):
            RegularOrder(None)

    def test_order_client_association(self):
        client = Client("Bob")
        order = RegularOrder(client)
        self.assertEqual(order.client.name, "Bob")

    def test_menu_is_empty_handling(self):
        menu = Menu()
        self.assertTrue(menu.is_empty())
        menu.add_dish(Dish("Soup", 50))
        self.assertFalse(menu.is_empty())

    def test_add_dishes_to_order(self):
        order = RegularOrder(Client("John"))
        order.add_dish(Dish("Burger", 150))
        self.assertEqual(len(order.dishes), 1)

    def test_notify_kitchen_on_new_order(self):
        notifier = KitchenNotifier()
        order = RegularOrder(Client("Vlad"))
        order.add_dish(Dish("Pizza", 200))
        notifier.update(order)
        self.assertTrue(notifier.notified)

    def test_menu_does_not_contain_unadded_dish(self):
        menu = Menu()
        menu.add_dish(Dish("Tea", 30))
        self.assertFalse(menu.contains_dish(Dish("Coffee", 40)))

    def test_order_created_with_empty_dishes_list(self):
        order = RegularOrder(Client("Eve"))
        self.assertEqual(len(order.dishes), 0)

if __name__ == '__main__':
    unittest.main()