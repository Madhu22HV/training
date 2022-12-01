# Databricks notebook source
spark.version

# COMMAND ----------

df = spark.read.text("/FileStore/tables/data/SPARK_README.md")

# COMMAND ----------

display(df.limit(10))

# COMMAND ----------

mnm_df3 = mnm_df2.groupBy("Color").count()
mnm_df3.show()
