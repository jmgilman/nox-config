from unittest import mock

from nox_helpers import tooling


def test_ctx_add():
    ctx = tooling.Ctx(
        flags=["--flag1"], args=["arg1"], env={"env1": "val1"}, test1="test"
    )
    ctx += tooling.Ctx(
        flags=["--flag2"], args=["arg2"], env={"env2": "val2"}, test2="test"
    )

    assert ctx.flags == ["--flag1", "--flag2"]
    assert ctx.args == ["arg1", "arg2"]
    assert ctx.env == {"env1": "val1", "env2": "val2"}
    assert ctx.kwargs == {"test1": "test", "test2": "test"}


def test_tooling_run(session: mock.MagicMock):
    t = tooling.Tool("tooling", flags=["--flag2"])
    ctx = tooling.Ctx(
        flags=["--flag1"], args=["arg1"], env={"env1": "val1"}, test1="test"
    )

    t.run(session, ctx)
    session.run.assert_called_once_with(
        "tooling",
        ctx.flags[0],
        "--flag2",
        ctx.args[0],
        env=ctx.env,
        test1="test",
    )


def test_tooling_setup(session: mock.MagicMock):
    t = tooling.Tool("tooling", deps=["dep1", "dep2"])

    t.setup(session, test="test1")
    session.install.assert_called_once_with(
        "tooling", "dep1", "dep2", test="test1"
    )


def test_toolings_setup(session: mock.MagicMock):
    t = [tooling.Tool("tooling1"), tooling.Tool("tooling2")]
    ts = tooling.Tools(t)

    ts.setup(session, test="test1")
    session.install.assert_any_call("tooling1", test="test1")
    session.install.assert_any_call("tooling2", test="test1")
    assert session.install.call_count == 2
