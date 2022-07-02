import unittest
from games_price_digger.src.utils import TestHTMLGetter


class TestHTMLGetterTests(unittest.TestCase):

    def test_get_html_file_by_name(self):
        """Test getting html by file name"""
        getter = TestHTMLGetter()
        result = getter.get_html_file_by_name('generic.html')
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
