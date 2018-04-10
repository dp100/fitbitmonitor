from requests import *
import json, sys
from vaultClient import *
refresh_url = "https://api.fitbit.com/oauth2/token"

vault = vaultClient("http://172.17.0.1:8200","jenkins", sys.argv[1])

fitbituser = vault.get("fitbit/fitbituser")
fitbittoken = vault.get("fitbit/fitbittoken")["value"]


def getMetric(metric, version):
    metric_headers = {
        "Authorization": "Bearer %s" % fitbittoken,
        "Accept": "application/json"
    }
    metric_url = "https://api.fitbit.com/%s/user/-/" % version
    print("Getting %s" % metric_url+metric)

    try:
        value=get(str(metric_url+metric), headers=metric_headers).json()
    except Exception:
        print(Exception)
        value = 0

    return value


def prettyprint(string):
    print(json.dumps(string, indent=4, sort_keys=True))
