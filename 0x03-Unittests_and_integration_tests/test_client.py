#!/usr/bin/env python3
"""
Test suite for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient.org method."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected JSON payload."""
        # Arrange: prepare a fake return value for get_json
        expected_payload = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_payload

        # Act: create instance and call org()
        client = GithubOrgClient(org_name)
        result = client.org()

        # Assert: org() returns what get_json returned
        self.assertEqual(result, expected_payload)
        # Assert: get_json was called exactly once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
