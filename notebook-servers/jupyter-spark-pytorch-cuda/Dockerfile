ARG GCR
FROM $GCR/notebook-servers/jupyter-spark:latest

# nvidia configs
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

COPY --chown=jovyan:users requirements.txt /tmp/requirements.txt
RUN : \
  && python3 -m pip install -r /tmp/requirements.txt --quiet --no-cache-dir \
  && rm -f /tmp/requirements.txt \
  && :
