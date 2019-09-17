# parse files or parse websites directly
import requests
from bs4 import BeautifulSoup
import pdb
page = "https://www.giga.de/tipp/borderlands-3-vip-und-shift-codes-aktuelle-liste-fuer-goldene-schluessel-und-loot/"


def parse_page():
    r = requests.get(page)
    html_response = r.text
    soup = BeautifulSoup(html_response, 'html.parser')
    html_tables = soup.select('div.table-responsive')
    value_table_list = []
    for html_table in html_tables:
        #print(html_table.prettify())
        name = html_table.select("td")[0]
        entries = html_table.select("tr")[1:]
        value_table = parse_tables(name, entries)
        value_table_list.append(value_table)
    return value_table_list
    #print(tables[0].prettify())
    #pdb.set_trace()

def parse_tables(name, entries):
    # for VIP table there is an additional column indicating the code type
    # this does not exist for shift table
    tdict = {}
    tdict["name"] = name.text
    tdict["entries"] = []
    for entry in entries:
        pentry = ""
        if "VIP" in tdict["name"]:
            if len(entry.select("td"))>1:
                pentry = parse_VIP(tdict, entry)
        elif "Shift" in tdict["name"]:
            pentry = parse_Shift(tdict, entry)
        else:
            print("[ERROR] cannot identify table type on this page")
            return
        if pentry:
            tdict["entries"].append(pentry)
    return tdict

def parse_VIP(tdict, entry):
    return (entry.select("td")[0].text, entry.select("td")[1].text)

def parse_Shift(tdict, entry):
    return entry.select("td")[0].text

if __name__ == "__main__":
    vtl = parse_page()
    for tl in vtl:
        print(tl)