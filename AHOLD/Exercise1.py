# Databricks notebook source
mnm_file = "/FileStore/tables/data/mnm_dataset.csv"

# COMMAND ----------

mnm1 = spark.read.csv(mnm_file)

# COMMAND ----------

mnm1.printSchema()

# COMMAND ----------

mnm2 = spark.read.format("csv").option("header","true").option("inferSchema","true").load(mnm_file)

# COMMAND ----------

mnm2.printSchema()

# COMMAND ----------

mnm2.groupBy("Color").count().show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Please find the aggregate count for California by filtering on State

# COMMAND ----------

from pyspark.sql.functions import col
mnm_state = mnm2.groupBy("State").count().filter(mnm2.State=='CA').show()
#mnm_CA = mnm_state.filter(col("State")=='CA')
#mnm_state.show()

# COMMAND ----------

from pyspark.sql.functions import sum
#display(mnm2.filter(mnm2.State=="CA").agg(sum("Count").alias("Total_count")))
mnm2.select("State","Color","Count").where(mnm2.State=='CA')

# COMMAND ----------

# MAGIC %md
# MAGIC #Please help me to find the count of all the colors and groupBy it with state and color, orderBy descending

# COMMAND ----------

from pyspark.sql.functions import col
mnm2_df_colors = mnm2.groupBy("Color","State").count()
mnm2_df_colors_order = mnm2_df_colors.orderBy(col("Color").desc(),col("State").desc()).display()

# COMMAND ----------

from pyspark.sql.functions import *
mnm2.select("State","Color","Count").groupBy("State","Color").agg(count("Count").alias("Total")).orderBy("Total",ascending=False).show()

# COMMAND ----------

# MAGIC %scala
# MAGIC import org.apache.spark.sql.functions._

# COMMAND ----------

# MAGIC %scala
# MAGIC val filepath = "/FileStore/tables/data/mnm_dataset.csv"
# MAGIC val mnm_file = spark.read.format("csv").option("header","true").option("inferSchema","true").load(filepath)

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC mnm_file.select("State","Color","Count").groupBy("State","Color").agg(count("Count").alias("Total")).orderBy(desc("Total")).show()

# COMMAND ----------

# MAGIC %scala
# MAGIC import org.apache.spark.sql.functions.col
# MAGIC mnm_file.select("State","Color","Count").where(col("State")==="CA").groupBy("State","Color").agg(count("Count").alias("Total")).orderBy(desc("Total")).show()

# COMMAND ----------


