ARG GCR
FROM $GCR/notebook-servers/base:latest
USER root

# args - software versions
ARG CODESERVER_VERSION=v4.5.1

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# install - code-server
RUN : \
  && curl -sL "https://github.com/cdr/code-server/releases/download/${CODESERVER_VERSION}/code-server_${CODESERVER_VERSION/v/}_amd64.deb" -o /tmp/code-server.deb \
  && dpkg -i /tmp/code-server.deb \
  && rm -f /tmp/code-server.deb \
  && :

# s6 - copy scripts
COPY --chown=jovyan:users s6/ /etc

# s6 - 01-copy-tmp-home
RUN : \
  && mkdir -p /tmp_home \
  && cp -r "${HOME}" /tmp_home \
  && chown -R "${NB_USER}:users" /tmp_home \
  && :
USER ${NB_UID}

EXPOSE 8888

ENTRYPOINT ["/init"]
