ARG GCR
FROM $GCR/notebook-servers/base:latest

USER root

# args - software versions
ARG MINIFORGE_ARCH="x86_64"
ARG MINIFORGE_VERSION=4.10.1-4
ARG PIP_VERSION=21.1.2
ARG PYTHON_VERSION=3.8.10

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# install -- node.js
RUN : \
  && export DEBIAN_FRONTEND=noninteractive \
  && curl -sL "https://deb.nodesource.com/gpgkey/nodesource.gpg.key" | apt-key add - \
  && echo "deb https://deb.nodesource.com/node_14.x focal main" > /etc/apt/sources.list.d/nodesource.list \
  && apt-get -yq update \
  && apt-get -yq install --no-install-recommends \
      nodejs \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && :

# setup environment for conda
ENV CONDA_DIR /opt/conda
ENV PATH "${CONDA_DIR}/bin:${PATH}"
RUN : \
  && mkdir -p "${CONDA_DIR}" \
  && echo ". /opt/conda/etc/profile.d/conda.sh" >> "${HOME}"/.bashrc \
  && echo ". /opt/conda/etc/profile.d/conda.sh" >> /etc/profile \
  && echo "conda activate base" >> "${HOME}"/.bashrc \
  && echo "conda activate base" >> /etc/profile \
  && chown -R "${NB_USER}:users" "${CONDA_DIR}" \
  && chown -R "${NB_USER}:users" "${HOME}" \
  && echo "NAMESPACE=\$(echo \$NB_PREFIX | awk -F '/' '{print \$3}')" >> /etc/profile \
  && echo "NOTEBOOK_NAME=\$(echo \$NB_PREFIX | awk -F '/' '{print \$4}')" >> /etc/profile \
  && :

# switch to NB_UID for installs
USER ${NB_UID}

# install - conda, pip, python
RUN : \
  && curl -sL "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-${MINIFORGE_ARCH}.sh" -o /tmp/Miniforge3.sh \
  && curl -sL "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-${MINIFORGE_ARCH}.sh.sha256" -o /tmp/Miniforge3.sh.sha256 \
  && echo "$(cat /tmp/Miniforge3.sh.sha256 | awk '{ print $1; }') /tmp/Miniforge3.sh" | sha256sum --check \
  && rm /tmp/Miniforge3.sh.sha256 \
  && /bin/bash /tmp/Miniforge3.sh -b -f -p "${CONDA_DIR}" \
  && rm /tmp/Miniforge3.sh \
  && conda config --system --set auto_update_conda false \
  && conda config --system --set show_channel_urls true \
  && echo "conda ${MINIFORGE_VERSION:0:-2}" >> "${CONDA_DIR}"/conda-meta/pinned \
  && echo "python ${PYTHON_VERSION}" >> "${CONDA_DIR}"/conda-meta/pinned \
  && conda install -y -q \
      python="${PYTHON_VERSION}" \
      conda="${MINIFORGE_VERSION:0:-2}" \
      pip="${PIP_VERSION}" \
  && conda update -y -q --all \
  && conda clean -a -f -y \
  && chown -R "${NB_USER}:users" "${CONDA_DIR}" \
  && chown -R "${NB_USER}:users" "${HOME}" \
  && :

# install - requirements.txt
COPY --chown=jovyan:users requirements.txt /tmp
RUN : \
 && python3 -m pip install -r /tmp/requirements.txt --quiet --no-cache-dir \
 && rm -f /tmp/requirements.txt \
 && jupyter lab --generate-config \
 && rm -rf "${HOME}/.cache/yarn" \
 && chown -R "${NB_USER}:users" "${CONDA_DIR}" \
 && chown -R "${NB_USER}:users" "${HOME}" \
 && :

# override default jupyter lab settings
COPY --chown=jovyan:users overrides.json /opt/conda/share/jupyter/lab/settings/overrides.json

# s6 - copy scripts
COPY --chown=jovyan:users s6/ /etc

# s6 - 01-copy-tmp-home
USER root
RUN : \
 && mkdir -p /tmp_home \
 && cp -r "${HOME}" /tmp_home \
 && chown -R "${NB_USER}:users" /tmp_home \
 && :
USER ${NB_UID}

EXPOSE 8888

ENTRYPOINT ["/init"]
