# Spark Delta Lake Image

## Goal

This repo is used to make build process of Spark Docker image transparent,
easy to understand, and automated.
It also adds delta-lake and S3 dependencies.
This README.md is used to document all changes in order to reuse it in later
spark versions (with every Spark version we need to start from scratch).

All of the necessary dependencies are downloaded within layers of the
dockerfile, while this repo / folder is kept small.

## Foundation

The image is based on the official redistributables from Spark:
<https://spark.apache.org/downloads.html> for the respective version.

We make use of their official Docker images:

1. Base image - `spark-3.2.1-bin-hadoop3.2/kubernetes/dockerfiles/spark`
2. Pyspark image - `spark-3.2.1-bin-hadoop3.2/kubernetes/dockerfiles/spark/bindings/python`

The original Dockerfiles assume all the resources are locally available.
We replace them with a download operation followed by placement on the correct path.

## Extra .jar files

It is better to include the necessary .jars to avoid downloading it while execution.

```bash
#https://mvnrepository.com/artifact/io.delta/delta-core_2.12/1.2.0
wget -P spark-3.2.1-bin-hadoop3.3.1/jars/ https://repo1.maven.org/maven2/io/delta/delta-core_2.12/1.2.0/delta-core_2.12-1.2.0.jar

#https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws/3.3.1
wget -P spark-3.2.1-bin-hadoop3.3.1/jars/ https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar

#https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-bundle/1.11.901
wget -P spark-3.2.1-bin-hadoop3.3.1/jars/ https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar
```

Those are needed for delta-lake + S3.

Feel free to add more useful .jars!

## Extra changes in Dockerfile

All changes are documented with comments: `spark/python/Dockerfile`.
In general makes it easier to use the Sparkimage.

## Extra pip packages

Additional pip images can be installed also within the Dockerfile: `spark/python/Dockerfile`.
Keep in mind to add the `pip install` below `USER ${spark_uid}`.
Otherwise it is installed as root and the app cannot find the dependencies
when it executues.

## How to build Dockerimage

Basically it creates a baseimage with spark which is used to create the
second image based on python.
Please use the automated CI/CD pipleine to build the image.

## How can I extend and use that for my needs?

- extend the Dockerfile
  - add your .jar files
  - add your pip packages

## Extra .py examples

We added some examples how to use spark delta lake:

- python/delta-lake-examples/databricksBenchmark.py
- python/delta-lake-examples/databricksBenchmarkS3.py
- python/delta-lake-examples/sparkdeltalake.py
- python/delta-lake-examples/sparkdeltalakes3.py
- python/delta-lake-examples/sparkdeltalakes3iam.py
- python/delta-lake-examples/sparkdeltalakes3iamAutomation.py
- python/delta-lake-examples/sparkdeltalakes3iamonly.py
