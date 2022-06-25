import requests
from src.EntryPayload import EntryPayload
from src.utils.config import get_config

ROOT_URL = "https://us-central1-mk64-ad77f.cloudfunctions.net"


def post_time(payload):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # Below we are encoding the payload as form-encoded
    # If it needs to be URL-encoded, change `data` to `params
    return requests.post(ROOT_URL + '/addTime', headers=headers, data=payload)


def send_to_gus(new_time, slug, rtype="NA"):
    cfg = get_config()
    payload = EntryPayload(cfg['userID'], slug, new_time, rtype)
    post_time(payload.to_json())
