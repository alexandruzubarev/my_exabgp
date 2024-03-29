#!/usr/bin/env python
# encoding: utf-8
"""
parsing.py

Created by Thomas Mangin on 2009-09-06.
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

import unittest

import os
import glob

from exabgp.configuration.ancient import Configuration
from exabgp.configuration.check import check_neighbor

from exabgp.configuration.setup import environment
env = environment.setup('')
env.log.enable = True
env.log.all = False
env.log.configuration = False
env.log.parser = False

"""
@alexandru zubarev:
Defined class TestControl.
In the first method setUp, configuration file path is created and has the value of joined path attributes with the list of configuration files properties.
The test is checking the neighbor configuration for all loaded config files.  
"""
class TestControl (unittest.TestCase):
    def setUp (self):
        location = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','conf','*.conf'))
        self.files = glob.glob(location)

    # These files contains invalid attribute we can not parse
    skip = 'attributes.conf'

    def test_all_configuration (self):
        neighbors = []
        for filename in self.files:
            if filename.endswith(self.skip):
                continue
            print '-'*80
            print filename
            print '='*80
            configuration = Configuration([filename,])
            configuration.reload()
            self.assertEqual(check_neighbor(configuration.neighbor),True)
            del configuration

if __name__ == '__main__':
    unittest.main()
