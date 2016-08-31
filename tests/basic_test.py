import unittest
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from bouncer.door import doorcheck
from bouncer.door import doorcounter
from bouncer.door import doorlock
from bouncer.door import doorunlock

class TestBasic(unittest.TestCase):
    def test_nothing(self):
        pass


if __name__ == '__main__':
    unittest.main()
