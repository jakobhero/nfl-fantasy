FROM python:3.14-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /uvx /bin/

WORKDIR /workspace

# install the dependencies first so that editing the scripts does not invalidate
# the layer that resolves them
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked

COPY . .
