# Databricks notebook source
# MAGIC %md
# MAGIC #UDFs

# COMMAND ----------

df = spark.read.csv("/FileStore/tables/data/flights/departuredelays.csv",header = True,inferSchema = True)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

from pyspark.sql.types import *

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

df1 = (spark.read.format("csv").schema("date STRING,delay INT,distance INT,origin STRING,destination STRING").option("header","true").option("path","/FileStore/tables/data/flights/departuredelays.csv").load())


# COMMAND ----------

df1.printSchema()

# COMMAND ----------

flightschema = StructType([StructField('date' , StringType(),True),
                 StructField('delay', IntegerType(),True),
                 StructField('distance', IntegerType(),True),
                 StructField('origin', StringType(),True),
                 StructField('destination', StringType(),True)])

# COMMAND ----------

df2 = spark.read.csv("/FileStore/tables/data/flights/departuredelays.csv",header = True,schema = flightschema)

# COMMAND ----------

df2.printSchema()

# COMMAND ----------

flightschema1 = StructType([StructField('date' ,TimestampType(),True),
                 StructField('delay', IntegerType(),True),
                 StructField('distance', IntegerType(),True),
                 StructField('origin', StringType(),True),
                 StructField('destination', StringType(),True)])

# COMMAND ----------

df3 = spark.read.csv("/FileStore/tables/data/flights/departuredelays.csv",header = True,schema = flightschema1)

# COMMAND ----------

df3.show(10)

# COMMAND ----------

df2 = df2.withColumn("date",df2["date"].cast(DateType()))

# COMMAND ----------

df2.show(10)

# COMMAND ----------

def dayhourmin(d_str):
    lst = [char for char in d_str]
    return "".join(lst[0:2]) + "/" + "".join(lst[2:4]) + " " +"" + "".join(lst[4:6]) + ":" + "".join(lst[6:])

# COMMAND ----------

def to_datetimestr(d_str):
    lst = [char for char in d_str]
    return current_date   + "".join(lst[0:2]) + "/" + "".join(lst[2:4]) + " " +"" + "".join(lst[4:6]) + ":" + "".join(lst[6:])

# COMMAND ----------

dayhourmin(None)

# COMMAND ----------

dayhourmin1 = udf(lambda z: dayhourmin(z),StringType())

# COMMAND ----------

spark.udf.register("dayhourmin1",dayhourmin ,StringType())

# COMMAND ----------

df1.createOrReplaceTempView("us_flight_delay_tbl")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from us_flight_delay_tbl

# COMMAND ----------

# MAGIC %sql
# MAGIC CACHE TABLE us_flight_delay_tbl

# COMMAND ----------

spark.sql("select * from us_flight_delay_tbl limit 10").show()

# COMMAND ----------

spark.sql("select distance,origin,destination,delay,dayhourmin1(date) from us_flight_delay_tbl where distance > '1000' limit 10").show()

# COMMAND ----------

spark.sql("select distance,origin,destination,delay,dayhourmin1(date) from us_flight_delay_tbl where origin ='SFO' and destination ='ORD' and delay > '120' limit 10").show()

# COMMAND ----------

spark.sql("""select distance,origin,destination,delay,
    CASE WHEN delay = '0' then 'no_delay'
     WHEN delay > '0' and delay < '30' then 'low'
     WHEN delay > '30' and delay < '120' then 'medium' 
     else 'high' end as flight_delay  from us_flight_delay_tbl where origin ='SFO' and destination ='ORD' and delay > '120' limit 10""").show()

# COMMAND ----------

# MAGIC %sql
# MAGIC select distance,origin,destination,delay,
# MAGIC CASE WHEN delay = '0' then 'no_delay'
# MAGIC      WHEN delay > '0' and delay < '30' then 'low'
# MAGIC      WHEN delay > '30' and delay < '120' then 'medium' 
# MAGIC      else 'high' end as flight_delay from us_flight_delay_tbl

# COMMAND ----------

spark.catalog.registerFunction

# COMMAND ----------

spark.catalog.listFunctions(name="dayhourmin1")

# COMMAND ----------


