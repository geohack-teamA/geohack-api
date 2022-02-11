# For development
# FROM python:3.9-slim as dev
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# EXPOSE 8000

# RUN apt-get update && \
#     apt-get install -y --no-install-recommends netcat && \
#     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# # copy poetry file
# COPY poetry.lock pyproject.toml ./

# # install packages
# RUN pip install poetry && \
#   poetry config virtualenvs.in-project true && \
#   poetry install --no-dev

# COPY . ./

# CMD poetry run uvicorn --host=0.0.0.0 app.main:app
# if migration is needed
# CMD poetry run alembic upgrade head && \
#     poetry run uvicorn --host=0.0.0.0 app.main:app

# For build
FROM python:3.9-slim as build

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry export -f requirements.txt > requirements.txt

# For production
FROM python:3.9-slim as prod

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=build /app/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . .

ARG PORT=80
ENV PORT=$PORT
EXPOSE $PORT

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
