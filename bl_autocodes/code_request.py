import requests
import json
import pdb
import random
import logging
import bl_autocodes.code_redeemer as redeemer

class blrequester():
    base_url = "https://2kgames.crowdtwist.com"
    base_referer = "/widgets/t/code-redemption/"
    base_request_url = "/code-redemption-campaign/redeem?cid="
    logging.basicConfig(level=logging.INFO)
    shift_base = "https://api.2k.com/borderlands/code/"
    shift_end = "/redeem/epic"
    shift_referer = "https://borderlands.com/en-US/vip-codes/"
    headerset = {
            "content-type": "application/json;charset=UTF-8",
            "accept-encoding": "gzip, deflate, br",
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
        }
    # is also contained in general borderlands data/ cookies
    cookieset = dict(
            prod_prod_ctlg_2_117="",
            prod_prod_ctuc_2_117="",
            prod_prod_ctut_2_117=""
        )
    # session cookie contains %22 characters, better use token
    session = ""

    def __init__(self):
        # get user and password and send request 
        # in order to get "token" and "prod_*" -cookies
        pass

    def __init__(self,cookieset, session, redeemed):
        self.cookieset = cookieset
        self.session = session
        self.redeemed = redeemed
        
    def request(self, name, entry):
        retval = False
        if "VIP" in name:
            #pass
            retval = self.request_vip(entry, self.headerset, self.cookieset)
        elif "Shift" in name:
            #pass
            retval = self.request_shift(entry, self.headerset, self.session)
        else:
            print("[ERROR] unknown code table")
        return retval


    def request_vip(self, entry, headerset, cookieset):
        code, etype = entry
        payload = {"code": code}
        sendout = False
        if not redeemer.is_redeemed(code,self.redeemed):
            if "Vault" in etype:
                referer = "9896/"
                request_url = "5261"
                sendout = True
            elif "E-Mail" in etype:
                referer = "9902/"
                request_url = "5264"
                sendout = True
            elif "Creator" in etype:
                # TODO
                pass
            else: 
                print("[ERROR] unknown code type")
        if sendout:
            headerset["referer"] = self.base_url + self.base_referer + referer
            headerset["cookie"] = "; ".join([a[0]+"="+a[1] for a in cookieset.items()])
            full_url = self.base_url + self.base_request_url + request_url
            response = requests.post(full_url, json=payload, headers=headerset)
            redeemer.save_redeemed(code,response)
            self.print_response(etype, code, response)
        return sendout



    def print_response(self, etype, code, response):
        msg = "[TYPE: {}] code:\"{}\" response: {} ".format(etype, code, response.text)
        logging.info(msg)

    def request_shift(self, entry, headerset, session):
        if redeemer.is_redeemed(entry,self.redeemed):
            return False
        # set additional headers to net get in trouble with CORS
        headerset["Origin"] = "https://borderlands.com"
        headerset["Sec-Fetch-Mode"] = "cors"
        headerset["referer"] = self.shift_referer
        headerset["X-SESSION"] = session
        #
        # prepare the transaction and get the job_id in order to do a succesful transaction
        full_url = self.shift_base + entry + self.shift_end
        response = requests.post(full_url, headers=headerset)
        json_response = json.loads(response.text)
        if "job_id" in json_response:
            job_id = json_response["job_id"]
            full_url = self.shift_base + entry + "/job/" + job_id
            response = requests.get(full_url, headers=headerset)
            redeemer.save_redeemed(entry,response)
        else:
            logging.info("[ERROR] could not evaluate job id from response: {}".format(response))
        #something is missing here:
        # generated error: INFO:root:[TYPE: shift] code:"ZFKJ3-TT3BB-JTBJT-T3JJT-JWX9H" response: {"error":"JOB_STILL_QUEUED","min_wait_milliseconds":250,"max_wait_milliseconds":500} 
        # in a second round code gets handled as ALREADY_REDEEMED
        self.print_response("shift", entry, response)
        return True


if __name__ == "__main__":
    pass

