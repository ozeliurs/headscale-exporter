import logging
import os

import requests

log = logging.getLogger('werkzeug')

BASE_URL = os.environ.get("HEADSCALE_BASE_URL")
API_KEY = os.environ.get("HEADSCALE_API_KEY")

if not BASE_URL or not API_KEY:
    raise ValueError("HEADSCALE_BASE_URL and HEADSCALE_API_KEY must be set")

if not BASE_URL.endswith("/"):
    BASE_URL += "/"

if not BASE_URL.endswith("/api/v1/"):
    BASE_URL += "api/v1/"

if not BASE_URL.startswith("http"):
    BASE_URL = "http://" + BASE_URL

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def get_users():
    url = f"{BASE_URL}user"
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception as e:
        from app import app
        log.error(f"Error getting users: {e} with response code: {response.status_code}\n{response.text}")
        raise e


def get_machines():
    url = f"{BASE_URL}machine"
    response = requests.get(url, headers=headers)

    if not response.ok:
        url = f"{BASE_URL}node"
        response = requests.get(url, headers=headers)

    try:
        return response.json()
    except Exception as e:
        from app import app
        log.error(f"Error getting machines: {e} with response code: {response.status_code}\n{response.text}")
        raise e


def get_routes():
    url = f"{BASE_URL}routes"
    response = requests.get(url, headers=headers)
    try:
        js = response.json()

        for route in js["routes"]:
            if not route.get("machine"):
                route["machine"] = route.get("node")

        return js
    except Exception as e:
        from app import app
        log.error(f"Error getting routes: {e} with response code: {response.status_code}\n{response.text}")
        raise e


def get_all():
    return {**get_users(), **get_machines(), **get_routes()}
