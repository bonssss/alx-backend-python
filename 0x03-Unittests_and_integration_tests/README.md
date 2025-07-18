# 0x03. Unittests and Integration Tests

This project is part of the **ALX Backend Specialization**. It focuses on writing unit and integration tests using Python’s `unittest` framework. You will learn how to use `parameterized`, `mock`, and best practices for testing real-world Python functions and classes.

---

## 🧪 Task 0: Parameterize a Unit Test

### Description
- Test the function `access_nested_map` from `utils.py`.
- Write a parameterized unit test using `@parameterized.expand`.
- Ensure the test method body is no longer than 2 lines.
- Use `assertEqual` to compare results.

### ✅ Tested Inputs

| nested_map               | path        | expected result |
|--------------------------|-------------|-----------------|
| `{"a": 1}`               | `("a",)`    | `1`             |
| `{"a": {"b": 2}}`        | `("a",)`    | `{"b": 2}`      |
| `{"a": {"b": 2}}`        | `("a", "b")`| `2`             |

### ✅ Sample Code
```python
@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
