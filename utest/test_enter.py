#!/usr/bin/env python

import unittest2 as unittest

import pycapsicum as p

class TestESG(unittest.TestCase):

    def test_esg(self):
        p.enter()
        self.assertTrue(p.sandboxed())
        self.assertTrue(p.getmode() == 1)

if __name__ == '__main__':
    unittest.main()

