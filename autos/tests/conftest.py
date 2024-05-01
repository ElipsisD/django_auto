import pytest


@pytest.fixture()
def client():
    from django.test import Client
    return Client()
