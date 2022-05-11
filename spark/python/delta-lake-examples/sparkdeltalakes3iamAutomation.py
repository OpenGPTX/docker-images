import os
import pyspark
from delta import *

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages "io.delta:delta-core_2.12:1.1.0,org.apache.hadoop:hadoop-aws:3.3.1" pyspark-shell'

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.WebIdentityTokenCredentialsProvider")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Create a Delta table on S3:
spark.range(5).write.format("delta").mode("overwrite").save("s3a://961123334118-dev-tim2-kf3-sparkdeltalake/delta-table")

# Read a Delta table on S3:
spark.read.format("delta").load("s3a://961123334118-dev-tim2-kf3-sparkdeltalake/delta-table").show()
