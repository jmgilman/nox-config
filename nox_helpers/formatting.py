from __future__ import annotations

from dataclasses import dataclass

import nox

from nox_helpers.tooling import Ctx, Tool


@dataclass
class Formatter(Tool):
    """A tool which is used for formatting source code.

    This class provides a loose interface for tools which fall under the
    category of formatters.
    """

    def check(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        """Validates the given list of files is formatted correctly.

        Args:
            session: The session in which to run this tool.
            files: A list of files to validate.
        """
        pass

    def format(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        """Formats the given list of files.

        Args:
            session: The session in which to run this tool.
            files: A list of files to format.
        """
        pass


@dataclass
class Black(Formatter):
    """A class for interacting with the black formatter.

    Args:
        config: An optional configuration file to pass with all executions.
    """

    binary: str = "black"
    config: str = ""

    def run(self, session: nox.Session, ctx: Ctx = Ctx()):
        if self.config:
            ctx += Ctx(flags=["--config", self.config])

        super().run(session, ctx)

    def check(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        ctx += Ctx(flags=["--check"], args=files)
        self.run(session, ctx)

    def format(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        ctx += Ctx(args=files)
        self.run(session, ctx)


@dataclass
class ISort(Formatter):
    """A class for interacting with the isort formatter.

    Args:
        config: An optional configuration file to pass with all executions.
    """

    binary: str = "isort"
    config: str = ""

    def run(self, session: nox.Session, ctx: Ctx = Ctx()):
        if self.config:
            ctx += Ctx(flags=["--settings-path", self.config])

        super().run(session, ctx)

    def check(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        ctx += Ctx(flags=["--check-only"], args=files)
        self.run(session, ctx)

    def format(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        ctx += Ctx(args=files)
        self.run(session, ctx)
