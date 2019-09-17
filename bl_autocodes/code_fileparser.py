# parse files or parse websites directly
import requests
from pyquery import PyQuery
import pdb
page = "https://www.giga.de/tipp/borderlands-3-vip-und-shift-codes-aktuelle-liste-fuer-goldene-schluessel-und-loot/"


def parse_page():
    r = requests.get(page)
    html_response = r.text
    pq = PyQuery(html_response)
    tag = pq('div.table-responsive')
    pdb.set_trace()

if __name__ == "__main__":
    parse_page()