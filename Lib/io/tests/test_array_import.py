#!/usr/bin/env python

# This python script tests the numpyio module.
# also check out numpyio.fread.__doc__ and other method docstrings.

import os
import unittest
from unittest import TestCase
import scipy
import scipy.io.numpyio as numpyio
from scipy import io, stats
from scipy import rand
from scipy_test.testing import assert_array_equal, assert_equal, assert_approx_equal
from scipy_test.testing import assert_almost_equal, assert_array_almost_equal
import Numeric
N = Numeric
import tempfile

class test_numpyio(TestCase):
    def check_basic(self):
        # Generate some data
        a = 255*rand(20)
        # Open a file
        fname = tempfile.mktemp('.dat')
        fid = open(fname,"wb")
        # Write the data as shorts
        numpyio.fwrite(fid,20,a,Numeric.Int16)
        fid.close()
        # Reopen the file and read in data
        fid = open(fname,"rb")
        print "\nDon't worry about a warning regarding the number of bytes read."
        b = numpyio.fread(fid,1000000,Numeric.Int16,Numeric.Int)
        fid.close()
        assert(N.product(a.astype(N.Int16) == b))
        os.remove(fname)

class test_read_array(TestCase):
    def check_complex(self):
        a = rand(13,4) + 1j*rand(13,4)
        fname = tempfile.mktemp('.dat')
        io.write_array(fname,a)
        b = io.read_array(fname,atype=scipy.Complex)
        assert_array_almost_equal(a,b,decimal=4)
        os.remove(fname)

    def check_float(self):
        a = rand(3,4)*30
        fname = tempfile.mktemp('.dat')
        io.write_array(fname,a)
        b = io.read_array(fname)
        assert_array_almost_equal(a,b,decimal=4)
        os.remove(fname)

    def check_integer(self):
        a = stats.randint(1,20,size=(3,4))
        fname = tempfile.mktemp('.dat')
        io.write_array(fname,a)
        b = io.read_array(fname,atype=scipy.Int)
        assert_array_equal(a,b)
        os.remove(fname)

def test_suite(level=1):
    suites = []
    if level > 0:
        suites.append( unittest.makeSuite(test_read_array, 'check_') )
        suites.append( unittest.makeSuite(test_numpyio, 'check_') )
        
    total_suite = unittest.TestSuite(suites)
    return total_suite

def test(level=10):
    all_tests = test_suite(level=level)
    runner = unittest.TextTestRunner()
    runner.run(all_tests)
    return runner

if __name__ == "__main__":
    test()


        
