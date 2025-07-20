#!/usr/bin/env python3
"""
Unittest for client.py module
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get with fixture payloads"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define side_effect to simulate requests.get().json()
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload.get("repos_url"):
                return MockResponse(cls.repos_payload)
            return None

        cls.mock_get.side_effect = lambda url: side_effect(url)

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list of repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license if specified"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


# Helper class for mock response object
class MockResponse:
    """Mocked response with json method"""
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json


if __name__ == '__main__':
    unittest.main()
