from unittest import mock

from nox_config import tool


def test_ctx_add():
    ctx = tool.Ctx(
        flags=["--flag1"], args=["arg1"], env={"env1": "val1"}, test1="test"
    )
    ctx += tool.Ctx(
        flags=["--flag2"], args=["arg2"], env={"env2": "val2"}, test2="test"
    )

    assert ctx.flags == ["--flag1", "--flag2"]
    assert ctx.args == ["arg1", "arg2"]
    assert ctx.env == {"env1": "val1", "env2": "val2"}
    assert ctx.kwargs == {"test1": "test", "test2": "test"}


def test_tool_run(session: mock.MagicMock):
    t = tool.Tool("tool")
    ctx = tool.Ctx(
        flags=["--flag1"], args=["arg1"], env={"env1": "val1"}, test1="test"
    )

    t.run(session, ctx)
    session.run.assert_called_once_with(
        "tool", ctx.flags[0], ctx.args[0], env=ctx.env, test1="test"
    )


def test_tool_setup(session: mock.MagicMock):
    t = tool.Tool("tool", deps=["dep1", "dep2"])

    t.setup(session, test="test1")
    session.install.assert_called_once_with(
        "tool", "dep1", "dep2", test="test1"
    )


def test_tools_setup(session: mock.MagicMock):
    t = [tool.Tool("tool1"), tool.Tool("tool2")]
    ts = tool.Tools(t)

    ts.setup(session, test="test1")
    session.install.assert_any_call("tool1", test="test1")
    session.install.assert_any_call("tool2", test="test1")
    assert session.install.call_count == 2
