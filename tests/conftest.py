import pytest
from pytest_mock import plugin


@pytest.fixture
def session(mocker: plugin.MockerFixture):
    return mocker.patch("nox.Session")
