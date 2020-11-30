from jsonschema import validate


def test_all_todos(all_todos_schema, api_test):
    res = api_test.get()
    validate(res.json(), all_todos_schema)


def test_one_todos(one_todos_schema, api_test):
    res = api_test.get(1)
    validate(res.json(), one_todos_schema)
