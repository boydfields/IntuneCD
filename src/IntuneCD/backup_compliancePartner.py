#!/usr/bin/env python3

"""
This module backs up all Compliance Partners in Intune.
"""

from .clean_filename import clean_filename
from .graph_request import makeapirequest
from .save_output import save_output
from .remove_keys import remove_keys

# Set MS Graph endpoint
ENDPOINT = "https://graph.microsoft.com/beta/deviceManagement/complianceManagementPartners"


# Get all Compliance Partners and save them in specified path
def savebackup(path, output, token):
    """
    Saves all Compliance Partners in Intune to a JSON or YAML file.

    :param path: Path to save the backup to
    :param output: Format the backup will be saved as
    :param token: Token to use for authenticating the request
    """

    config_count = 0
    configpath = path + "/" + "Partner Connections/Compliance/"
    data = makeapirequest(ENDPOINT, token)

    for partner in data['value']:
        if partner['partnerState'] == "unknown":
            continue

        config_count += 1
        print("Backing up Compliance Partner: " + partner['displayName'])

        partner = remove_keys(partner)

        # Get filename without illegal characters
        fname = clean_filename(partner['displayName'])
        # Save Compliance policy as JSON or YAML depending on configured
        # value in "-o"
        save_output(output, configpath, fname, partner)

    return config_count
