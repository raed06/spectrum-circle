# Contributing to SpectrumCircle

First off, thank you for your interest in contributing to SpectrumCircle! 💙  
This project exists to support the autism and neurodiversity community, and every contribution matters.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Before You Start](#before-you-start)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Contribution Principles](#contribution-principles)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).  
Please read it before contributing.

---

## Before You Start

> **Important**: SpectrumCircle follows an *issue-first* policy.  
> **Do not open a Pull Request without a linked issue that has been approved first.**

This helps avoid duplicated work and ensures every contribution aligns with the project's direction.

---

## How to Contribute

### Reporting Bugs

If you found a bug, please [open a Bug Report issue](../../issues/new?template=bug_report.md) and include:

- A clear and descriptive title
- Steps to reproduce the problem
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or screenshots if available

### Suggesting Features

Have an idea? [Open a Feature Request issue](../../issues/new?template=feature_request.md) and describe:

- What problem does this solve?
- How would it work?
- Why does it align with SpectrumCircle's mission?

Wait for maintainer feedback before starting any implementation.

### Contributing Code

1. **Open or find an issue** — check [open issues](../../issues) first to avoid duplicates.
2. **Comment on the issue** to let the maintainer know you'd like to work on it.
3. **Wait for approval** — a maintainer will assign the issue to you and give a green light.
4. **Fork and implement** — once approved, fork the repo and start coding.
5. **Open a Pull Request** — link it to the issue using `Closes #<issue-number>`.

---

## Development Setup

```bash
# 1. Fork the repository and clone your fork
git clone https://github.com/<your-username>/spectrum-circle.git
cd spectrum-circle

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Fill in your API keys in .env

# 5. Start the database (requires Docker)
cd docker/postgres && docker-compose up -d && cd ../..

# 6. Run the tests to verify your setup
pytest tests/ -v
```

---

## Pull Request Guidelines

- **One PR per issue** — keep changes focused and atomic.
- **Link the issue** — include `Closes #<issue-number>` in the PR description.
- **Write tests** — any new feature or bug fix should include relevant tests.
- **Follow existing code style** — consistent formatting, clear variable names, docstrings where appropriate.
- **Update the README** if your change affects setup, usage, or architecture.
- **Do not break existing tests** — all CI checks must pass before review.

### Branch Naming

Use descriptive branch names following this pattern:

```
feature/<short-description>     # New features
fix/<short-description>         # Bug fixes
docs/<short-description>        # Documentation only
refactor/<short-description>    # Code refactoring
```

---

## Contribution Principles

Because SpectrumCircle serves the autism and neurodiversity community, all contributions must:

- Use **neurodiversity-affirming language** — avoid deficit-based framing.
- Respect **user privacy and data protection** — this app handles sensitive personal information.
- Prioritize **safety** — never weaken crisis detection or intervention logic.
- Be **accessible** — consider users with different sensory and cognitive profiles.

If you're unsure whether something aligns with these principles, open an issue and ask first. There are no bad questions here.

---

Thank you for helping make SpectrumCircle better for everyone. 💙
