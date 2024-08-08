FROM python:3.12.4-bullseye AS base

LABEL maintainer="Shahan <shahan.khaan@gmail.com>"
LABEL description="This is a python test project for candidates registry based on fastapi framework"

RUN apt-get update --fix-missing \
  && apt-get install -y --no-install-recommends curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

EXPOSE 7000

WORKDIR /code

RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./pyproject.toml
RUN poetry install --only main --no-root --no-cache

HEALTHCHECK --retries=5 --timeout=5s CMD curl -f localhost:7000/healthcheck || exit 1

COPY ./docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

### dev stage
FROM base AS dev
ENV ENVIRONMENT=development
ENV CHOKIDAR_USEPOLLING=true
ENV PATH=/code/.venv/bin:$PATH
RUN poetry install --no-cache
COPY . .
ARG BUILD_FLAG
RUN if [ "$BUILD_FLAG" = "y" ]; then poetry build --format sdist; \
    else echo "Skipping build step as per build argument"; \
    fi

### production stage
FROM base AS source
COPY . .
COPY --from=dev /code/dist/*.tar.gz ./
RUN pip install /code/*.tar.gz

FROM source AS prod
CMD ["poetry", "run", "uvicorn", "--host 0.0.0.0", "--port 7000", "main:app"]
