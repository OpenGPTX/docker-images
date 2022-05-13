ARG GCR
FROM $GCR/notebook-servers/jupyter:latest

# install - requirements.txt
COPY --chown=jovyan:users requirements.txt /tmp/requirements.txt
RUN : \
  && python3 -m pip install -r /tmp/requirements.txt --quiet --no-cache-dir \
  && rm -f /tmp/requirements.txt \
  && :

USER root
RUN apt-get update && apt-get install default-jdk -y

# set up an ipython profile and add extension to it
# since ipython profile is not available until jupyterlab is started
ENV IPYTHONDIR /opt/.ipython
RUN : \
 && ipython profile create --ipython-dir="$IPYTHONDIR" \
 && echo "c.InteractiveShellApp.extensions.append('sparkmonitor.kernelextension')" \
    >> "$IPYTHONDIR"/profile_default/ipython_kernel_config.py \
 && chown -R jovyan:users "$IPYTHONDIR" \
 && :

COPY --chown=jovyan:users conf /opt/spark/conf
ENV SPARK_CONF_DIR /opt/spark/conf

USER "${NB_UID}"
