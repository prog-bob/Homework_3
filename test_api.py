import pytest

POSTS_MAX = 200


# a) positive/negative тесты для Getting a resource
@pytest.mark.parametrize('id', [1, POSTS_MAX])
def test_get_positive(api_test, id):
    res = api_test.get(id)

    assert res.status_code == 200
    assert res.json()['id'] == id


@pytest.mark.parametrize('id', [-1, 0, POSTS_MAX + 1])
def test_get_negative(api_test, id):
    res = api_test.get(id)

    assert res.status_code == 404
    assert not res.json()


# b) positive тесты для Listing all resources
def test_listing_positive(api_test):
    res = api_test.get()

    assert res.status_code == 200
    assert len(res.json()) == POSTS_MAX


# c) positive тесты для Creating a resource
def test_create_positive(api_test):
    payload = {'title': 'foo', 'body': 'bar', 'userId': 1, "completed": True}
    res = api_test.post(payload)
    assert res.status_code == 201
    j = res.json()
    assert j['id'] == POSTS_MAX + 1
    assert j['userId'] == 1
    assert j['title'] == 'foo'
    assert j['body'] == 'bar'
    assert j['completed'] is True


# d) positive/negative тесты для Updating a resource with PUT.
def test_update_positive(api_test):
    payload = {'title': 'foo', 'body': 'bar', 'userId': 1, "completed": True}
    res = api_test.put(payload, 2)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['userId'] == 1
    assert res_json['title'] == 'foo'
    assert res_json['body'] == 'bar'
    assert res_json['completed'] is True
    assert res_json['id'] == 2


@pytest.mark.parametrize("id, userId", [(1000, 1000), (1000, 1)])
def test_update_negative(api_test, id, userId):
    payload = {'title': 'foo', 'body': 'bar', 'userId': userId}
    res = api_test.put(payload, id)

    assert res.status_code == 500


# e) positive тесты для Updating a resource with PATCH
@pytest.mark.parametrize("id", [1, 2, 3])
@pytest.mark.parametrize("title", ['foo', 'bar'])
def test_update_patch_positive(api_test, id, title):
    payload = {'title': title,  "completed": False}
    res = api_test.patch(payload, id)

    assert res.status_code == 200
    res_json = res.json()
    assert res_json['id'] == id
    assert res_json['title'] == title
    assert res_json['completed'] is False


# f) positive тесты для Deleting a resource
def test_delete_positive(api_test):
    res = api_test.delete(1)

    assert res.status_code == 200
    assert not res.json()


# g) positive/negative тесты для Filtering resources.
def test_filtering_positive(api_test):
    res = api_test.get(params={'userId': 10,
                               'id': 194,
                               'title': 'sed ut vero sit molestiae'})

    j = res.json()[0]
    assert j['title'] == 'sed ut vero sit molestiae'
    assert j['completed'] is False
    assert j['id'] == 194
    assert j['userId'] == 10


def test_filtering_negative(api_test):
    res = api_test.get(params={'userId': 1,
                               'id': 1,
                               'title': 'no title',
                               'completed': False})

    res_json = res.json()
    assert len(res_json) == 0
