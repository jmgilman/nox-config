from unittest import mock

from nox_tools import testing, tooling


def test_pytest_run(session: mock.MagicMock):
    p = testing.Pytest(config="test.conf")
    ctx = tooling.Ctx()
    p.run(session, ctx)

    session.run.assert_called_once_with("pytest", "-c", "test.conf", env={})


def test_pytest_setup(session: mock.MagicMock):
    p = testing.Pytest(deps=["dep1"])
    p.setup(session)

    session.install.assert_called_once_with("pytest", "dep1")


def test_pytest_lint(session: mock.MagicMock):
    p = testing.Pytest(config="test.conf")
    ctx = tooling.Ctx()
    p.test(session, ["file1", "file2"], ctx)

    session.run.assert_called_once_with(
        "pytest", "-c", "test.conf", "file1", "file2", env={}
    )
