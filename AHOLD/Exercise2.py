# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC #SFO Fire Calls

# COMMAND ----------

sf_fire_file ="/FileStore/tables/data/sf-fire/sf_fire_calls.csv"

# COMMAND ----------

# MAGIC %fs ls "/FileStore/tables/data/sf-fire/sf_fire_calls.csv"

# COMMAND ----------

# MAGIC %fs head "/FileStore/tables/data/sf-fire/sf_fire_calls.csv"

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df = spark.read.csv("/FileStore/tables/data/sf-fire/sf_fire_calls.csv",header = True, inferSchema = True)

# COMMAND ----------

df.count()

# COMMAND ----------

df.cache()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

display(df.limit(5))

# COMMAND ----------

df.where(df.CallType =="Medical Incident").display()

# COMMAND ----------

df.where(df.CallType =="Medical Incident").count()

# COMMAND ----------

display(df.select("CallNumber","CallType").filter(df.Delay > 5))

# COMMAND ----------


