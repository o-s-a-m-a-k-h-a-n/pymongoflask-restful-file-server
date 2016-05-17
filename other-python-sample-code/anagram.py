import unittest

def anagram(first_string, second_string):
    first_set = list(first_string.upper())
    second_set = list(second_string.upper())
    first_set.sort()
    second_set.sort()
    return (first_set == second_set)

class TestAnagram(unittest.TestCase):

    def test_case_a(self):
        self.assertTrue(anagram("Anna","Nana"))

    def test_case_b(self):
        self.assertTrue(anagram("Tops","Pots"))

    def test_case_c(self):
        self.assertFalse(anagram("StanleyCup","Cannucks"))
    
    def test_case_d(self):
        self.assertFalse(anagram("anagrams", "anagramz"))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnagram)
    unittest.TextTestRunner(verbosity=2).run(suite)
