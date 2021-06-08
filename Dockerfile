FROM python:3.8-slim

RUN groupmod -g 1000 users \
    && useradd -u 911 -U -d /home/viaduct -s /bin/false viaduct \
    && usermod -G users viaduct \
    && mkdir -p /home/viaduct \
    && chown viaduct:users /home/viaduct


RUN pip install poetry && poetry config virtualenvs.create false

RUN mkdir /home/viaduct/app && chown viaduct:users /home/viaduct/app
WORKDIR /home/viaduct/app

COPY poetry.lock pyproject.toml ./

RUN poetry install
RUN poetry add freezegun

COPY --chown=viaduct . .

USER viaduct
ENV PYTHONPATH=/home/viaduct/app
