ARG GCR
FROM $GCR/spark/base:latest

WORKDIR /

ARG MINIFORGE_ARCH="x86_64"
ARG MINIFORGE_VERSION=4.10.1-4
ARG PIP_VERSION=21.1.2
ARG PYTHON_VERSION=3.8.10
ARG SPARK_VERSION=3.2.1
ARG HADOOP_VERSION=3.2
ARG DELTA_LAKE_VERSION=1.2.0

ENV CONDA_DIR /opt/conda
ENV PATH "${CONDA_DIR}/bin:${PATH}"

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Reset to root to run installation tasks
USER 0

RUN : \
  && apt-get update \
  && apt-get install curl -y \
  # Removed the .cache to save space
  && rm -rf /root/.cache && rm -rf /var/cache/apt/* \
  && :

# setup environment for conda
ENV CONDA_DIR /opt/conda
ENV PATH "${CONDA_DIR}/bin:${PATH}"
RUN : \
  && mkdir -p "${CONDA_DIR}" \
  && echo ". /opt/conda/etc/profile.d/conda.sh" >> ${HOME}/.bashrc \
  && echo ". /opt/conda/etc/profile.d/conda.sh" >> /etc/profile \
  && echo "conda activate base" >> ${HOME}/.bashrc \
  && echo "conda activate base" >> /etc/profile \
  && :

# install - conda, pip, python
RUN : \
  && set -x \
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
    python=${PYTHON_VERSION} \
    conda=${MINIFORGE_VERSION:0:-2} \
    pip=${PIP_VERSION} \
  && conda update -y -q --all \
  && conda clean -a -f -y \
  && :

# download spark from archive and setup pyspark
RUN : \
  && set -x \
  && mkdir ${SPARK_HOME}/python \
  && curl -sL "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" -o /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
  && tar -xzf /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /tmp/ \
  && rm /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
  && mkdir -p ${SPARK_HOME}/python/ \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/python/pyspark ${SPARK_HOME}/python/pyspark \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/python/lib ${SPARK_HOME}/python/lib \
  && rm -rf /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} \
  && :

COPY delta-lake-examples ${SPARK_HOME}/examples

#Fix "ModuleNotFoundError: No module named 'pyspark'"
ENV PYTHONPATH ${SPARK_HOME}/python:${SPARK_HOME}/python/lib:$PYTHONPATH

#FIX "Exception in thread "main" java.io.FileNotFoundException: /opt/spark/.ivy2/cache/resolved-org.apache.spark-spark-submit-parent-2b634464-81ff-4034-a0e8-99b0a983f8ad-1.0.xml (No such file or directory)"
RUN mkdir /opt/spark/.ivy2 \
    && chmod g+w /opt/spark/.ivy2 \
    && chmod a+x /opt/spark/.ivy2

WORKDIR /opt/spark/work-dir
ENTRYPOINT [ "/opt/entrypoint.sh" ]

#Fix "ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied: '/.local'" when pip install delta-spark
RUN mkdir /.local \
    && chmod g+w /.local \
    && chmod a+x /.local

# Specify the User that the actual main process will run as
ARG spark_uid=185

# Let non-root user install pip packages
RUN :\
  && chown ${spark_uid}:${spark_uid} -R /opt/spark/python \
  && chown -R ${spark_uid}:${spark_uid} "${CONDA_DIR}" \
  && chown -R ${spark_uid}:${spark_uid} ${HOME} \
  && :

USER ${spark_uid}

# Install delta-spark as non-root
RUN pip install delta-spark==${DELTA_LAKE_VERSION}  --no-cache-dir -t /opt/spark/python/

COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir -t /opt/spark/python/
