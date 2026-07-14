# CLAUDE.md

Context and working agreement for AI-assisted development on this project.

## Project overview

FeedbackAI is a full-stack demo application: users submit text and an LLM classifies
sentiment, extracts topics, and generates a summary. Results are persisted in
PostgreSQL and displayed in a small analytics dashboard.

- **Frontend:** React + Vite, TypeScript
- **Backend:** Python 3.12+, FastAPI, Pydantic
- **Database:** PostgreSQL via SQLAlchemy ORM, migrations with Alembic
- **AI:** external LLM API
- **Infra:** AWS (S3 + CloudFront, EC2/Lambda, RDS), Docker for local dev
- **Package management:** `uv` (Python), `npm` (Node)

## Primary goal: learning

This is a portfolio project whose main purpose is for the author to **understand** the
code, not just ship it. Therefore, when generating or modifying code:

1. **Explain before and after.** Briefly state what you are about to build and why,
   then walk through the key parts of the generated code.
2. **Prefer clarity over cleverness.** Choose the readable approach; avoid obscure
   one-liners and premature abstraction.
3. **Comment the non-obvious.** Add short docstrings/comments where they aid
   understanding — not on trivial lines.
4. **Surface decisions.** When there is a meaningful choice (e.g. ORM vs raw SQL,
   sync vs async, EC2 vs Lambda), name the trade-off so it can be defended in an
   interview.
5. **Go one slice at a time.** Implement one vertical feature per change; don't
   scaffold the whole app at once.

## Repository structure

```
backend/    # FastAPI application
frontend/   # React (Vite) application
```

## Language policy

- **All repository artifacts in English:** code, identifiers, comments, docstrings,
  commit messages, README, and other docs.
- **Explanations to the author in chat:** neutral Latin American Spanish.

## Git workflow

- One feature per branch (e.g. `feat/analysis-endpoint`), merged via pull request.
- **Conventional Commits, in English.** Format: `type(scope): summary`.
  - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `perf`.
  - Examples:
    - `feat(api): add POST /analyses endpoint`
    - `fix(db): handle missing session on startup`
    - `chore(deps): pin fastapi version`
- Keep commits small and focused; the summary line stays under ~72 characters.

## Coding conventions

### Backend (Python / FastAPI)

- Type hints on all function signatures; validate I/O with Pydantic models.
- Use `async def` for request handlers that perform I/O.
- Keep a layered structure: routes → services → data access; don't put business
  logic in route handlers.
- Format and lint with Ruff.
- Never hardcode configuration or secrets — read them from environment variables.

### Frontend (React / TypeScript)

- Functional components with hooks only.
- Type props and API responses explicitly; avoid `any`.
- Keep components small and single-purpose; lift shared state deliberately.
- Format with Prettier, lint with ESLint.

## Testing

- Backend: `pytest`. Frontend: React Testing Library.
- Add at least one test alongside each new feature before opening a PR.

## Security

- **Never commit secrets.** `.env` is git-ignored; document required variables in
  `.env.example` (values omitted).
- Access secrets in production via a managed store (AWS Secrets Manager / SSM),
  never in source.
- Configure CORS explicitly; do not use a wildcard origin in production.