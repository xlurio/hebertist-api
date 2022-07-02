import unittest
from games_price_digger.src.iterators import SimpleIterator


class SimpleIteratorTests(unittest.TestCase):
    test_list = [0, 1, 2]

    def setUp(self) -> None:
        self.simple_iterator = SimpleIterator(self.test_list)

    def test_next_method(self):
        """Test next() method"""
        self.simple_iterator.next()
        current_index = self.simple_iterator.get_index()
        self.assertEqual(current_index, 1)

    def test_first_method(self):
        """Test first() method"""
        self.simple_iterator.next()
        self.simple_iterator.first()
        current_index = self.simple_iterator.get_index()
        self.assertEqual(current_index, 0)

    def test_is_not_done(self):
        """Test is_done() when the index is in bounds"""
        self.assertFalse(self.simple_iterator.is_done())

    def test_is_done(self):
        """Test is_done() when the index is out of bounds"""
        for _ in range(3):
            self.simple_iterator.next()
        self.assertTrue(self.simple_iterator.is_done())


if __name__ == '__main__':
    unittest.main()
