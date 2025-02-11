#!/usr/bin/env python3

"""
This module backs up all App Protection Policies in Intune.
"""

import re

from .clean_filename import clean_filename
from .graph_request import makeapirequest
from .graph_batch import batch_assignment, get_object_assignment
from .save_output import save_output
from .remove_keys import remove_keys

# Set MS Graph endpoint
q_param = {
    "$filter": "(microsoft.graph.managedApp/appAvailability) eq null or (microsoft.graph.managedApp/appAvailability) "
               "eq 'lineOfBusiness' or isAssigned eq true"}
ENDPOINT = "https://graph.microsoft.com/beta/deviceAppManagement/mobileApps"


def match(platform, input) -> bool:
    """
    This function matches the platform from the @odata.type.

    :param platform: The platform to match
    :param input: The OData type
    :return: False if no match, True if match
    """

    string = f'.*{platform}.*$'
    pattern = re.compile(string)
    match = pattern.match(input, re.IGNORECASE)
    return bool(match)


# Get all applications and save them in specified path
def savebackup(path, output, exclude, token):
    """
    Saves all applications in Intune to a JSON or YAML file.

    :param path: Path to save the backup to
    :param output: Format the backup will be saved as
    :param exclude: If "assignments" is in the list, it will not back up the assignments
    :param token: Token to use for authenticating the request
    """

    config_count = 0

    data = makeapirequest(ENDPOINT, token, q_param)
    assignment_responses = batch_assignment(
        data, 'deviceAppManagement/mobileApps/', '/assignments', token)

    for app in data['value']:
        app_name = ""
        platform = ""
        config_count += 1

        if "assignments" not in exclude:
            assignments = get_object_assignment(
                app['id'], assignment_responses)
            if assignments:
                app['assignments'] = assignments

        app = remove_keys(app)
        app.pop('description', None)

        # If app type is VPP, add Apple ID to the name as the app can exist
        # multiple times
        if app['@odata.type'] == '#microsoft.graph.iosVppApp':
            app_name = app['displayName'] + '_iOSVppApp_' + \
                str(app['vppTokenAppleId'].split('@')[0])
        elif app['@odata.type'] == '#microsoft.graph.macOsVppApp':
            app_name = app['displayName'] + '_macOSVppApp_' + \
                str(app['vppTokenAppleId'].split('@')[0])
        # If app type is Win32 or MSI, add version to the name as multiple
        # versions can exist
        elif app['@odata.type'] == '#microsoft.graph.win32LobApp':
            if app['displayVersion'] is None:
                app_name = app['displayName'] + '_Win32'
            else:
                app_name = app['displayName'] + '_Win32_' + \
                    str(app['displayVersion']).replace('.', '_')
        elif app['@odata.type'] == '#microsoft.graph.windowsMobileMSI':
            app_name = app['displayName'] + '_WinMSI_' + \
                str(app['productVersion']).replace('.', '_')
        # If app is not VPP, Win32 or MSI only add the app type to the name
        else:
            app_name = app['displayName'] + '_' + \
                str(app['@odata.type'].split('.')[2])

        # Get application platform
        if match('ios', str(app['@odata.type']).lower()) is True:
            platform = 'iOS'
        if match('macos', str(app['@odata.type']).lower()) is True:
            platform = 'macOS'
        if match('android', str(app['@odata.type']).lower()) is True:
            platform = 'Android'
        if match('windows', str(app['@odata.type']).lower()) is True:
            platform = 'Windows'
        if match('microsoft', str(app['@odata.type']).lower()) is True:
            platform = 'Windows'
        if match('win32', str(app['@odata.type']).lower()) is True:
            platform = 'Windows'
        if match('office', str(app['@odata.type']).lower()) is True:
            platform = 'Office Suite'
        if app['@odata.type'] == '#microsoft.graph.webApp':
            platform = 'Web App'

        print(f"Backing up Application: {app['displayName']}")

        configpath = f'{path}/Applications/{platform}/'

        # Get filename without illegal characters
        fname = clean_filename(app_name)

        save_output(output, configpath, fname, app)

    return config_count
