import unittest
from unittest import TestCase

from petstagram.pets.models import Pet


class TestPte(TestCase):
    def setUp(self) -> None:
        self.pet = Pet('Dog', 'name', 'age')

    def test_pet_with_correct_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
