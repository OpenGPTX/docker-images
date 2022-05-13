
import os
import pyspark
from delta import *

import time

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages "io.delta:delta-core_2.12:1.1.0,org.apache.hadoop:hadoop-aws:3.3.1" pyspark-shell'

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.driver.memory", "7g") \
    .config("spark.hadoop.fs.s3a.access.key", "AKIA4SD*******************") \
    .config("spark.hadoop.fs.s3a.secret.key", "DMyLZp60ZuR**************************************") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

import dbldatagen as dg

schema = dg.SchemaParser.parseCreateTable(spark, """
    create table Test1 (
    source string ,
    language string ,
    topic string ,
    license string )
""")

data_rows = 4*10**9

x3 = (dg.DataGenerator(sparkSession=spark, name="test_table_query", rows=data_rows, partitions=20)
      .withSchema(schema)
      .withIdOutput()
      .withColumnSpec("source", values=["hackernews", "cc", "wikipedia", "academic", "books", "pubmed", "opensubtitiles", "youtubesubtitles"], random=True)
      .withColumnSpec("language", values=["en", "de", "fr", "es", "ru"], random=True)
      .withColumnSpec("topic", values=["software", "medical", "cultural", "academic", "hardware", "ai", "ml", "random"], random=True)
      .withColumnSpec("license", values=["MIT", "GPL-v2", "GPL-v3", "private", "apache", "cc"], random=True)
     )

x3_output_full = x3.build()

start = time.monotonic_ns()
#x3_output_full.write.format("delta").mode("overwrite").saveAsTable("test_data")
x3_output_full.write.format("delta").mode("overwrite").saveAsTable("test_data", path='s3a://tims-delta-lake/delta-table-bench')
print("Time elapsed : ", (time.monotonic_ns() - start)/10**9, "s")

data_table = spark.table("test_data")
data_table.count()

#display(data_table.groupby("language").count())
start = time.monotonic_ns()
data_table.groupby("language").count().show()
print("Time elapsed : ", (time.monotonic_ns() - start)/10**9, "s")
#32s (2m)

#display(data_table.groupby("language", "license").avg())
start = time.monotonic_ns()
data_table.groupby("language", "license").avg().show()
print("Time elapsed : ", (time.monotonic_ns() - start)/10**9, "s")
#87s (6,5m)

#display(data_table.groupby("topic", "source").count())
start = time.monotonic_ns()
data_table.groupby("topic", "source").count().show()
print("Time elapsed : ", (time.monotonic_ns() - start)/10**9, "s")
#73s (4m)
