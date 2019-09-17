#!/usr/bin/python3
import bl_autocodes.code_fileparser as code_fileparser
import bl_autocodes.code_request as requester
from time import sleep
import random
# is also contained in general borderlands data/ cookies
cookieset = dict(
            prod_prod_ctlg_2_117="a",
            prod_prod_ctuc_2_117="a",
            prod_prod_ctut_2_117="a"
        )
    # session cookie contains %22 characters, better use token
session = ""

if __name__ == "__main__":
    tdicts = code_fileparser.parse_page()
    req = requester.blrequester(cookieset, session)
    for tdict in tdicts:
        name = tdict["name"]
        for entry in tdict["entries"]:
            r = random.uniform(1,4)
            req.request(name, entry)
            print("sleep for {} seconds before next request".format(r))
            sleep(r)