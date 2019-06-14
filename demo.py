#!/usr/bin/env python3

from functionfaker import response_player, store
import os
import requests
import json

@response_player()
def add(x, y):
    return x + y

@response_player()
def get_geonames(url, params):

    response = requests.get(url, params = params)
    return json.loads(response.content.decode("utf-8"))

if __name__ == "__main__":

    # remove any previous responses
    store.clear()

    # enter record mode, to record function responses.
    os.environ['RECORD'] = "record"
    # call the add function to record some responses.
    add(1,2)
    add(1,y=3)
    add(1,3)
    add(2,1)

    # call the geonames API for Wagga Wagga to record a response.
    parameters = {"username" : "willem.sijp" , "type" : "json", "placename" : "wagga", "countrycode" : "au"}
    url = 'http://api.geonames.org/postalCodeSearch'
    response = get_geonames(url, parameters)

    # enter replay mode, so that function will not run, but return stored values instead.
    os.environ['RECORD'] = "replay"

    result = add(1,2)
    print("The saved result of adding 1 and 2 using function 'add' is %d"%result)

    response = get_geonames(url, parameters)
    print("The saved API response:")
    print(response)

    # clean up responses
    store.clear()
