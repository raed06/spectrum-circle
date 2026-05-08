# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅ Yes     |

---

## Reporting a Vulnerability

SpectrumCircle handles sensitive data from neurodivergent individuals and their
families. We take security issues extremely seriously.

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead, report them privately by:

1. Going to the **[Security tab](https://github.com/raed06/spectrum-circle/security/advisories/new)**
   in this repository and opening a private advisory.
2. Or contacting the maintainer directly via GitHub: [@raed06](https://github.com/raed06)

### What to include in your report

- A clear description of the vulnerability
- Steps to reproduce it
- Potential impact (what data or functionality is affected)
- Your suggested fix, if any

---

## What Happens After You Report

1. You will receive an acknowledgment within **72 hours**
2. We will investigate and keep you updated on progress
3. Once fixed, we will credit you in the release notes (unless you prefer to stay anonymous)

---

## Areas of Special Concern

Given the nature of this project, we are especially vigilant about:

- **User data privacy** — conversation history, sensory profiles, and personal routines
- **Crisis detection integrity** — any bypass or weakening of safety logic is critical
- **Prompt injection** — attacks that could alter the AI's safe messaging behavior
- **Authentication and authorization** — unauthorized access to user profiles or sessions

---

## Data Handling Disclaimer

SpectrumCircle stores conversation history and user profiles in a PostgreSQL database.
Deployers are responsible for securing their own infrastructure, encrypting data at rest,
and complying with applicable data protection regulations (e.g., GDPR, HIPAA where relevant).

The project maintainer is not liable for data breaches resulting from misconfigured
deployments. Always follow the setup guidelines in the README and never expose your
`.env` file or database credentials publicly.
