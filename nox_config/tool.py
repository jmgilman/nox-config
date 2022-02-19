from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar

import nox

T = TypeVar("T", bound="Tool")


@dataclass
class Ctx:
    """Context information passed when running a tool.

    This class serves as the primary pipeline for getting data from the initial
    call context all the way down to invoking session.run() with a Nox session.
    It breaks up the normal run() input into a combination of flags, arguments,
    and environment variables. The addition operator is defined to allow adding
    two Ctx's together. In this case, the RHS flags/args are added after the
    LHS flags/args. For example:

        ctx = Ctx(flags=["--flag1"])
        ctx += Ctx(flags=["--flag2"])
        assert ctx.flags == ["--flag1", "--flag2"]

    The constructor supports ingesting additional arbirary keyword arguments.
    These are also additive and will be passed down to session.run().

    Attributes:
        flags: Command-line flags to pass
        args: Command-line arguments to pass
        env: Environment variables to be set
    """

    flags: list[str]
    args: list[str]
    env: dict[str, str]

    def __init__(
        self,
        flags: list[str] = [],
        args: list[str] = [],
        env: dict[str, str] = {},
        **kwargs,
    ):
        self.flags = flags
        self.args = args
        self.env = env
        self.kwargs = kwargs

    def __add__(self, other: Ctx):
        return Ctx(
            flags=self.flags + other.flags,
            args=self.args + other.args,
            env=self.env | other.env,
            **(self.kwargs | other.kwargs),
        )


@dataclass
class Tool:
    """An arbitrary tool used in a nox configuration.

    This class serves as the base class from which all tools inherit from. It
    provides methods for installing the tool and it's dependencies as well as
    running arbitrary commands using the tool. Many tools are provided out of
    the box by this package, however, additional ones can be created by
    inheriting from this class.

    Attributes:
        binary: The name of the binary for this tool.
        deps: Additional dependencies required to run this tool.
    """

    binary: str
    deps: list[str] = field(default_factory=list)

    def run(self, session: nox.Session, ctx: Ctx = Ctx()):
        """Runs this tool using the session and context.

        Args:
            session: The session to run this tool in.
            ctx: The context to use for running the tool.
        """
        session.run(
            self.binary, *ctx.flags, *ctx.args, env=ctx.env, **ctx.kwargs
        )

    def setup(self, session: nox.Session, **kwargs) -> None:
        """Installs this tool and any declared dependencies using the session.

        Args:
            session: The session to install this tool in.
        """
        session.install(self.binary, *self.deps, **kwargs)


class Tools(list[T]):
    """A list of Tool's.

    This class provides a thin wrapper around a list of Tool objects. It
    provides a single method for performing setup on all tools contained in the
    list.
    """

    def setup(self, session: nox.Session, **kwargs) -> None:
        """Installs all tools contained in this list using the session.

        Args:
            session: The session to install the tools in.
        """
        for tool in self:
            tool.setup(session, **kwargs)
