import requests
from src.EntryPayload import EntryPayload
from src.utils.config import get_config


def post_time(payload):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # Below we are encoding the payload as form-encoded
    # If it needs to be URL-encoded, change `data` to `params
    return requests.post(get_config()['db-endpoint'], headers=headers, data=payload)


def send_to_gus(new_time, slug, rtype="NA"):
    cfg = get_config()
    payload = EntryPayload(cfg['userID'], slug, new_time, rtype)
    post_time(payload.to_dict())
