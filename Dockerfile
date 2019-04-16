FROM bearstech/python-dev:3 as build

COPY requirements.txt /usr/src/
RUN python3 -m venv /opt/issuer/venv \
        && /opt/issuer/venv/bin/pip install -U pip wheel \
        && /opt/issuer/venv/bin/pip install -r /usr/src/requirements.txt

FROM bearstech/python:3

ARG uid=1001
RUN useradd issuer --uid ${uid} --shell /bin/bash

COPY --from=build /opt/issuer /opt/issuer
COPY *.py /opt/issuer/

EXPOSE 5000
USER issuer

CMD ["/opt/issuer/bin/python", "/opt/issuer/issuer.py"]

