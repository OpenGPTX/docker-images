ARG java_image_tag=11-jre-slim

FROM openjdk:${java_image_tag}

ARG spark_uid=185
ARG SPARK_VERSION=3.2.1
ARG HADOOP_VERSION=3.2
ARG DELTA_LAKE_VERSION=1.2.0
ARG SPARKNLP_VERSION=4.0.2
ENV SPARK_HOME /opt/spark

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN : \
  && set -ex \
  && sed -i 's/http:\/\/deb.\(.*\)/https:\/\/deb.\1/g' /etc/apt/sources.list \
  && apt-get update \
  && ln -s /lib /lib64 \
  && apt-get install -y bash tini libc6 libpam-modules krb5-user libnss3 procps curl \
  && mkdir -p /opt/spark \
  && mkdir -p /opt/spark/examples \
  && mkdir -p /opt/spark/work-dir \
  && touch /opt/spark/RELEASE \
  && echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su \
  && chgrp root /etc/passwd && chmod ug+rw /etc/passwd \
  && rm -rf /var/cache/apt/* \
  && :

RUN : \
  && set -x \
  && curl -sL "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" -o /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
  && tar -xzf /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /tmp/ \
  && rm /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
  && mkdir -p /opt/spark/ \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars /opt/spark/jars \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin /opt/spark/bin \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/sbin /opt/spark/sbin \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/kubernetes/dockerfiles/spark/entrypoint.sh /opt/ \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/kubernetes/dockerfiles/spark/decom.sh /opt/ \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/examples /opt/spark/ \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/kubernetes/tests /opt/spark/tests \
  && cp -r /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/data /opt/spark/data \
  && rm -rf /tmp/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} \
  && curl -sL "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar" -o /opt/spark/jars/hadoop-aws-3.3.1.jar \
  && curl -sL "https://repo1.maven.org/maven2/io/delta/delta-core_2.12/${DELTA_LAKE_VERSION}/delta-core_2.12-${DELTA_LAKE_VERSION}.jar" -o /opt/spark/jars/delta-core_2.12-${DELTA_LAKE_VERSION}.jar \
  && curl -sL "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar" -o /opt/spark/jars/aws-java-sdk-bundle-1.11.901.jar \
  # use sparknlp fat jars as it comes with all dependencies pre-installed
  && curl -sL "https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/jars/spark-nlp-assembly-${SPARKNLP_VERSION}.jar" -o /opt/spark/jars/spark-nlp_2.12-${SPARKNLP_VERSION}.jar \
  && curl -sL "https://repo1.maven.org/maven2/org/apache/spark/spark-hadoop-cloud_2.13/3.2.1/spark-hadoop-cloud_2.13-3.2.1.jar" -o /opt/spark/jars/spark-hadoop-cloud_2.13-3.2.1.jar \
  && curl -sL "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-client-core/3.2.1/hadoop-mapreduce-client-core-3.2.1.jar" -o /opt/spark/jars/hadoop-mapreduce-client-core-3.2.1.jar \
  && :

WORKDIR /opt/spark/work-dir
RUN chmod g+w /opt/spark/work-dir \
    && chmod a+x /opt/decom.sh

ENTRYPOINT [ "/opt/entrypoint.sh" ]

# Specify the User that the actual main process will run as
USER "${spark_uid}"
