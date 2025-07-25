#!/usr/bin/env python3
"""
Unittest for client.py module with integration testing
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class MockResponse:
    """Mocked response object for requests.get().json()"""
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_payload, mock_get_json):
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
        client = GithubOrgClient("google")
        self.assertEqual(
            client._public_repos_url,
            "https://api.github.com/orgs/google/repos"
        )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            client = GithubOrgClient("google")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        ({"license": {"key": "私のライセンス"}}, "my_license", True),
        ({"license": {"key": "他のライセンス"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for the public_repos method"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and provide fixtures"""
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            else:
                raise ValueError(f"Unexpected URL: {url}")

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

    def test_public_repos_empty(self):
        """Test public_repos with empty repos_payload"""
        self.mock_get.side_effect = lambda url: MockResponse(self.org_payload) if url == "https://api.github.com/orgs/google" else MockResponse([])
        client = GithubOrgClient("google")
        stef.assertEqual(client.public_repos(), [])

    def test_public_repos_with_invalid_license(self):
        """Test public_repos with repos missing license"""
        invalid_repos = [{"name": "repo1", "license": None}, {"name": "repo2"}]
        self.mock_get.side_effect = lambda url: MockResponse(self.org_payload) if url == "https://api.github.com/orgs/google" else MockResponse(invalid_repos)
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), [])


if __name__ == '__main__':
    unittest.main()