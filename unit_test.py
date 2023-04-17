import os
import unittest
import json
from dotenv import load_dotenv
from unittest import mock
from unittest.mock import MagicMock, patch
from app import scan
import pkg_resources


class TestGetScan(unittest.TestCase):

    @mock.patch.dict(os.environ, {'NETBOXURL': 'localhost:27017', 'NETBOXTOKEN': '1234'})
    def test_getScan(self):
        self.assertEqual(os.environ['NETBOXURL'], 'localhost:27017')
        # Mock external dependencies
        mock_requests_get = MagicMock()
        mock_requests_get.return_value.json.return_value = {
            "results": [
                {
                    "primary_ip4": {
                        "address": "192.168.0.1/24"
                    },
                    "site": {
                        "slug": "hmc-coporate-headquaters"
                    }
                },
                {
                    "primary_ip4": {
                        "address": "192.168.0.2/24"
                    },
                    "site": {
                        "slug": "remote-site"
                    }
                }
            ]
        }
        mock_subprocess_run = MagicMock(return_value=MagicMock(returncode=0))

        # Patch the external dependencies
        with patch('requests.get', mock_requests_get), \
                patch('subprocess.run', mock_subprocess_run):
            # Call the function being tested
            response = scan.getScan()
            response_data = json.loads(response.data)
            # Assertions
            self.assertIsNotNone(response)
            self.assertIsNotNone(response_data)
            self.assertEqual(len(response_data['devicesMain']), 1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response_data['devicesMain']), 1)
            self.assertEqual(len(response_data['devicesRemote']), 1)
            self.assertEqual(response_data['upDevicesMain'], 1)
            self.assertEqual(response_data['upDevicesRemote'], 1)
            self.assertEqual(response_data['downDevicesMain'], 0)
            self.assertEqual(response_data['downDevicesRemote'], 0)

    def test_getScan_error(self):
        # Test error handling when an exception is raised
        with patch('requests.get', side_effect=Exception('Test Exception')):
            response = scan.getScan()
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, b'Test Exception')

    def test_requirements(self):
        with open('requirements.txt') as f:
            requirements = [line.strip() for line in f.readlines()]
            for requirement in requirements:
                try:
                    pkg_resources.require(requirement)
                except pkg_resources.DistributionNotFound:
                    self.fail(
                        f"Requirement '{requirement}' not found in requirements.txt")
