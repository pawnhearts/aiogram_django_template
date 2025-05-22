FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
ENV UV_LINK_MODE=copy

RUN apt-get update && \
    apt-get install -y gettext postgresql-client-15 libpq-dev wait-for-it libmagic1  && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/* && rm -rf /tmp/*

# Change the working directory to the `app` directory
WORKDIR /app

ADD . /app

RUN uv sync --frozen --no-install-project

# Install dependencies
#RUN --mount=type=cache,target=/root/.cache/uv \
#    --mount=type=bind,source=uv.lock,target=uv.lock \
#    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#    uv sync --frozen --no-install-project
#
# Copy the project into the image
#ADD . /app

# Sync the project
#RUN --mount=type=cache,target=/root/.cache/uv \
#    uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/entrypoint.sh"]
