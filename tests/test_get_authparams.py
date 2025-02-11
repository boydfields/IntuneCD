#!/usr/bin/env python3

"""
This module tests the get_authparams function.
"""

import unittest

from unittest.mock import patch
from testfixtures import TempDirectory
from src.IntuneCD.get_authparams import getAuth


@patch('src.IntuneCD.get_authparams.getAuth')
@patch('src.IntuneCD.get_authparams.obtain_accesstoken', return_value="token")
class TestGetAuth(unittest.TestCase):
    """Test class for get_auth."""

    def setUp(self):
        self.directory = TempDirectory()
        self.directory.create()
        self.directory.write(
            'auth_dev.json',
            '{"params": {"DEV_CLIENT_ID": "test", "DEV_CLIENT_SECRET": "test", "DEV_TENANT_NAME": "test"}}',
            encoding='utf-8')
        self.directory.write(
            'auth_prod.json',
            '{"params": {"PROD_CLIENT_ID": "test", "PROD_CLIENT_SECRET": "test", "PROD_TENANT_NAME": "test"}}',
            encoding='utf-8')
        self.directory.write(
            'auth.json',
            '{"params": {"CLIENT_ID": "test", "CLIENT_SECRET": "test", "TENANT_NAME": "test"}}',
            encoding='utf-8')
        self.auth_dev_json = self.directory.path + '/auth_dev.json'
        self.auth_prod_json = self.directory.path + '/auth_prod.json'
        self.auth_json = self.directory.path + '/auth.json'

    def tearDown(self):
        self.directory.cleanup()

    def test_get_auth_devtoprod_env_dev(
            self, mock_getAuth, mock_obtain_accesstoken):
        """The auth params should be returned."""
        with patch.dict('os.environ', {'DEV_CLIENT_ID': 'test', 'DEV_CLIENT_SECRET': 'test', 'DEV_TENANT_NAME': 'test'}):
            result = getAuth('devtoprod', localauth=None, tenant='DEV')
            self.assertEqual(result, "token")

    def test_get_auth_devtoprod_env_prod(
            self, mock_getAuth, mock_obtain_accesstoken):
        """The auth params should be returned."""
        with patch.dict('os.environ', {'PROD_CLIENT_ID': 'test', 'PROD_CLIENT_SECRET': 'test', 'PROD_TENANT_NAME': 'test'}):
            result = getAuth('devtoprod', localauth=None, tenant='PROD')
            self.assertEqual(result, "token")

    def test_get_auth_devtoprod_localauth_dev(
            self, mock_getAuth, mock_obtain_accesstoken):
        """The auth params should be returned."""
        result = getAuth(
            'devtoprod',
            localauth=self.auth_dev_json,
            tenant='DEV')
        self.assertEqual(result, "token")

    def test_get_auth_devtoprod_localauth_prod(
            self, mock_getAuth, mock_obtain_accesstoken):
        """The auth params should be returned."""
        result = getAuth(
            'devtoprod',
            localauth=self.auth_prod_json,
            tenant='PROD')
        self.assertEqual(result, "token")

    def test_get_auth_standalone_env(
            self, mock_getAuth, mock_obtain_accesstoken):
        """The auth params should be returned."""
        with patch.dict('os.environ', {'CLIENT_ID': 'test', 'CLIENT_SECRET': 'test', 'TENANT_NAME': 'test'}):
            result = getAuth('standalone', localauth=None, tenant=None)
            self.assertEqual(result, "token")

    def test_get_auth_standalone_localauth(
            self, mock_getAuth, mock_obtain_accesstoken):
        """The auth params should be returned."""
        result = getAuth('standalone', localauth=self.auth_json, tenant=None)
        self.assertEqual(result, "token")

    def test_get_auth_devtoprod_missing_env_dev(
            self, mock_getAuth, mock_obtain_accesstoken):
        """Exception should be raised due to missing env."""
        with patch.dict('os.environ', {'DEV_CLIENT_ID': 'test', 'DEV_CLIENT_SECRET': 'test'}):
            with self.assertRaises(Exception):
                getAuth('devtoprod', localauth=None, tenant='DEV')

    def test_get_auth_devtoprod_missing_env_prod(
            self, mock_getAuth, mock_obtain_accesstoken):
        """Exception should be raised due to missing env."""
        with patch.dict('os.environ', {'PROD_CLIENT_ID': 'test', 'PROD_CLIENT_SECRET': 'test'}):
            with self.assertRaises(Exception):
                getAuth('devtoprod', localauth=None, tenant='PROD')

    def test_get_auth_standalone_missing_env(
            self, mock_getAuth, mock_obtain_accesstoken):
        """Exception should be raised due to missing env."""
        with patch.dict('os.environ', {'CLIENT_ID': 'test', 'CLIENT_SECRET': 'test'}):
            with self.assertRaises(Exception):
                getAuth('standalone', localauth=None, tenant=None)


if __name__ == '__main__':
    unittest.main()
