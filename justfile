# ──────────────────────────────────────────────────────────────────────
#  myapp — project control plane
#  Run `just --list` for a quick overview of available commands.
# ──────────────────────────────────────────────────────────────────────

set dotenv-load := false

# Default recipe shown when you run `just` with no arguments
default:
    @just --list

# ── Onboarding ────────────────────────────────────────────────────────

# Bootstrap the project: install deps, create data dirs, run doctor
init:
    uv sync --all-extras
    mkdir -p data/json data/db
    uv run pre-commit install
    @just doctor

# Sync dependencies from lockfile
sync:
    uv sync --all-extras

# Verify environment health
doctor:
    uv run project doctor

# ── Development ───────────────────────────────────────────────────────

# Format code
fmt:
    uv run ruff format src/

# Lint code
lint:
    uv run ruff check src/

# Lint and auto-fix
lint-fix:
    uv run ruff check --fix src/

# Type-check code
typecheck:
    uv run mypy src/myapp/

# Run tests
test *ARGS:
    uv run pytest {{ARGS}}

# Run tests with coverage
cov:
    uv run pytest --cov=myapp --cov-report=term-missing

# Run all quality checks (fmt check + lint + typecheck + tests)
check:
    uv run ruff format --check src/
    uv run ruff check src/
    uv run mypy src/myapp/
    uv run pytest

# Run pre-commit hooks on all files
pre-commit:
    uv run pre-commit run --all-files

# ── Run ───────────────────────────────────────────────────────────────

# Run the default service
run:
    uv run project run

# Run a CLI command (pass any args)
cli *ARGS:
    uv run project {{ARGS}}

# Run Streamlit UI
ui:
    uv run streamlit run ui/streamlit_app.py

# ── Build & Release ──────────────────────────────────────────────────

# Build wheel + sdist
build:
    uv build

# Publish to PyPI (configure credentials first)
publish:
    uv publish

# Build Docker image
docker-build:
    docker build -t myapp:latest .

# Run Docker container
docker-run:
    docker run --rm -it myapp:latest

# ── Docs ──────────────────────────────────────────────────────────────

# Serve docs locally (requires mkdocs in dev deps)
docs-serve:
    @echo "Docs are in docs/ — open docs/quickstart.md to get started"

# Build static docs
docs-build:
    @echo "Docs are in docs/ — static markdown, no build needed"

# ── Service patterns ─────────────────────────────────────────────────
# To add commands for a new service, copy one of the patterns below
# and replace "example" with your service name.

# Run example service
svc-example-run:
    uv run project svc example list

# Test example service
svc-example-test:
    uv run pytest src/myapp/services/example/tests/

# Show example service schema
svc-example-schema:
    uv run project svc example schema
