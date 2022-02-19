from dataclasses import dataclass

import nox

from nox_helpers.tooling import Ctx, Tool


@dataclass
class Tester(Tool):
    """A tool which is used for testing source code.

    This class provides a loose interface for tools which fall under the
    category of testers.
    """

    def test(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        """Tests the given list of files.

        Args:
            session: The session in which to run this tool.
            files: A list of files to test.
        """
        pass


@dataclass
class Pytest(Tester):
    """A class for interacting with the pytest testing suite.

    Args:
        config: An optional configuration file to pass with all executions.
    """

    binary: str = "pytest"
    config: str = ""

    def run(self, session: nox.Session, ctx: Ctx = Ctx()):
        if self.config:
            ctx += Ctx(flags=["-c", self.config])

        super().run(session, ctx)

    def test(self, session: nox.Session, files: list[str], ctx: Ctx = Ctx()):
        ctx += Ctx(args=files)
        self.run(session, ctx)
