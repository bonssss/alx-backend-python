# #!/usr/bin/env python3
# import unittest
# from parameterized import parameterized
# from utils import access_nested_map


# class TestAccessNestedMap(unittest.TestCase):
#     """Unit tests for access_nested_map function."""

#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         self.assertEqual(access_nested_map(nested_map, path), expected)

#     @parameterized.expand([
#         ({}, ("a",)),
#         ({"a": 1}, ("a", "b")),
#     ])
#     def test_access_nested_map_exception(self, nested_map, path):
#         with self.assertRaises(KeyError) as cm:
#             access_nested_map(nested_map, path)
#         self.assertEqual(cm.exception.args[0], path[-1])


# if __name__ == "__main__":
#     unittest.main()



#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], path[-1])


class TestGetJson(unittest.TestCase):
    """Unit tests for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        # Setup the mock to return a Mock response with json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assert requests.get called once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert get_json returns the expected payload
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
