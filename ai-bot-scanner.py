import requests as r
import json
import time

API_KEY = "rl_fhTUzGUbMKYH26Sgquu7vQoPu"

def doRequest(endpoint, args = {}):
    return r.get(
        f"https://api.stackexchange.com/2.3/{endpoint}",
        params =  {
            "key": API_KEY,
            "pagesize": 100,
            **args
        },
    )

sites = []

print("Gathering sites")
page = 1
while True:
    res = doRequest("sites", {
        "page": page
    })

    if res.status_code != 200:
        print("Rate limited")
        time.sleep(5)
        continue

    j = res.json()
    for site in j["items"]:
        if site["site_state"] == "linked_meta":
            continue
        sites.append(site["api_site_parameter"])
    print("Accumulated sites:", len(sites))

    if j["has_more"] == False:
        print("All sites found")
        break
    page += 1


print()

siteIdx = 0

while siteIdx < len(sites):
    res = doRequest("users/-2", {"site": sites[siteIdx]})
    if res.status_code != 200:
        print("Rate limited")
        time.sleep(10)
        continue

    if len(res.json()["items"]) == 1:
        print(sites[siteIdx], "has a shitty misinformation bot")

    siteIdx += 1
