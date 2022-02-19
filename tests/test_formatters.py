from unittest import mock

from nox_config import formatters, tool


def test_black_run(session: mock.MagicMock):
    b = formatters.Black(config="test.conf")
    ctx = tool.Ctx()
    b.run(session, ctx)

    session.run.assert_called_once_with(
        "black", "--config", "test.conf", env={}
    )


def test_black_setup(session: mock.MagicMock):
    b = formatters.Black(deps=["dep1"])
    b.setup(session)

    session.install.assert_called_once_with("black", "dep1")


def test_isort_run(session: mock.MagicMock):
    b = formatters.ISort(config="test.conf")
    ctx = tool.Ctx()
    b.run(session, ctx)

    session.run.assert_called_once_with(
        "isort", "--settings-path", "test.conf", env={}
    )


def test_isort_setup(session: mock.MagicMock):
    b = formatters.ISort(deps=["dep1"])
    b.setup(session)

    session.install.assert_called_once_with("isort", "dep1")
