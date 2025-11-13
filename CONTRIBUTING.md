# Contributing to Flo

Thank you for your interest in contributing to Flo! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Flo-Lang.git
   cd Flo-Lang
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Running Tests

Run the test suite:

```bash
python3 -m unittest tests/test_flo.py -v
```

### Running Examples

Test the CLI:

```bash
python3 src/flo_cli.py run examples/hello.flo
```

Or use the wrapper script:

```bash
./flo run examples/hello.flo
```

## Project Structure

```
Flo-Lang/
├── src/
│   ├── flo/
│   │   ├── lexer/       # Tokenizer
│   │   ├── parser/      # Parser (AST builder)
│   │   ├── interpreter/ # Interpreter
│   │   └── stdlib/      # Standard library
│   └── flo_cli.py       # CLI tool
├── examples/            # Example programs
├── docs/               # Documentation
├── tests/              # Test suite
└── README.md           # Main documentation
```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Flo version
- Python version

### Suggesting Features

Feature requests are welcome! Please create an issue with:

- Clear description of the feature
- Use cases
- Examples of how it would work
- Why it would be valuable

### Contributing Code

1. **Pick an issue** or create one for your feature
2. **Write code** following our style guidelines
3. **Add tests** for your changes
4. **Update documentation** if needed
5. **Submit a pull request**

## Code Style

### Python Code

- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Flo Code

- Use consistent indentation (4 spaces)
- Write clear, readable code
- Add comments for complex logic
- Follow examples in the `examples/` directory

## Testing

### Writing Tests

Add tests for:

- New features
- Bug fixes
- Edge cases

Test files should be in the `tests/` directory and follow the naming pattern `test_*.py`.

Example test:

```python
def test_new_feature(self):
    code = """
    # Your Flo code here
    x = 10
    x + 5
    """
    result = self.run_code(code)
    self.assertEqual(result, 15)
```

### Running Tests

```bash
# Run all tests
python3 -m unittest discover tests

# Run specific test file
python3 -m unittest tests/test_flo.py

# Run with verbose output
python3 -m unittest tests/test_flo.py -v
```

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use clear, concise language
- Include examples where helpful

### User Documentation

Update documentation when:

- Adding new language features
- Changing existing behavior
- Adding new CLI commands
- Adding standard library modules

Documentation files:

- `README.md` - Main project documentation
- `docs/LANGUAGE_REFERENCE.md` - Language syntax reference
- `docs/GETTING_STARTED.md` - Getting started guide
- Example programs in `examples/`

## Pull Request Process

1. **Create a pull request** with a clear title and description
2. **Link related issues** using keywords like "Fixes #123"
3. **Ensure tests pass** - all existing and new tests should pass
4. **Update documentation** - if your changes affect user-facing features
5. **Keep commits clean** - write clear commit messages
6. **Be responsive** - address review comments promptly

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How did you test your changes?

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] Commit messages are clear
```

## Commit Message Guidelines

Write clear, descriptive commit messages:

```
Add feature: Brief description

Longer explanation of what changed and why.

Fixes #123
```

Examples:
- `Fix: Correct parser handling of nested expressions`
- `Add: Support for async/await syntax`
- `Docs: Update getting started guide`
- `Test: Add tests for list operations`

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and professional
- Provide constructive feedback
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks
- Trolling or insulting comments
- Publishing private information
- Other unprofessional conduct

## Getting Help

If you need help:

- Check the documentation in `docs/`
- Look at examples in `examples/`
- Ask questions in GitHub issues
- Review existing code

## Recognition

Contributors will be recognized in:

- GitHub contributors page
- Future CONTRIBUTORS.md file
- Release notes (for significant contributions)

## License

By contributing to Flo, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Flo! Your efforts help make Flo better for everyone. 🚀
