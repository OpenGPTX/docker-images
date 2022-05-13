import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages "org.apache.hadoop:hadoop-aws:3.3.1" pyspark-shell'

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(os.environ.get('AWS_ROLE_ARN'))
print(os.environ.get('AWS_WEB_IDENTITY_TOKEN_FILE'))
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

import pyspark

sc=pyspark.SparkContext()
sc.setSystemProperty("com.amazonaws.services.s3.enableV4", "true")

hadoop_conf=sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
hadoop_conf.set("com.amazonaws.services.s3.enableV4", "true")
hadoop_conf.set("fs.s3a.connection.maximum", "100000")
hadoop_conf.set("fs.s3a.aws.credentials.provider", "com.amazonaws.auth.WebIdentityTokenCredentialsProvider")

spark=pyspark.sql.SparkSession(sc)

# Create a Delta table on S3:
spark.range(5).write.format("delta").mode("overwrite").save("s3a://tims-delta-lake/delta-table")

# Read a Delta table on S3:
spark.read.format("delta").load("s3a://tims-delta-lake/delta-table").show()
