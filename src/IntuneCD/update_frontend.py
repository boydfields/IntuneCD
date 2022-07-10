#!/usr/bin/env python3

"""
This module is used to update the IntuneCD frontend.
"""

import os
import requests

API_KEY = os.environ.get("API_KEY")


def update_frontend(frontend, data):
    """
    This function updates the frontend with the number of configurations, diff count backup stream and update stream.

    :param frontend: The frontend to update
    :param data: The data to update the frontend with
    """
    if not API_KEY:
        raise Exception("API_KEY environment variable is not set")

    else:
        headers = {'X-API-Key': API_KEY}
        response = requests.post(frontend, json=data, headers=headers)

        if response.status_code != 200:
            print("Error updating frontend")
            print(response.text)
