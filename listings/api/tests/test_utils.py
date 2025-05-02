from django.test import TestCase
from api.utils import convert_price_to_cents, format_price_from_cents

class PriceUtilsTests(TestCase):
    def test_convert_price_to_cents(self):
        # Test basic dollar amounts
        self.assertEqual(convert_price_to_cents('$100'), 10000)
        self.assertEqual(convert_price_to_cents('$1,000'), 100000)
        self.assertEqual(convert_price_to_cents('$1,234.56'), 123456)
        
        # Test K suffix
        self.assertEqual(convert_price_to_cents('$100K'), 10000000)
        self.assertEqual(convert_price_to_cents('$1.5K'), 150000)
        self.assertEqual(convert_price_to_cents('$1,234K'), 123400000)
        
        # Test M suffix
        self.assertEqual(convert_price_to_cents('$1M'), 100000000)
        self.assertEqual(convert_price_to_cents('$1.5M'), 150000000)
        self.assertEqual(convert_price_to_cents('$1.23M'), 123000000)
        
        # Test edge cases
        self.assertIsNone(convert_price_to_cents(''))
        self.assertIsNone(convert_price_to_cents(None))
        self.assertIsNone(convert_price_to_cents('invalid'))
        self.assertIsNone(convert_price_to_cents('$invalid'))
        
        # Test whitespace handling
        self.assertEqual(convert_price_to_cents(' $100 '), 10000)
        self.assertEqual(convert_price_to_cents('$ 100K '), 10000000)
        self.assertEqual(convert_price_to_cents(' $ 1.5M '), 150000000)

    def test_format_price_from_cents(self):
        # Test basic dollar amounts
        self.assertEqual(format_price_from_cents(10000), '$100')
        self.assertEqual(format_price_from_cents(100000), '$1,000')
        self.assertEqual(format_price_from_cents(123456), '$1,235')
        
        # Test amounts under $10M (should use commas)
        self.assertEqual(format_price_from_cents(10000000), '$100,000')
        self.assertEqual(format_price_from_cents(150000), '$1,500')
        self.assertEqual(format_price_from_cents(123400000), '$1,234,000')
        self.assertEqual(format_price_from_cents(100000000), '$1,000,000')
        self.assertEqual(format_price_from_cents(150000000), '$1,500,000')
        self.assertEqual(format_price_from_cents(123000000), '$1,230,000')
        
        # Test edge cases
        self.assertIsNone(format_price_from_cents(None))
        self.assertIsNone(format_price_from_cents(0))
        
        # Test very large numbers (over $10M use M suffix)
        self.assertEqual(format_price_from_cents(1000000000), '$10.0M')
        self.assertEqual(format_price_from_cents(1234567890), '$12.3M') 