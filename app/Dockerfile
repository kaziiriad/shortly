
FROM python:3.13.0-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /uvx /bin/

# Create a working directory
WORKDIR /app
# Copy the requirements file
COPY uv.lock pyproject.toml /app/

# Install the dependencies
RUN uv sync

ENV PYTHONPATH="/app"

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
# RUN chown -R "$USER":"$USER" $APP_DIR

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
