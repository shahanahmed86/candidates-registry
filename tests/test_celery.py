from library.celery import add


def test_add_task():
    result = add(4, 6)
    assert result == 10
