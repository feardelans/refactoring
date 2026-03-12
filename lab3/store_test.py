import unittest
from lab_store import User, Product, Order

class TestInternetStore(unittest.TestCase):
    def setUp(self):
        self.user = User(1, "ivan_p", "ivan@email.com")
        self.p1 = Product(101, "Клавіатура", 1200.0)
        self.p2 = Product(102, "Монітор", 8500.0)
        self.order = Order(500, self.user)

    def test_user_registration_string(self):
        self.assertIn("ivan_p", self.user.register())

    def test_add_product(self):
        self.order.add_product(self.p1)
        self.assertEqual(len(self.order.get_products()), 1)

    def test_total_calculation(self):
        self.order.add_product(self.p1)
        self.order.add_product(self.p2)
        self.assertEqual(self.order.calculate_total(), 9700.0)

    def test_remove_product(self):
        self.order.add_product(self.p1)
        self.order.remove_product(self.p1)
        self.assertNotIn(self.p1, self.order.get_products())

    def test_empty_order_total(self):
        self.assertEqual(self.order.calculate_total(), 0)

    def test_order_belongs_to_correct_user(self):
        self.assertEqual(self.order.user.username, "ivan_p")

    def test_product_price_type(self):
        self.assertIsInstance(self.p1.price, float)

    def test_duplicate_products(self):
        self.order.add_product(self.p1)
        self.order.add_product(self.p1)
        self.assertEqual(self.order.calculate_total(), 2400.0)

    def test_user_view_orders_is_list(self):
        self.assertIsInstance(self.user.view_orders(), list)


    def test_remove_non_existent_product(self):
        self.order.add_product(self.p1)
        self.order.remove_product(self.p2)
        self.assertEqual(len(self.order.get_products()), 1)

if __name__ == '__main__':
    unittest.main()