import os
here = os.path.dirname(os.path.realpath(__file__))

rfid_json = open(here + "/rfid.json", "r").read()
weight_json = open(here + "/weight.json", "r").read()
valid_json = open(here + "/valid.json", "r").read()
invalid_json = "whoa there"
