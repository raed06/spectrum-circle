# Changelog

All notable changes to SpectrumCircle will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]
<!-- Changes that are being worked on but not yet released go here -->

---

## [1.0.0] - 2026-05-07

### Added
- 🤖 AI-powered conversational support system for the autism and neurodiversity community
- 🧠 Multi-agent architecture with specialized MCP servers:
  - `autism_support_mcp` — general support and psychoeducation
  - `crisis_mcp` — real-time crisis detection and intervention
  - `calendar_mcp` — routine and schedule management
  - `sensory_mcp` — sensory profile tracking and recommendations
  - `social_mcp` — social skills coaching and support
- 🚨 Crisis detection system with automatic escalation and safe messaging protocols
- 📅 Personalized routine management adapted to neurodivergent needs
- 🌡️ Sensory sensitivity tracking with environment recommendations
- 💬 Social skills coaching with context-aware guidance
- 🗄️ PostgreSQL database with full conversation history and user profiles
- 📊 Langfuse integration for LLM observability and tracing
- 🐳 Docker support for local development (PostgreSQL + Langfuse)
- 🧪 Test suite covering core agent logic and crisis detection
- 📖 Full API documentation via FastAPI auto-generated Swagger UI (`/docs`)
- 📹 Demo video showcasing key features

### Technical Stack
- **Backend**: FastAPI + Python 3.11
- **AI**: OpenAI GPT models + Anthropic Claude (fine-tuned variants)
- **Agent framework**: MCP (Model Context Protocol)
- **Database**: PostgreSQL 15
- **Observability**: Langfuse
- **Testing**: pytest

---

## How to Read This Changelog

Each version uses these categories:

| Category | Meaning |
|----------|---------|
| `Added` | New features |
| `Changed` | Changes to existing functionality |
| `Deprecated` | Features that will be removed soon |
| `Removed` | Features that were removed |
| `Fixed` | Bug fixes |
| `Security` | Security vulnerability fixes |

---

[Unreleased]: https://github.com/raed06/spectrum-circle/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/raed06/spectrum-circle/releases/tag/v1.0.0
