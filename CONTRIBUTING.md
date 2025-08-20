# Contributing to Peady

Thank you for your interest in contributing to Peady! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork the Repository

Fork the project repository and clone your fork:

```bash
git clone https://github.com/your-username/peady.git
cd peady
```

### 2. Set up Development Environment

Run the development setup script:

```bash
chmod +x setup_dev.sh
./setup_dev.sh
```

Or manually:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python manage.py migrate
python manage.py createsuperuser
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes

- Write clean, readable code
- Follow Django and Python best practices
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes

```bash
python manage.py test
```

### 6. Commit Your Changes

Use clear and descriptive commit messages:

```bash
git add .
git commit -m "Add feature: description of your changes"
```

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use Django best practices
- Write clear, self-documenting code
- Add docstrings to functions and classes

### Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Aim for good test coverage

### Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Update API documentation for new endpoints

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: OS, Python version, Django version
6. **Error Messages**: Any relevant error messages or logs

## 💡 Feature Requests

When suggesting features:

1. **Description**: Clear description of the feature
2. **Use Case**: Why this feature would be useful
3. **Implementation Ideas**: Any thoughts on implementation

## 📝 Pull Request Guidelines

- Keep PRs focused on a single feature/fix
- Write clear PR descriptions
- Reference related issues
- Ensure tests pass
- Update documentation if needed

## 🏗️ Project Structure

```
peady/
├── api/                 # Main API routing
├── users/              # User management
├── pet/                # Pet models and views
├── order/              # Cart and order management
├── payment/            # Payment processing
└── peady/              # Django settings
```

## 📞 Questions?

If you have questions, feel free to:

- Open an issue on GitHub
- Contact the maintainers
- Join our community discussions

Thank you for contributing to Peady! 🐾