#!/usr/bin/env python3
#encoding:utf-8

""" unit tests.

"""

from collections import OrderedDict
import os
import copy
import unittest
from functionfaker import response_player, responder

class TestFF(unittest.TestCase):
    """ Collect 3 dois that are known to be in PubMed
    """

    # we need to set self argument to None, and a unittest class argument also to None.
    @response_player(args2ignore=[0,1])
    def add(self, x, y):
        return x + y

    @response_player(args2ignore=[0,1])
    def test_dict_function(self, D):
        return list(D.keys())[0]

    def setUp(self):

        print('Setting up %s'%type(self).__name__)

        responder.clear()

    def tearDown(self):
        print('Tearing down %s'%type(self).__name__)

        responder.clear()

    def test_add_result_after_recording(self):
        responder.clear()

        os.environ['RECORD'] = "record"
        self.add(1,2)

        os.environ['RECORD'] = "replay"
        result = self.add(1,2)

        self.assertEqual(result, 3)


    def test_key_in_recording(self):
        responder.clear()

        os.environ['RECORD'] = "record"
        self.add(1,2)

        D = responder._load_responses()
        key = responder.hash_args([None,None,1,2,{}])

        self.assertEqual(key in D, True)

    def test_key_value_in_recording(self):
        responder.clear()

        os.environ['RECORD'] = "record"
        self.add(1,2)

        D = responder._load_responses()
        key = responder.hash_args([None,None,1,2,{}])

        self.assertEqual(D.get(key, 0), 3)


    def test_ordering_of_dicts_doesnt_matter(self):
        responder.clear()

        os.environ['RECORD'] = "record"
        self.test_dict_function(OrderedDict([(1,2), (4,5)]))

        # The order of the dict elements should not matter
        os.environ['RECORD'] = "replay"
        result = self.test_dict_function( OrderedDict([(4,5), (1,2) ]) )

        self.assertEqual(result, 1)



if __name__ == '__main__':


    unittest.main()
