#!/usr/bin/env python3

import unittest

import pycapsicum as p

TFILE='/tmp/testioctls'

class TestIOCTLS(unittest.TestCase):

    def setUp(self):
        super(TestIOCTLS, self).setUp()
        f = open(TFILE, 'w')
        f.write('foo')
        f.close()

    def test_limget(self):
        testf = open(TFILE, 'w')

        testlim = [1,2,3,4,5]

        p.ioctls_limit(testf, testlim)
        limit = p.ioctls_get(testf)
        self.assertEqual(limit, (len(testlim),testlim) )

        testlim2 = [1,2,5]

        p.ioctls_limit(testf, testlim2)
        limit = p.ioctls_get(testf)
        self.assertEqual(limit, (len(testlim2),testlim2) )

        testf.close()

if __name__ == '__main__':
    unittest.main()

