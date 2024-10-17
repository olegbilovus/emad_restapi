FROM python:3.12-slim AS install-dependencies

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends build-essential gcc && \
    apt-get clean && \
    python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.12-slim

COPY --from=install-dependencies /opt/venv /opt/venv

WORKDIR /app

COPY ./app .

ENV PATH="/opt/venv/bin:$PATH"
CMD ["fastapi", "run", "main.py", "--port", "80"]