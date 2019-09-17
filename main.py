import bl_autocodes.code_fileparser as code_fileparser
import bl_autocodes.code_request as requester

if __name__ == "__main__":
    codes = code_fileparser.parse()
    for code in codes:
        status, points = requester.request(code)
        pt_str = ""
        if points >= 0:
            pt_str += "- Received {} points".format(points)
        print("[{}] status for code {}  {}".format(status, code, pt_str))
        