import json

redeemed_file = "redeemed_codes.txt"

def redcode(code):
    with open(redeemed_file, "a") as f:
        f.write(code+"\n")

def save_redeemed(code, response):
    txt = response.text
    json_resp = json.loads(response.text)
    if "points" in json_resp:
        redcode(code)
    elif "exception" in json_resp:
        if "model" in json_resp["exception"]:
            red_str = "This entry has already been redeemed."
            inv_str = "This entry is invalid."
            resp_str = json_resp["exception"]["model"]
            if resp_str == red_str or resp_str == inv_str:
                redcode(code)


def loadred():
    try:
        with open(redeemed_file, "r") as f:
            fread = f.readlines()
        return [x.strip("\n") for x in fread]
    except FileNotFoundError:
        redcode("Redeemed_Codes:")
        return []
    

def is_redeemed(code, redeemed):
    if code in redeemed:
        return True
    else:
        return False