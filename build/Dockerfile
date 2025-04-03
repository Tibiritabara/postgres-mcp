# Use Python 3.12 slim image as the base
FROM python:3.12-slim

# Add a new non-root user to execute the app
RUN useradd -m server

# Switch to the new user
USER server

# Set the working directory
WORKDIR /server

# Add the user's local bin to the path
ENV PATH="${PATH}:/home/server/.local/bin"
ENV PYTHONPATH="/server/src"

# Copy the pyproject.toml and uv.lock files
COPY --chown=server:server ./pyproject.toml ./uv.lock ./

# Force uv to compile the bytecode
ENV UV_COMPILE_BYTECODE=1

# Install dependencies
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync --frozen --no-cache

# Copy the code to the container
COPY --chown=server:server ./src /server/src

# Command to run the application using the new main.py
CMD ["./.venv/bin/mcp", "run", "src/main.py"]
