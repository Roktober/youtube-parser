FROM python:3.9.5-slim-buster as common-deps
LABEL Description="Yotube parser" Author="Roktober"

RUN groupadd --system youtube_parser && useradd --no-log-init --shell /bin/false --system --gid youtube_parser youtube_parser

ENV TZ='Europe/Moscow'

ENV APP_DIR=/app

WORKDIR ${APP_DIR}

COPY requirements.in ${APP_DIR}/requirements.txt
RUN pip install --no-cache-dir -r ${APP_DIR}/requirements.txt

FROM common-deps as dev

COPY ./requirements-dev.txt ${APP_DIR}/requirements-dev.txt
RUN pip install --no-cache-dir -r ${APP_DIR}/requirements-dev.txt

COPY ./mypy.ini ./mypy.ini
COPY ./youtube_parser ./youtube_parser

# -------------------- unit tests and linters --------------------
FROM dev as dev-unittested

RUN mypy ${APP_DIR}/youtube_parser

# -------------------- final image --------------------
FROM common-deps as final

COPY --from=dev-unittested ${APP_DIR}/youtube_parser ./youtube_parser

USER youtube_parser

CMD python -m youtube_parser
