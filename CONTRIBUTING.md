# Contributing to ANTIVIRUS 🛡️

Thank you for considering contributing to ANTIVIRUS! This project is built by the community, for the community. Whether you're fixing bugs, adding features, improving documentation, or sharing threat intelligence, your contributions are valued.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Security Vulnerabilities](#security-vulnerabilities)

---

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors.

### Our Principles

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Collaborative**: Work together to build something great
- **Be Professional**: Keep discussions constructive and on-topic
- **Be Open**: Share knowledge and help others learn
- **Be Secure**: Never share or commit sensitive information

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling, insulting, or derogatory remarks
- Publishing others' private information
- Sharing malware or exploit code without proper context
- Any conduct that could be considered inappropriate

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip or poetry for package management
- Basic understanding of cybersecurity concepts

### Fork and Clone

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/Antivirus.git
cd Antivirus

# Add upstream remote
git remote add upstream https://github.com/Blackmvmba88/Antivirus.git
```

---

## 💻 Development Setup

### 1. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n antivirus python=3.8
conda activate antivirus
```

### 2. Install Dependencies

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Verify Installation

```bash
# Run tests
python -m pytest

# Check code style
flake8 antivirus/
black --check antivirus/

# Run the CLI
antivirus --help
```

---

## 🔧 How to Contribute

### Types of Contributions

1. **Bug Fixes** 🐛
   - Fix existing issues
   - Improve error handling
   - Optimize performance

2. **New Features** ✨
   - Implement roadmap items
   - Add new detection methods
   - Enhance CLI capabilities

3. **Documentation** 📚
   - Improve README
   - Write tutorials
   - Add code comments

4. **Threat Intelligence** 🧠
   - Submit malware signatures
   - Share attack patterns
   - Update detection rules

5. **Testing** 🧪
   - Write unit tests
   - Create integration tests
   - Improve test coverage

### Finding Issues to Work On

- Check [Good First Issues](https://github.com/Blackmvmba88/Antivirus/labels/good%20first%20issue)
- Look for [Help Wanted](https://github.com/Blackmvmba88/Antivirus/labels/help%20wanted) labels
- Review the [Roadmap](docs/roadmap.md) for upcoming features

---

## 📝 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length**: 100 characters max
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings
- **Imports**: Grouped and alphabetically sorted

### Code Formatting

We use **Black** for automatic code formatting:

```bash
# Format your code
black antivirus/

# Check formatting
black --check antivirus/
```

### Linting

We use **flake8** for linting:

```bash
# Run linter
flake8 antivirus/

# Configuration is in setup.cfg
```

### Type Hints

Use type hints for function signatures:

```python
def scan_file(file_path: str, severity: int = 1) -> dict:
    """Scan a single file for threats."""
    pass
```

### Documentation

- Use docstrings for all public functions and classes
- Follow [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for docstrings

```python
def detect_threat(file_hash: str) -> Optional[Threat]:
    """
    Detect if a file hash matches known threats.
    
    Args:
        file_hash: MD5, SHA1, or SHA256 hash of the file
        
    Returns:
        Threat object if found, None otherwise
        
    Example:
        >>> threat = detect_threat("a1b2c3d4...")
        >>> print(threat.severity)
        'HIGH'
    """
    pass
```

---

## 🧪 Testing Requirements

### Writing Tests

- All new features must include tests
- Aim for >80% code coverage
- Use `pytest` for testing

### Test Structure

```
tests/
├── unit/           # Unit tests for individual functions
├── integration/    # Integration tests for modules
├── fixtures/       # Test data and fixtures
└── conftest.py     # Pytest configuration
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=antivirus --cov-report=html

# Run specific test file
pytest tests/unit/test_scanner.py

# Run with verbose output
pytest -v
```

### Test Example

```python
import pytest
from antivirus.core.scanner import FileScanner

def test_scan_clean_file(tmp_path):
    """Test scanning a clean file."""
    # Create test file
    test_file = tmp_path / "clean.txt"
    test_file.write_text("Hello World")
    
    # Scan file
    scanner = FileScanner()
    result = scanner.scan(str(test_file))
    
    # Assert
    assert result.is_clean is True
    assert result.threats == []
```

---

## 📨 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(scanner): add SHA256 hash detection

Implement SHA256 hash checking in addition to MD5 and SHA1.
This improves detection accuracy and security.

Closes #42

---

fix(cli): handle missing file gracefully

Previously, scanning a non-existent file would crash.
Now it displays a user-friendly error message.

Fixes #38

---

docs(readme): update installation instructions

Add clarification for Windows users about virtual environments.
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update from upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests and linters**
   ```bash
   pytest
   flake8 antivirus/
   black antivirus/
   ```

3. **Update documentation**
   - Update README if needed
   - Add docstrings
   - Update CHANGELOG.md

### Submitting PR

1. **Push to your fork**
   ```bash
   git push origin your-branch-name
   ```

2. **Create Pull Request**
   - Use a clear, descriptive title
   - Reference related issues
   - Describe what changed and why
   - Include screenshots for UI changes
   - List any breaking changes

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Related Issues
   Closes #123
   
   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests added/updated
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented)
   ```

### Review Process

1. **Automated Checks**: CI/CD will run tests and linters
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

---

## 🔒 Security Vulnerabilities

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:

1. Go to [Security Advisories](https://github.com/Blackmvmba88/Antivirus/security/advisories)
2. Click "Report a vulnerability"
3. Provide detailed information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Responsible Disclosure

- We aim to respond within 48 hours
- We'll work with you to understand and fix the issue
- Credit will be given in release notes (if desired)
- We follow a 90-day disclosure timeline

---

## 📚 Additional Resources

- [Architecture Documentation](docs/architecture.md)
- [API Reference](docs/api.md)
- [Roadmap](docs/roadmap.md)
- [FAQ](docs/faq.md)

---

## 🎉 Recognition

Contributors are recognized in:
- README.md credits section
- CHANGELOG.md release notes
- GitHub contributors page

### Levels of Contribution

- **🌱 Contributor**: Made 1+ merged PR
- **🌿 Active Contributor**: Made 5+ merged PRs
- **🌳 Core Contributor**: Made 20+ merged PRs or significant features
- **🏆 Maintainer**: Trusted community member with merge rights

---

## 💬 Questions?

- **GitHub Discussions**: For general questions
- **Issues**: For bug reports and feature requests
- **Discord/Slack**: [Join our community](#) (coming soon)

---

## 📜 License

By contributing to ANTIVIRUS, you agree that your contributions will be licensed under the Apache License 2.0.

---

**Thank you for making ANTIVIRUS better! 🛡️**
