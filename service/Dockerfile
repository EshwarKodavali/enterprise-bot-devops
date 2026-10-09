FROM python:3.12.11-slim-bookworm AS builder

WORKDIR /build
COPY app.py .
RUN python -m py_compile app.py

FROM python:3.12.11-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_NAME=demo-service \
    VERSION=1.0.0

WORKDIR /app

RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --home-dir /app appuser

COPY --from=builder --chown=appuser:appgroup /build/app.py /app/app.py

USER appuser:appgroup

EXPOSE 8080

CMD ["python", "-B", "app.py"]
