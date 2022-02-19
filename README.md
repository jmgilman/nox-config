# nox-helpers

<p align="center">
    <a href="https://github.com/jmgilman/loguricorn/actions/nox-helpers/ci.yml">
        <img src="https://github.com/jmgilman/loguricorn/actions/nox-helpers/ci.yml/badge.svg"/>
    </a>
    <a href="https://pypi.org/project/nox-helpers">
        <img src="https://img.shields.io/pypi/v/nox-helpers"/>
    </a>
</p>

> A package for abstracting common tools used in [nox][1] configs

## Usage

Install the package:

```shell
pip install nox-helpers
```

Add it to your existing `noxfile.py` configuration:

```python
from nox_helpers import formatting

black = formatting.Black(config="pyproject.toml")

@session(python="3.10")
def format(session: nox.Session):
    black.setup(session)
    black.check(session, ["."])
```

Additional parameters may be passed by including context:

```python
from nox_helpers import tooling

@session(python="3.10")
def format(session: nox.Session):
    black.setup(session)
    black.check(session, ["."], tooling.Ctx(flags=["--diff"]))
```

Alternatively, you can include the flag with every command:

```python
black = formatting.Black(config="pyproject.toml", flags=["--diff"])
```

## Customizing

The package ships with helpers for common tools used in Python development.
Adding additional helpers can be done by inheriting from the `Tool` class or
one of its subclasses. The below example shows the `Black` helper:

```python
from dataclasses import dataclass

import nox

from nox_helpers.tooling import Ctx, Tool


@dataclass
class Black(Formatter):
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
```

It inherits from the `Formatter` class which declares `check` and `format`
methods. The base `Tool` class contains two common methods used in all tooling:
`run` and `setup`. In most cases the only one you may need to override is the
`run` method. In the above case, the method checks to see if a configuration
was given and adds it to the flags of any command run. The two remaining
methods utilize this `run` method with additional flags and arguments depending
on what's being accomplished.

## Example

Here is a more full-featured example of a `noxfile.py`:

```python
import nox

from nox import session
from nox_helpers import formatting, linting, testing
from nox_helpers.tooling import Tools

PYTHON_VERSIONS = ["3.10"]

# Formatters
black = formatting.Black(config="pyproject.toml")
isort = formatting.ISort(config="pyproject.toml")
formatters = Tools([black, isort])

# Linters
flake8 = linting.Flake8()
mypy = linting.Mypy()
linters = Tools([flake8, mypy])

# Security
bandit = linting.Bandit()
security_linters = Tools([bandit])

# Testing
pytest = testing.Pytest(deps=["pytest_mock", "."])
testers = Tools([pytest])


@session(python=PYTHON_VERSIONS)
def format(session: nox.Session):
    formatters.setup(session) # Installs the tools and all declared deps
    for formatter in formatters:
        formatter.check(session, ["."]) # Validates files are formatted


@session(python=PYTHON_VERSIONS)
def lint(session: nox.Session):
    linters.setup(session)
    for linter in linters:
        linter.lint(session, ["."]) # Runs linting validation

    for linter in security_linters:
        linter.lint(session, ["my_pkg/"])


@session(python=PYTHON_VERSIONS)
def test(session: nox.Session):
    testers.setup(session)
    for tester in testers:
        tester.test(session, ["tests/"]) # Runs tests
```

## Testing

```shell
nox -s test
```

To generate a coverage report:

```shell
nox -s coverage
```

## Contributing

Check out the [issues][2] for items needing attention or submit your own and
then:

1. [Fork the repo][3]
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

[1]: https://nox.thea.codes/en/stable/
[2]: https://github.com/jmgilman/nox-helpers/issues
[3]: https://github.com/jmgilman/nox-helpers/fork
