from dataclasses import dataclass

import nox

from nox_tools.tooling import Ctx, Tool


@dataclass
class Linter(Tool):
    """A tool which is used for linting source code.

    This class provides a loose interface for tools which fall under the
    category of linters.
    """

    def lint(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        """Lints the given list of files.

        Args:
            session: The session in which to run this tool.
            files: A list of files to lint.
        """
        pass


@dataclass
class Bandit(Linter):
    """A class for interacting with the bandit linter.

    Args:
        config: An optional configuration file to pass with all executions.
    """

    binary: str = "bandit"
    config: str = ""

    def run(self, session: nox.Session, ctx: Ctx = Ctx()):
        if self.config:
            ctx += Ctx(flags=["--config", self.config])

        super().run(session, ctx)

    def lint(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        ctx += Ctx(args=files)
        self.run(session, ctx)


@dataclass
class Flake8(Linter):
    """A class for interacting with the flake8 linter.

    Args:
        config: An optional configuration file to pass with all executions.
    """

    binary: str = "flake8"
    config: str = ""

    def run(self, session: nox.Session, ctx: Ctx = Ctx()):
        if self.config:
            ctx += Ctx(flags=["--config", self.config])

        super().run(session, ctx)

    def lint(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        ctx += Ctx(args=files)
        self.run(session, ctx)


@dataclass
class Mypy(Linter):
    """A class for interacting with the mypy linter.

    Args:
        config: An optional configuration file to pass with all executions.
    """

    binary: str = "mypy"
    config: str = ""

    def run(self, session: nox.Session, ctx: Ctx = Ctx()):
        if self.config:
            ctx += Ctx(flags=["--config-file", self.config])

        super().run(session, ctx)

    def lint(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        ctx += Ctx(args=files)
        self.run(session, ctx)
