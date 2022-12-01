# Databricks notebook source
dbutils.widgets.text("input","")
y = dbutils.widgets.get("input")
print ("parameter value : ")
print (y)
