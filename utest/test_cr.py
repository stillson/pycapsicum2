#!/usr/bin/env python

import unittest2 as unittest

import pycapsicum as p

TFILE='/tmp/testfcntls'

class TestCR(unittest.TestCase):

    def setUp(self):
        super(TestCR, self).setUp()
        f = open(TFILE, 'w')
        f.write('foo')
        f.close()

    def test_cr(self):
        testf = open(TFILE, 'rw')

        cr1 = p.CapRights()
        self.assertEquals(cr1.caps, [])


        caps2 = ['CAP_READ', 'CAP_MMAP', "CAP_LOOKUP"]
        cr2 = p.CapRights(caps2)
        self.assertEquals(cr2.caps, caps2)

        clear_caps = ['CAP_MMAP', 'CAP_FLOCK']
        after_caps = sorted(list(set(caps2) - set(clear_caps)))
        cr2.clear(clear_caps)
        self.assertEquals( sorted(cr2.caps), after_caps)

        self.assertTrue( cr2.is_set(after_caps))
        self.assertFalse(cr2.is_set(caps2))

        self.assertTrue(cr2.is_valid())

        cr3 = p.CapRights(clear_caps)
        cr2.merge(cr3)

        after_caps2 = sorted(list(set(caps2).union(set(clear_caps))))
        self.assertEqual(sorted(cr2.caps), after_caps2)

        self.assertTrue(cr2.contains(cr3))
        self.assertFalse(cr1.contains(cr3))

        cr2.remove(cr3)
        self.assertEqual(sorted(cr2.caps), after_caps)

        cr2.limit(testf)
        cr3.get(testf)

        self.assertEqual(cr2.caps, cr3.caps)

if __name__ == '__main__':
    unittest.main()

