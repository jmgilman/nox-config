from unittest import mock

from nox_config import linting, tool


def test_flake8_run(session: mock.MagicMock):
    f = linting.Flake8(config="test.conf")
    ctx = tool.Ctx()
    f.run(session, ctx)

    session.run.assert_called_once_with(
        "flake8", "--config", "test.conf", env={}
    )


def test_flake8_setup(session: mock.MagicMock):
    f = linting.Flake8(deps=["dep1"])
    f.setup(session)

    session.install.assert_called_once_with("flake8", "dep1")


def test_flake8_lint(session: mock.MagicMock):
    f = linting.Flake8(config="test.conf")
    ctx = tool.Ctx()
    f.lint(session, ["file1", "file2"], ctx)

    session.run.assert_called_once_with(
        "flake8", "--config", "test.conf", "file1", "file2", env={}
    )


def test_bandit_run(session: mock.MagicMock):
    b = linting.Bandit(config="test.conf")
    ctx = tool.Ctx()
    b.run(session, ctx)

    session.run.assert_called_once_with(
        "bandit", "--config", "test.conf", env={}
    )


def test_bandit_setup(session: mock.MagicMock):
    b = linting.Bandit(deps=["dep1"])
    b.setup(session)

    session.install.assert_called_once_with("bandit", "dep1")


def test_bandit_lint(session: mock.MagicMock):
    b = linting.Bandit(config="test.conf")
    ctx = tool.Ctx()
    b.lint(session, ["file1", "file2"], ctx)

    session.run.assert_called_once_with(
        "bandit", "--config", "test.conf", "file1", "file2", env={}
    )


def test_mypy_run(session: mock.MagicMock):
    m = linting.Mypy(config="test.conf")
    ctx = tool.Ctx()
    m.run(session, ctx)

    session.run.assert_called_once_with(
        "mypy", "--config-file", "test.conf", env={}
    )


def test_mypy_setup(session: mock.MagicMock):
    m = linting.Mypy(deps=["dep1"])
    m.setup(session)

    session.install.assert_called_once_with("mypy", "dep1")


def test_mypy_lint(session: mock.MagicMock):
    m = linting.Mypy(config="test.conf")
    ctx = tool.Ctx()
    m.lint(session, ["file1", "file2"], ctx)

    session.run.assert_called_once_with(
        "mypy", "--config-file", "test.conf", "file1", "file2", env={}
    )
