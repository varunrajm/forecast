# Contributing to Forecasta

Thanks for your interest in contributing! This document explains how to set up
the project locally, run the test suite, and submit changes.

## Development Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # macOS / Linux
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Running Tests

### Backend

```bash
cd backend
python -m unittest discover
```

### Frontend

```bash
cd frontend
npm run lint
npm run build
```

## Code Style

- **Python:** Follow PEP 8. Use type hints where reasonable.
- **TypeScript:** Follow the existing `eslint.config.mjs` rules. Avoid `any`.
- Keep functions small and focused. Add docstrings for non-obvious logic.
- Match the surrounding code's comment density and naming.

## Pull Request Process

1. Fork the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes in small, focused commits.
3. Ensure all tests pass and the linter is clean.
4. Update the README or docs if your change affects setup or usage.
5. Open a pull request with a clear description of what changed and why.

## Reporting Bugs

Open a GitHub issue and include:

- Steps to reproduce
- Expected vs. actual behaviour
- Backend / frontend logs
- Python and Node versions

## Feature Requests

Open a GitHub issue describing the problem you want to solve and the proposed
approach. Larger changes are best discussed before implementation.
