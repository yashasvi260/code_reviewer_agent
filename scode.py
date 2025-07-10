from pyspark.sql.functions import col, month, sum

df = spark.read.format("delta").load("/mnt/data/purchases")

result = df.filter(col("status") == "Completed") \
    .groupBy("customer_id", month("purchase_date").alias("purchase_month")) \
    .agg(sum("amount").alias("total_spent"))
