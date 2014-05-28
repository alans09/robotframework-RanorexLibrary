""" Unittests of rxconnector module """
import unittest
import os
import sys
sys.path.append(os.path.abspath('..\\..'))
from src.rxconnector import RanorexLibrary


class RanorexLibraryTest(unittest.TestCase):
    """ Basic unittests for rxconnector """
    def setUp(self):
        self.sut = RanorexLibrary()

    def test__return_type_valid(self):
        """ Test to check if correct element is asociated """
        result = self.sut._RanorexLibrary__return_type('/cell')
        self.assertEquals(result, 'Cell')

    def test__return_type_invalid(self):
        """ Test if correct exception is raised when unknown element """
        with self.assertRaises(AssertionError) as context:
            self.sut._RanorexLibrary__return_type('/cedll')
        self.assertEqual(context.exception.message,
                         'Element is not supported. Entered element: cedll')

    def test__return_type_empty(self):
        """ Test if correct exception is raised when no element """
        with self.assertRaises(AssertionError) as context:
            self.sut._RanorexLibrary__return_type('')
        self.assertEqual(context.exception.message, 'No element entered')


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(RanorexLibraryTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
