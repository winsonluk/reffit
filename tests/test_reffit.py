'''Tests for reffit.py'''
import unittest

# Import the package
import reffit

# Import the get_asin function from reffit module
from reffit.reffit import get_asin


class TestASIN(unittest.TestCase):
    '''Test get_asin

    Test Class for get_asin function in reffit.py.
    '''

    def setUp(self):
        self.asin = '0123456789'

    def test_none(self):
        '''Test ASIN retrieval with a nonexistent ASIN.

        Tests that an ASIN retrieval for a nonexistent ASIN
        raises ValueError.
        '''
        comment = 'stub'
        self.assertRaises(ValueError, get_asin, comment)

    def test_out_of_range(self):
        '''Test ASIN retrieval with an incomplete ASIN.

        Tests that an ASIN retrieval for an existent ASIN that exists
        out of range of the comment raises ValueError.
        '''
        comment = 'foo/dp/bar'
        self.assertRaises(ValueError, get_asin, comment)

    def test_with_gp(self):
        '''Test ASIN retrieval in the form /gp/product/ASIN.

        Tests that a comment with /gp/product/ASIN returns ASIN.
        '''
        comment = 'foo/gp/product/0123456789bar'
        self.assertEqual(get_asin(comment), self.asin)

    def test_with_dp(self):
        '''Test ASIN retrieval in the form /dp/ASIN.

        Tests that a comment with /dp/ASIN returns ASIN.
        '''
        comment = 'foo/dp/0123456789bar'
        self.assertEqual(get_asin(comment), self.asin)

    def test_with_dp_and_gp(self):
        '''Test ASIN retrieval with both /gp/product/ASIN and /dp/ASIN.

        Tests that a comment with both /gp/product/ASIN and /dp/ASIN
        returns one ASIN only.
        '''
        comment = 'foo/dp/0123456789/gp/product/bar'
        self.assertEqual(get_asin(comment), self.asin)

if __name__ == '__main__':
    unittest.main()
