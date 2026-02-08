# myapp

A fork-ready, microservice-friendly Python template.

Clone, init, test, run — then extend with your own services.

## Quickstart

```bash
just init       # install deps, create data dirs, setup pre-commit hooks
just test       # run all tests
just run        # run the default service
```

Requires [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just). See `just doctor` for environment checks.

**First time setup:**
- `just init` automatically installs pre-commit hooks that format your code before every commit
- This prevents CI failures due to formatting issues

## What You Get

- **uv-native** workflows — `pyproject.toml` as single source of truth, `uv.lock` committed
- **Microservice architecture** — each service in `src/myapp/services/` with clear boundaries
- **Typed schemas** — Pydantic models at every boundary, versioned with `schema_version`
- **Dual persistence** — JSON (atomic file writes) + SQLite (WAL mode), independent by design
- **CLI** — Click-based, auto-discovers service commands (`project svc <name> <cmd>`)
- **Optional Streamlit UI** — wraps the same service APIs as the CLI
- **Quality gates** — ruff, mypy, pytest, all runnable via `just check`
- **CI** — GitHub Actions running the same gates with uv

## Project Structure

```
src/myapp/
├── cli/              # top-level CLI entrypoint
├── shared/           # config, logging, base schemas, persistence
│   └── persistence/  # BaseStore, JsonStore, SqliteStore
└── services/
    └── example/      # example service (copy to create new ones)
        ├── api.py        # public interface
        ├── schemas.py    # I/O models
        ├── cli.py        # service CLI commands
        ├── storage/      # JSON + SQLite adapters
        └── tests/        # service tests
ui/                   # optional Streamlit app
data/                 # runtime data (gitignored contents)
docs/                 # guides and reference
```

## Commands

```bash
just --list           # see all available commands
just init             # bootstrap project
just doctor           # verify environment
just fmt              # format code
just lint             # lint code
just typecheck        # run mypy
just test             # run pytest
just check            # all quality gates
just run              # run default service
just cli <args>       # run any CLI command
just ui               # launch Streamlit
```

## Documentation

| Guide | Description |
|-------|-------------|
| [Quickstart](docs/quickstart.md) | Get running in 3 commands |
| [Architecture](docs/architecture.md) | Services, boundaries, data flow |
| [CLI Reference](docs/cli-reference.md) | All commands and options |
| [Persistence](docs/persistence.md) | JSON vs SQLite, no-sync explained |
| [Extending](docs/extending.md) | Add services, commands, schemas, UI pages |

## Adding a New Service

```bash
mkdir -p src/myapp/services/myservice/{storage,tests}
# Copy and adapt from services/example/
# The CLI auto-discovers it — no registration needed
project svc myservice --help
```

See [Extending](docs/extending.md) for the full walkthrough.

## License

MIT
