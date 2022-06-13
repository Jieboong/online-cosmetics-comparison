#!/usr/bin/env python
# coding: utf-8

# ### Musinsa Data PreProcess

# In[527]:


import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.conf import SparkConf
from pyspark.sql.types import StringType
from pyspark.sql.functions import concat, split, col, when, lit, round,collect_list, array
from pyspark.sql.functions import regexp_replace,regexp_extract
from datetime import datetime, timedelta
import json

sc = SparkSession.builder.appName("preprocess").getOrCreate()


# In[475]:


start = '2022-06-03'
last = '2022-06-13'

start_date = datetime.strptime(start, '%Y-%m-%d')
last_date = datetime.strptime(last, '%Y-%m-%d')

with open('hdfs://localhost:9000/input/20220602.json') as f:
    data = json.load(f)

d = sc.sparkContext.parallelize(data).toDF()
d = d.withColumn("date", lit('2022-06-02'))
while start_date <= last_date :
    dates = start_date.strftime("%Y%m%d")
    print(dates)
    
    with open('hdfs://localhost:9000/input/'+dates+'.json') as nxt :
        
        nxt_df  = sc.sparkContext.parallelize(json.load(nxt)).toDF()
        
        nxt_df = nxt_df.withColumn("date", lit(start_date.strftime("%Y-%m-%d")))
        d = d.union(nxt_df)
        
    start_date += timedelta(days=1)


# In[476]:


d.printSchema()


# In[477]:


from pyspark.sql.types import IntegerType

df = d.withColumn("original_price", regexp_replace(d.old_price, ',', '').cast(IntegerType()))\
.withColumn("discount_price", regexp_replace(d.new_price, ',', '').cast(IntegerType()))\
.withColumn("store", lit("musinsa"))\
.drop(d.old_price)\
.drop(d.new_price)


# In[478]:


df.show(5)


# In[479]:


df = df.withColumn("p_id", concat(df.store.substr(0, 1), df.product_id))\
.withColumn("discount_percent", round(((df.original_price - df.discount_price)/df.original_price)*100, 1))

df = df.withColumnRenamed("p_id", "id").withColumn("o_id", col("product_id")).drop("product_id")

df = df.withColumn("volume", regexp_extract("title", "\d+ml", 0).alias("volume"))\
.withColumn("quantity", regexp_extract("title", "x\d+", 0))\
.withColumn("volume", when(col("volume")=="", 0).otherwise(col("volume")))\
.withColumn("quantity", when(col("quantity") == "", "1개").otherwise(col("quantity")))\
.withColumn("big_category", col("category"))\
.withColumn("small_category", array(lit("")))\
.drop("category")\
.drop("option")\
.drop("sale")


# In[480]:


df.show()


# In[481]:


mu_df = df.withColumn("cost_effect", round(df.discount_price/df.volume, 1))\
    .withColumn("product_name", regexp_replace(regexp_replace("title", "\([^)]*\)", ""), "\[[^]]*\]", "")).drop("title")


# In[500]:


mu_df = mu_df.na.fill(0)


# ### Olive Young Data Preprocess

# In[501]:


start = '2022-06-06'
last = '2022-06-13'

start_date = datetime.strptime(start, '%Y-%m-%d')
last_date = datetime.strptime(last, '%Y-%m-%d')

origin_data = sc.read.json('hdfs://localhost:9000/input/olive_20220605.json')
origin_data = origin_data.withColumn("date", lit("2022-06-05"))
while start_date <= last_date :
    dates = start_date.strftime("%Y%m%d")
    
    nxt = sc.read.json('hdfs://localhost:9000/input/olive_' + dates+'.json')
    nxt = nxt.withColumn("date", lit(start_date.strftime("%Y-%m-%d")))
    
    origin_data = origin_data.union(nxt)
    
    print(dates)
    start_date += timedelta(days=1)


# In[502]:


from pyspark.sql.types import IntegerType

df = origin_data.withColumn("original_price", regexp_replace(origin_data.original_price, ',', '').cast(IntegerType()))\
.withColumn("discount_price", regexp_replace(origin_data.cur_price, ',', '').cast(IntegerType()))\
.withColumn("image", origin_data.img)\
.withColumn("store", lit("olive"))\
.drop(origin_data.cur_price)\
.drop(origin_data.img)\
.drop(origin_data.payment_benefit)


# In[503]:


df = df.withColumn("p_id", concat(df.store.substr(0, 1), df.id))\
            .withColumn("o_id", col("id")).drop("id")\
.withColumn("discount_percent", round(((df.original_price - df.discount_price)/df.original_price)*100, 1))


# In[504]:


df = df.withColumnRenamed("p_id", "id")


# In[505]:


df = df.withColumn("volume", regexp_extract("name", "\d+ml", 0).alias("volume"))\
.withColumn("quantity", regexp_extract("name", "x\d+", 0))\
.withColumn("volume", when(col("volume")=="", None).otherwise(col("volume")))\
.withColumn("quantity", when(col("quantity") == "", "1개").otherwise(col("quantity")))\
.drop("on_discount").drop("soldout").drop("")


# In[506]:


olive_df = df.withColumn("cost_effect", round(df.discount_price/df.volume, 1))\
    .withColumn("product_name", regexp_replace(regexp_replace("name", "\([^)]*\)", ""), "\[[^]]*\]", ""))\
    .drop("color_options")\
    .drop("name")


# In[507]:


mu_df = mu_df.withColumn("shipping", lit(""))


# In[508]:


olive_df.printSchema()
mu_df.printSchema()


# In[511]:


olive_df.write.json("olive")


# In[512]:


mu_df.write.json("mu")


# In[ ]:


mu_df.show(5)


# In[514]:


olive_df.write.format("json").save('olive.json')


# In[515]:


olive_price = olive_df.select(['id', 'date', 'discount_price'])


# In[516]:


olive_price.show()


# In[517]:


olive_price.write.format("json").save("olive_price")

