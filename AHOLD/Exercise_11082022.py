# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC ###different data sources - JSON, CSV, Parquet, ORC, Avro

# COMMAND ----------

parquet_file = '/FileStore/tables/data/flights/summary-data/parquet/2010-summary.parquet'

json_file = '/FileStore/tables/data/flights/summary-data/json/*'

csv_file ='/FileStore/tables/data/flights/summary-data/csv/*'

orc_file = '/FileStore/tables/data/flights/summary-data/orc/2010-summary.orc'

avro_file = '/FileStore/tables/data/flights/summary-data/avro/*'

# COMMAND ----------

df1 = spark.read.parquet(parquet_file)
df1.printSchema()

# COMMAND ----------

# MAGIC %fs ls "/FileStore/tables/data/flights/summary-data/csv/"

# COMMAND ----------

df = spark.read.csv("/FileStore/tables/data/flights/summary-data/csv/2010_summary.csv", header = True)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

par_schema ="DEST_COUNTRY_NAME STRING,ORIGIN_COUNTRY_NAME STRING,count INT"

# COMMAND ----------

df_par = spark.read.parquet(parquet_file, schema = par_schema )

# COMMAND ----------

df_par = spark.read.format("parquet").option("schema", "par_schema").load(parquet_file)

# COMMAND ----------

df_par.printSchema()

# COMMAND ----------

from pyspark.sql.types import *

# COMMAND ----------

par_schema = StructType([StructField('DEST_COUNTRY_NAME' , StringType(),True),
                 StructField('ORIGIN_COUNTRY_NAME', IntegerType(),True),
                 StructField('ORIGIN_COUNTRY_NAME', IntegerType(),True)
                 ])

# COMMAND ----------

df_par.createOrReplaceTempView('us_flight_delay')

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from us_flight_delay limit 10

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE us_flight_delay_par using parquet LOCATION '/FileStore/tables/data/flights/summary-data/parquet/2010-summary.parquet'

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from us_flight_delay_par limit 5

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE us_flight_delay_csv using CSV LOCATION '/FileStore/tables/data/flights/summary-data/csv/2010_summary.csv'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE us_flight_delay_json using JSON LOCATION '/FileStore/tables/data/flights/summary-data/json/2010_summary.json'

# COMMAND ----------

# MAGIC %sql
# MAGIC --DROP TABLE us_flight_delay_orc
# MAGIC CREATE TABLE us_flight_delay_orc (DEST_COUNTRY_NAME STRING,ORIGIN_COUNTRY_NAME STRING,count LONG) USING orc LOCATION '/FileStore/tables/data/flights/summary-data/orc/2010_summary.orc/part-r-00000-2c4f7d96-e703-4de3-af1b-1441d172c80f.snappy.orc'

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from us_flight_delay_orc limit 5

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE us_flight_delay_avro using avro LOCATION '/FileStore/tables/data/flights/summary-data/avro/_/part_00000_tid_7128780539805330008_467d814d_6f80_4951_a951_f9f7fb8e3930_1434_1_c000.avro'

# COMMAND ----------

df_avro = spark.read.format("avro").load("/FileStore/tables/data/flights/summary-data/avro/_/part_00000_tid_7128780539805330008_467d814d_6f80_4951_a951_f9f7fb8e3930_1434_1_c000.avro")

# COMMAND ----------

df_avro.show(10)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from us_flight_delay_avro limit 10

# COMMAND ----------

# MAGIC %fs head '/FileStore/tables/data/flights/summary-data/json/2010_summary.json'

# COMMAND ----------

/FileStore/tables/data/cctvVideos/train_images/label=0

# COMMAND ----------

from pyspark.ml import image

# COMMAND ----------

df_image = spark.read.format("image").load("/FileStore/tables/data/cctvVideos/train_images/")

# COMMAND ----------

df_image.printSchema()


# COMMAND ----------

df_image.display()

# COMMAND ----------

df_image.show(2)

# COMMAND ----------

df_img = spark.read.format("binaryfile").option("pathGlobFilter","*.jpg").load("/FileStore/tables/data/cctvVideos/train_images/")

# COMMAND ----------

df_img.show(10)

# COMMAND ----------

df_img.printSchema()

# COMMAND ----------

spark.sql("SHOW Databases").show()

# COMMAND ----------

spark.sql("CREATE DATABASE training")

# COMMAND ----------

spark.sql("USE DATABASE training")

# COMMAND ----------

spark.sql("show tables").show()

# COMMAND ----------

spark.sql("CREATE TABLE us_filght_delay (date STRING, delay INT , distance INT, origin STRING , destination STRING )")

# COMMAND ----------

df_delay = spark.read.csv("/FileStore/tables/data/flights/departuredelays.csv",header=True, schema = ("date STRING, delay INT , distance INT, origin STRING , destination STRING "))

# COMMAND ----------

df_delay.printSchema()

# COMMAND ----------

df_delay.write.mode("overwrite").saveAsTable("us_filght_delay")

# COMMAND ----------

display(spark.catalog.listTables(dbName="training"))

# COMMAND ----------

spark.catalog.listTables(dbName="training")

# COMMAND ----------


