import os
import pyspark
from delta import configure_spark_with_delta_pip

# add the maven packages you want to use
maven_packages = [
    "io.delta:delta-core_2.12:1.1.0",
    "org.apache.hadoop:hadoop-aws:3.3.1",
]
maven_packages = ",".join(maven_packages)

os.environ["JAVA_HOME"] = "/usr/lib/jvm/default-java"
os.environ["PYSPARK_SUBMIT_ARGS"] = f'--packages "{maven_packages}" pyspark-shell'

builder = (
    pyspark.sql.SparkSession.builder.appName("MyApp")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "com.amazonaws.auth.WebIdentityTokenCredentialsProvider",
    )
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()

df = spark.range(5).withColumnRenamed("id", "num")
df.write.format("parquet").mode("overwrite").save("s3a://opengptx/examples/kfp/numbers")
