'''Tests for reffit.py'''
import unittest

# Import the package
import reffit

# Import the reffit module
from reffit.reffit import get_asin

class TestASIN(unittest.TestCase):
    def setUp(self):
        self.asin = '0123456789'
    def test_none(self):
        comment = 'stub'
        self.assertRaises(ValueError, get_asin, comment)
    def test_with_gp(self):
        comment = 'foo/gp/product/0123456789bar'
        self.assertEqual(get_asin(comment), self.asin)
    def test_with_dp(self):
        comment = 'foo/dp/0123456789bar'
        self.assertEqual(get_asin(comment), self.asin)
    def test_with_dp_and_gp(self):
        comment = 'foo/dp/0123456789/gp/product/bar'
        self.assertEqual(get_asin(comment), self.asin)
    def test_out_of_range(self):
        comment = 'foo/dp/bar'
        self.assertRaises(ValueError, get_asin, comment)

if __name__ == '__main__':
    unittest.main()
