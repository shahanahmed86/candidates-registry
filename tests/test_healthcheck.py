from os import uname

from fastapi import Response

from .utils import client


def test_healthcheck():
    response: Response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == f"I am healthy at {uname().nodename}"
