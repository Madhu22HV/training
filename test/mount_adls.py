# Databricks notebook source
adlsAccountname = 'trainstorage22'

# COMMAND ----------

adlsContainerName = 'blobinput'

# COMMAND ----------

mountpoint = '/mnt/raw'

# COMMAND ----------

ClientId = dbutils.secrets.get(scope="adb-scope",key="ClientID")

# COMMAND ----------

TenantId = dbutils.secrets.get(scope="adb-scope",key="TenantID")

# COMMAND ----------

SecretValue = dbutils.secrets.get(scope="adb-scope",key="SecretValue")

# COMMAND ----------

endpoint = "https://login.microsoftonline.com/" + TenantId + "/oauth2/token"

# COMMAND ----------

source = "abfss://" + adlsContainerName + "@" + adlsAccountname + ".dfs.core.windows.net/"

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": ClientId,
          "fs.azure.account.oauth2.client.secret": SecretValue,
          "fs.azure.account.oauth2.client.endpoint":  endpoint }

# COMMAND ----------

if not any(mount.mountpoint == mountpoint for mount in dbutils.fs.mounts()):
    dbutils.fs.mount(
        source = source,
        mount_point = mountpoint,
        extra_configs = configs)

# COMMAND ----------

dbutils.fs.ls('/mnt/raw/test/test1/')

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

df = spark.read.csv("/mnt/raw/raw/mnm_dataset.csv",header=True,inferSchema=True)

# COMMAND ----------

df.createOrReplaceTempView("mnm")

# COMMAND ----------

# MAGIC %sql
# MAGIC select sum(count),color from mnm where state ='CA' group by color

# COMMAND ----------

# MAGIC %sql
# MAGIC select sum(count),color from mnm where state ='CA' group by color order by color desc

# COMMAND ----------


