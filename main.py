import bl_autocodes.code_fileparser as code_fileparser
import bl_autocodes.code_request as requester
from time import sleep
import random

if __name__ == "__main__":
    tdicts = code_fileparser.parse_page()
    req = requester.blrequester()
    for tdict in tdicts:
        name = tdict["name"]
        for entry in tdict["entries"]:
            r = random.uniform(1,4)
            req.request(name, entry)
            print("sleep for {} seconds".format(r))
            sleep(r)
            # kann alles in die requester logic rein
            #   pt_str = ""
            #   if points >= 0:
            #       pt_str += "- Received {} points".format(points)
            #   print("[{}] status for code {}  {}".format(status, code, pt_str))
#