from __future__ import (absolute_import, division, print_function)

import os
import unittest

from lxml import etree

from wof.examples.flask.cbi.cbi_sos_parser import parse_datavalues_from_get_observation


@unittest.skip("DOA needs work to build a cache, and update tests to be valid")
class TestCbiParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_datavalues_from_get_observation(self):

        path = os.path.join(
            os.path.dirname(__file__),
            'cbi_sos_examples',
            'cbi_get_observations.xml'
        )

        f = open(path)
        tree = etree.parse(f)

        dataval_list = \
            parse_datavalues_from_get_observation(tree, '014',
                                                  'water_temperature')

        self.assertTrue(dataval_list)
        self.assertTrue(len(dataval_list) == 2)

        for datavalue in dataval_list:
            self.assertTrue(datavalue.DataValue)
