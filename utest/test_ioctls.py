#!/usr/bin/env python

import unittest2 as unittest

import pycapsicum as p

TFILE='/tmp/testioctls'

class TestIOCTLS(unittest.TestCase):

    def setUp(self):
        super(TestIOCTLS, self).setUp()
        f = open(TFILE, 'w')
        f.write('foo')
        f.close()

    def test_limget(self):
        testf = open(TFILE, 'rw')

        testlim = [1,2,3,4,5]

        p.ioctls_limit(testf, testlim)
        limit = p.ioctls_get(testf)
        self.assertEquals(limit, (len(testlim),testlim) )

        testlim2 = [1,2,5]

        p.ioctls_limit(testf, testlim2)
        limit = p.ioctls_get(testf)
        self.assertEquals(limit, (len(testlim2),testlim2) )

if __name__ == '__main__':
    unittest.main()

