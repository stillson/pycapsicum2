#!/usr/bin/env python

import unittest2 as unittest

import pycapsicum as p

TFILE='/tmp/testfcntls'

class TestFCNTLS(unittest.TestCase):

    def setUp(self):
        super(TestFCNTLS, self).setUp()
        f = open(TFILE, 'w')
        f.write('foo')
        f.close()

    def test_limget(self):
        testf = open(TFILE, 'rw')

        testlim = p.CAP_FCNTL_ALL

        p.fcntls_limit(testf, testlim)
        limit = p.fcntls_get(testf)
        self.assertEquals(limit, (testlim, 0))

        testlim2 = p.CAP_FCNTL_GETFL | p.CAP_FCNTL_GETOWN

        p.fcntls_limit(testf, testlim2)
        limit = p.fcntls_get(testf)
        self.assertEquals(limit, (testlim2, 0))

if __name__ == '__main__':
    unittest.main()

