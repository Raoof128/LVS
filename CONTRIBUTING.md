# Contributing to LLM Vulnerability Scanner

Thank you for your interest in contributing to the LLM Vulnerability Scanner! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/llm-security/vuln-scanner.git
   cd vuln-scanner
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   make install-dev
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests**
   ```bash
   make test
   ```

4. **Format and lint your code**
   ```bash
   make format
   make lint
   ```

### Code Quality Standards

All code must meet the following standards:

- **Type Hints**: All functions must have type hints
- **Docstrings**: All public functions and classes must have docstrings following Google style
- **Testing**: New features must include unit tests with >80% coverage
- **Formatting**: Code must pass `black` and `isort` formatting
- **Linting**: Code must pass `flake8` and `mypy` checks

### Adding New Scanner Modules

To add a new vulnerability scanner module:

1. Create a new file in `backend/engines/` (e.g., `new_scanner.py`)
2. Inherit from `ScannerModule` base class
3. Implement the `scan()` method
4. Add corresponding tests in `tests/`
5. Update the scanner list in `backend/api/scan.py`
6. Document the OWASP category mapping

Example:
```python
from typing import List
from .base import ScannerModule
from .target_wrapper import TargetLLM
from .risk_engine import Vulnerability, Severity

class NewScanner(ScannerModule):
    """Scanner for NEW_VULNERABILITY_TYPE."""
    
    def scan(self, target: TargetLLM) -> List[Vulnerability]:
        vulnerabilities = []
        # Implementation here
        return vulnerabilities
```

## Pull Request Process

1. **Update documentation** - Ensure README and relevant docs are updated
2. **Add tests** - All new code must have tests
3. **Pass CI checks** - All tests and linting must pass
4. **Request review** - Tag relevant maintainers
5. **Address feedback** - Respond to review comments

### Pull Request Template

```
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added
- [ ] All tests passing
- [ ] Linting passing

## Related Issues
Closes #(issue number)
```

## Reporting Bugs

Submit bug reports via GitHub Issues with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Logs and error messages

## Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- Clear use case
- Expected benefits
- Implementation approach (if applicable)

## Questions?

Open a GitHub Discussion or contact the maintainers.

Thank you for contributing! 🎉
