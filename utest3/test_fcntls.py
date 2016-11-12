#!/usr/bin/env python3

import unittest

import pycapsicum as p

TFILE='/tmp/testfcntls'

class TestFCNTLS(unittest.TestCase):

    def setUp(self):
        super(TestFCNTLS, self).setUp()
        f = open(TFILE, 'w')
        f.write('foo')
        f.close()

    def test_limget(self):
        testf = open(TFILE, 'w')

        testlim = p.CAP_FCNTL_ALL

        p.fcntls_limit(testf, testlim)
        limit = p.fcntls_get(testf)
        self.assertEqual(limit, (testlim, 0))

        testlim2 = p.CAP_FCNTL_GETFL | p.CAP_FCNTL_GETOWN

        p.fcntls_limit(testf, testlim2)
        limit = p.fcntls_get(testf)
        self.assertEqual(limit, (testlim2, 0))
        testf.close()

if __name__ == '__main__':
    unittest.main()

