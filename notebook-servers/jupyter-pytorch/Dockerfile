ARG GCR
FROM $GCR/notebook-servers/jupyter:latest

COPY --chown=jovyan:users requirements.txt /tmp/requirements.txt
RUN : \
  && python3 -m pip install -r /tmp/requirements.txt --quiet --no-cache-dir \
  && rm -f /tmp/requirements.txt \
  && :
