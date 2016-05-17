import unittest

def fizz_buzz():
    result = []
    for i in range(1,101):
        result.append("fizz"*(i%3==0) + "buzz"*(i%5==0) or i)
    return result

class TestFizzBuzz(unittest.TestCase):

    def test_fizz(self):
        self.assertEqual(fizz_buzz()[2],'fizz')

    def test_buzz(self):
        self.assertEqual(fizz_buzz()[4], 'buzz')

    def test_fizzbuzz(self):
        self.assertEqual(fizz_buzz()[44], 'fizzbuzz')

    def test_number_type(self):
        self.assertTrue(fizz_buzz()[88], type(1))

    def test_number_value(self):
        self.assertTrue(fizz_buzz()[88], 89)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFizzBuzz)
    unittest.TextTestRunner(verbosity=2).run(suite)
