import unittest

def palindrome(input_string):
    input = input_string.upper()
    reversed = input[::-1]
    if input == reversed:
        return True
    else:
        return False

class TestPalindrome(unittest.TestCase):

    def test_even_characters(self):
        self.assertTrue(palindrome("Anna"))

    def test_odd_characters(self):
        self.assertTrue(palindrome("Bob"))

    def test_invalid_palindrome(self):
        self.assertFalse(palindrome("cumul8"))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPalindrome)
    unittest.TextTestRunner(verbosity=2).run(suite)
