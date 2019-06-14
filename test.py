#!/usr/bin/env python3
#encoding:utf-8

""" unit tests.

"""

from collections import OrderedDict
import os
import copy
import unittest
from functionfaker.functionfaker import response_player, store

class TestFF(unittest.TestCase):
    """ Collect 3 dois that are known to be in PubMed
    """

    class TestMethods():
        # we need to set self argument to None, and a unittest class argument also to None.
        @response_player(args2ignore=[0])
        def add(self, x, y):
            return x + y

        @response_player(args2ignore=[0])
        def test_dict_function(self, D = None):
            if D is not None:
                return list(D.keys())[0]

    test_methods = TestMethods()

    def setUp(self):

        os.environ['RECORD'] = ""
        print('Setting up %s'%type(self).__name__)
        store.clear()

    def tearDown(self):
        os.environ['RECORD'] = ""
        print('Tearing down %s'%type(self).__name__)
        store.clear()

    def test_add_result_after_recording(self):

        print("*Recording and replaying add*")
        os.environ['RECORD'] = "record"
        self.test_methods.add(1,2)

        os.environ['RECORD'] = "replay"
        result = self.test_methods.add(1,2)

        self.assertEqual(result, 3)


    def test_key_in_recording(self):

        print("*Recording and checking responses key*")
        os.environ['RECORD'] = "record"
        self.test_methods.add(1,2)

        D = store._load_responses()
        key = store.hash_args(['add',None,1,2,{}])

        self.assertEqual(key in D, True)

    def test_key_value_in_recording(self):

        print("*Recording and checking responses value*")
        os.environ['RECORD'] = "record"
        self.test_methods.add(1,2)

        D = store._load_responses()
        key = store.hash_args(['add',None,1,2,{}])

        self.assertEqual(D.get(key, 0), 3)


    def test_ordering_of_dicts_doesnt_matter(self):
        print("*Testing ordering of dicts effect*")
        os.environ['RECORD'] = "record"
        self.test_methods.test_dict_function(OrderedDict([(1,2), (4,5)]))

        # The order of the dict elements should not matter
        os.environ['RECORD'] = "replay"
        result = self.test_methods.test_dict_function( OrderedDict([(4,5), (1,2) ]) )

        self.assertEqual(result, 1)



if __name__ == '__main__':


    unittest.main()
