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


def test_black_check(session: mock.MagicMock):
    b = formatters.Black()
    ctx = tool.Ctx()
    b.check(session, ["file1", "file2"], ctx)

    session.run.assert_called_once_with(
        "black", "--check", "file1", "file2", env={}
    )


def test_black_format(session: mock.MagicMock):
    b = formatters.Black()
    ctx = tool.Ctx()
    b.format(session, ["file1", "file2"], ctx)

    session.run.assert_called_once_with("black", "file1", "file2", env={})


def test_isort_run(session: mock.MagicMock):
    i = formatters.ISort(config="test.conf")
    ctx = tool.Ctx()
    i.run(session, ctx)

    session.run.assert_called_once_with(
        "isort", "--settings-path", "test.conf", env={}
    )


def test_isort_setup(session: mock.MagicMock):
    i = formatters.ISort(deps=["dep1"])
    i.setup(session)

    session.install.assert_called_once_with("isort", "dep1")


def test_isort_check(session: mock.MagicMock):
    i = formatters.ISort()
    ctx = tool.Ctx()
    i.check(session, ["file1", "file2"], ctx)

    session.run.assert_called_once_with(
        "isort", "--check-only", "file1", "file2", env={}
    )


def test_isort_format(session: mock.MagicMock):
    i = formatters.ISort()
    ctx = tool.Ctx()
    i.format(session, ["file1", "file2"], ctx)

    session.run.assert_called_once_with("isort", "file1", "file2", env={})
