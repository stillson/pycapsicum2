#!/usr/bin/env python3

import os.path

import unittest

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
        self.assertTrue(f.fileno() > -1)
        f.close()

if __name__ == '__main__':
    unittest.main()

