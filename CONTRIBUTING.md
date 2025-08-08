# Contributing to WebUtils

First off, thank you for considering contributing to WebUtils! We appreciate your time and effort in helping us improve this project.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

1. **Check for existing issues** - Before creating a new issue, please search the [issue tracker](https://github.com/louisgoodnews/WebUtils/issues) to see if the problem has already been reported.

2. **Create a detailed bug report** - If you're reporting a bug, please include:
   - A clear, descriptive title
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Python version and operating system
   - Any relevant error messages or logs

### Suggesting Enhancements

1. **Check existing feature requests** - Search the issues to see if your enhancement has already been suggested.

2. **Create a feature request** - If you have an idea for a new feature:
   - Describe the feature and why it would be useful
   - Include any relevant use cases
   - If possible, provide a proposed API or implementation approach

### Your First Code Contribution

1. **Set up your development environment**
   ```bash
   # Fork and clone the repository
   git clone https://github.com/your-username/WebUtils.git
   cd WebUtils
   
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   
   # Install development dependencies
   pip install -e .[dev]
   pre-commit install
   ```

2. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number-description
   ```

3. **Make your changes** - Follow the coding standards below

4. **Run tests**
   ```bash
   pytest
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Type: Short description of changes"
   ```

   Commit message format:
   ```
   Type: Short description
   
   More detailed description if needed.
   
   Closes #issue-number
   ```
   
   Types:
   - `Feat`: New feature
   - `Fix`: Bug fix
   - `Docs`: Documentation changes
   - `Style`: Code style changes
   - `Refactor`: Code changes that neither fix a bug nor add a feature
   - `Test`: Adding missing tests or correcting existing tests
   - `Chore`: Changes to the build process or auxiliary tools

6. **Push your changes**
   ```bash
   git push origin your-branch-name
   ```

7. **Create a Pull Request** - Open a PR against the `main` branch

## Coding Standards

### Python Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function signatures
- Keep functions small and focused on a single responsibility
- Write docstrings following [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

### Code Formatting
- Use `black` for code formatting
- Use `isort` for import sorting
- Maximum line length: 88 characters

### Testing
- Write tests for all new features and bug fixes
- Aim for good test coverage
- Place tests in the `tests/` directory
- Test files should mirror the package structure

## Code Review Process

1. A maintainer will review your PR and provide feedback
2. Address any review comments and push your changes
3. Once approved, your PR will be merged into the main branch
4. Your contribution will be included in the next release

## Need Help?

If you have any questions about contributing, please open an issue or contact [@louisgoodnews](https://github.com/louisgoodnews).

Thank you for contributing to WebUtils! 🎉
