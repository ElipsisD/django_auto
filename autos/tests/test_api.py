import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ("url_name", "title", "status"), [
        pytest.param("home", "Главная страница", 200,
                     id="home api status code"),
        pytest.param("autos", "Автомобили", 200,
                     id="autos api status code"),
        pytest.param("spares", "Запчасти", 200,
                     id="spares api status code"),
        pytest.param("error", "Ошибка", 400,
                     marks=pytest.mark.xfail,
                     id="error test"),
    ],
)
def test_home_api(url_name: str, title: str, status: int, client: Client) -> None:
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == status
    assert response.context_data["title"] == title
