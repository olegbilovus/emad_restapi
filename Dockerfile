FROM python:3.12-slim AS install-dependencies

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends build-essential gcc && \
    apt-get clean && \
    python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.12-slim

RUN useradd -m app && \
    apt-get update &&  \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean

USER app

COPY --from=install-dependencies /opt/venv /opt/venv

WORKDIR /app

COPY ./app .

HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -s --fail http://127.0.0.1:8080/health || exit 1

ENV PATH="/opt/venv/bin:$PATH"
CMD ["fastapi", "run", "main.py", "--port", "8080"]