import pytest

POSTS_MAX = 200


"""
_______________________________________________________________
a) positive/negative тесты для Getting a resource
---------------------------------------------------------------
"""
@pytest.mark.parametrize('id', [1, POSTS_MAX])
def test_get_positive(api_test, id):
    res = api_test.get(id)

    assert res.status_code == 200
    assert res.json()['id'] == id


@pytest.mark.parametrize('id', [-1, POSTS_MAX + 1])
def test_get_negative(api_test, id):
    res = api_test.get(id)

    assert res.status_code == 404
    assert not res.json()


"""
_______________________________________________________________
b) positive тесты для Listing all resources
---------------------------------------------------------------
"""
def test_listing_positive(api_test):
    res = api_test.get()

    assert res.status_code == 200
    assert len(res.json()) == POSTS_MAX


"""
_______________________________________________________________
c) positive тесты для Creating a resource
---------------------------------------------------------------
"""
@pytest.mark.parametrize("userId", list(range(0,10,2)))
@pytest.mark.parametrize("title, body", [('foo', 'bar'), ('one', 'two')])
def test_create_positive(api_test, userId, title, body):
    payload = {'title': title, 'body': body, 'userId': userId}
    res = api_test.post(payload)

    # assert res.status_code == 201
    j = res.json()
    assert j['id'] == POSTS_MAX + 1
    assert j['userId'] == userId
    assert j['title'] == title
    assert j['body'] == body


"""
_______________________________________________________________
d) positive/negative тесты для Updating a resource with PUT. 
---------------------------------------------------------------
"""
@pytest.mark.parametrize("id, userId", list(zip(list(range(20,0,-2)), list(range(0,10,2)))))
@pytest.mark.parametrize("title, body", [('foo', 'bar'), ('one', 'two')])
def test_update_positive(api_test, id, userId, title, body):
    payload = {'title': title, 'body': body, 'userId': userId}
    res = api_test.put(payload, id)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['userId'] == userId
    assert res_json['id'] == id


@pytest.mark.parametrize("id, userId", [(1000, 1000), (2000, 2000)])
def test_update_negative(api_test, id, userId):
    payload = {'title': 'foo', 'body': 'bar', 'userId': userId}
    res = api_test.put(payload, id)

    assert res.status_code == 500


"""
_______________________________________________________________
e) positive тесты для Updating a resource with PATCH 
---------------------------------------------------------------
"""
@pytest.mark.parametrize("id", [1,2,3])
@pytest.mark.parametrize("title", ['foo', 'bar'])
def test_update_positive(api_test, id, title):
    payload = {'title': title}
    res = api_test.patch(payload, id)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['id'] == id
    assert res_json['title'] == title


"""
_______________________________________________________________
f) positive тесты для Deleting a resource 
---------------------------------------------------------------
"""
@pytest.fixture(scope="module", params=[1,2,3])
def id_value(request):
    yield request.param

def test_delete_positive(api_test, id_value):
    res = api_test.delete(id_value)

    assert res.status_code == 200
    assert not res.json()

"""
_______________________________________________________________
g) positive/negative тесты для Filtering resources. 
---------------------------------------------------------------
"""
@pytest.mark.parametrize("userId", list(range(0,10,2)))
def test_filtering_positive(api_test, userId):
    res = api_test.post(params={'userId': userId})

    # assert res.status_code == 201
    j = res.json()
    assert j['id'] == POSTS_MAX + 1


@pytest.mark.parametrize("id, userId", [(1000, 3000), (700, 900)])
@pytest.mark.parametrize("title, completed", [('foo', True), ('one', False)])
def test_filtering_negative(api_test, id, userId, title, completed):
    payload = {'title': title, 'completed': completed, 'userId': userId}
    res = api_test.post(params=payload)

    assert res.status_code == 201
    res_json = res.json()
    assert res_json["id"] == 201
