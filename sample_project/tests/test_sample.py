import unittest
import random
from sampleproject.sample import Sample


class TestSample(unittest.TestCase):

    def test_add(self):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        self.assertEqual(a+b,
                         Sample.add(a, b))


if __name__ == "__main__":
    unittest.main()
