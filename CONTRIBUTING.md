# Contributing to gdpy

Thanks for your interest in contributing to gdpy! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Adding New Endpoints](#adding-new-endpoints)
- [Documentation](#documentation)
- [Testing](#testing)

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gdpy.git
   cd gdpy
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

Install the project with development dependencies:

```bash
# Using uv (recommended)
uv sync --all-extras

# Or using pip
pip install -e ".[dev]"
```

### Running Checks

Before submitting changes, run all checks:

```bash
# Linting
uv run ruff check gdpy/

# Formatting
uv run ruff format gdpy/

# Type checking
uv run mypy gdpy/

# Run tests
uv run pytest

# Run all checks at once
uv run ruff check gdpy/ && uv run mypy gdpy/ && uv run pytest
```

## Project Structure

```
gdpy/
├── gdpy/
│   ├── __init__.py         # Public API exports
│   ├── client.py           # Client and AsyncClient classes
│   ├── constants.py        # API constants (URLs, secrets)
│   ├── exceptions.py       # Exception classes
│   ├── crypto/             # Cryptographic utilities
│   │   ├── base64.py       # Base64 encoding/decoding
│   │   ├── chk.py          # CHK generation
│   │   ├── gjp.py          # GJP2 encoding
│   │   └── xor.py          # XOR cipher
│   ├── models/             # Pydantic models
│   │   ├── __init__.py     # Model exports
│   │   └── user.py         # User, Level, Comment, etc.
│   └── utils/              # Utility functions
│       └── parsing.py      # Response parsing
├── docs/                   # Documentation
├── tests/                  # Test files
├── pyproject.toml          # Project configuration
└── README.md
```

## Coding Standards

### Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible

### Code Formatting

We use [Ruff](https://docs.astral.sh/ruff/) for formatting and linting:

```bash
# Format code
uv run ruff format gdpy/

# Fix linting issues
uv run ruff check gdpy/ --fix
```

### Type Annotations

All functions must have type annotations:

```python
# Good
def get_level(self, level_id: int) -> Level:
    ...

# Bad
def get_level(self, level_id):
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def get_user(self, account_id: int) -> User:
    """Get a user by their account ID.

    Args:
        account_id: The account ID of the user.

    Returns:
        A User object with the user's information.

    Raises:
        NotFoundError: If the user is not found.

    Example:
        ```python
        user = client.get_user(account_id=71)
        print(user.username)
        ```
    """
```

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:

```
feat: add upload_level endpoint
fix: handle rate limiting errors correctly
docs: update API coverage table
refactor: simplify LevelDifficulty enum
```

## Pull Requests

1. **Create a feature branch** from `main`
2. **Make your changes** following the coding standards
3. **Run all checks** before pushing:
   ```bash
   uv run ruff check gdpy/ && uv run mypy gdpy/ && uv run pytest
   ```
4. **Push your branch** and open a Pull Request
5. **Describe your changes** in the PR description
6. **Link any related issues** using GitHub keywords (e.g., "Fixes #123")

### PR Checklist

- [ ] Code follows the project's style guidelines
- [ ] All checks pass (ruff, mypy, pytest)
- [ ] New features have appropriate tests
- [ ] Documentation is updated if needed
- [ ] Commit messages follow conventional commits

## Adding New Endpoints

When adding a new API endpoint:

### 1. Check the API Documentation

Refer to the [gd-docs](https://github.com/Rifct/gd-docs) repository for endpoint specifications.

### 2. Add the Method

Add the method to both `Client` (sync) and `AsyncClient` (async) classes:

```python
# In Client class
def new_endpoint(self, param: int) -> ReturnType:
    """Method description.

    Args:
        param: Parameter description.

    Returns:
        Return type description.

    Raises:
        RuntimeError: If not authenticated.
    """
    if not self.is_authenticated:
        raise RuntimeError("Must be authenticated")
    data = {
        "accountID": str(self._account_id),
        "gjp2": self._get_gjp2(),
        "param": str(param),
    }
    response = self._request("endpointName.php", data)
    return ReturnType.model_validate(parse_response(response))

# In AsyncClient class
async def new_endpoint(self, param: int) -> ReturnType:
    """Method description."""
    if not self.is_authenticated:
        raise RuntimeError("Must be authenticated")
    data = {
        "accountID": str(self._account_id),
        "gjp2": self._get_gjp2(),
        "param": str(param),
    }
    response = await self._request("endpointName.php", data)
    return ReturnType.model_validate(parse_response(response))
```

### 3. Create Models (if needed)

Add new Pydantic models in `gdpy/models/user.py`:

```python
class NewModel(BaseModel):
    """Description of the model.

    Attributes:
        field1: Field description.
        field2: Field description.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    field1: int = Field(alias="1")
    field2: str = Field(default="", alias="2")
```

### 4. Export the Model

Add the model to `gdpy/models/__init__.py`.

### 5. Update Documentation

- Update `docs/api-coverage.md` with the new endpoint status
- Update `docs/index.md` coverage summary
- Update the "Missing Features" section if applicable

## Documentation

### Building Docs Locally

```bash
uv run mkdocs serve
```

This starts a local server at `http://127.0.0.1:8000`.

### Updating API Coverage

When adding endpoints, update the coverage in both files:

1. `docs/api-coverage.md` - Detailed endpoint table
2. `docs/index.md` - Summary table

Calculate correct percentages using Python:

```python
total_implemented = sum([3, 4, 10, 7, 3, 12, 4, 2, 1, 2])  # Add your values
total_endpoints = sum([5, 4, 11, 7, 6, 12, 4, 3, 3, 2])     # Add your values
print(f"{total_implemented}/{total_endpoints} = {total_implemented/total_endpoints*100:.0f}%")
```

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=gdpy

# Run specific test file
uv run pytest tests/test_crypto.py

# Run specific test
uv run pytest tests/test_crypto.py::TestCrypto::test_xor_cipher
```

### Writing Tests

Tests should be placed in the `tests/` directory:

```python
import pytest
from gdpy import Client


def test_new_feature():
    """Test description."""
    with Client() as client:
        result = client.new_endpoint(param=123)
        assert result.field1 == 123
```

## Need Help?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Ask questions in issue discussions

Thank you for contributing! 🎮
