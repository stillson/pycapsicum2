#!/usr/bin/env python

import os.path

import unittest2 as unittest

import pycapsicum as p

TFILE  = '/tmp/testOpen'
TDIR   = os.path.dirname(TFILE)
TFNAME = os.path.basename(TFILE)


class TestOpen(unittest.TestCase):

    def setUp(self):
        super(TestOpen, self).setUp()
        f = open(TFILE, 'w')
        f.write('foo')
        f.close()

    def test_limget(self):

        testd = p.opendir(TDIR, 'r')
        self.assertTrue(testd > -1)
        f = p.openat(testd,TFNAME, 'r')
        self.assertTrue(f > -1)

if __name__ == '__main__':
    unittest.main()

