#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession
import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.conf import SparkConf
from pyspark.sql.types import StringType, IntegerType, FloatType
#import pyspark.sql.functions as f
from pyspark.sql.functions import concat, split, col, when, lit, round, collect_list, array, substring, regexp_replace,regexp_extract, length, trim, expr
from datetime import datetime, timedelta
import json, re


# In[2]:


sc = SparkSession.builder.appName('preprocess').getOrCreate()


# In[3]:


start_str = '2022-05-24'
end_str = '2022-06-12'

start_date = datetime.strptime(start_str, '%Y-%m-%d')
end_date = datetime.strptime(end_str, '%Y-%m-%d')


# In[34]:


# prepare dataframe
import os
filepath = os.getcwd() + '/' # remove after local test
# filepath = 'hdfs://localhost:9000/input/'

with open(filepath + 'coupang20220524.json', 'rt', encoding='UTF8') as f:
    data = json.load(f)
          
origin_data = sc.sparkContext.parallelize(data).toDF()
origin_data = origin_data.withColumn("date", lit("2022-05-24"))
          
while start_date <= end_date :
    dates = start_date.strftime("%Y%m%d")
    
    with open(filepath + 'coupang' + dates + '.json', 'rt', encoding='UTF8') as nxt :
        nxt_df  = sc.sparkContext.parallelize(json.load(nxt)).toDF()
        nxt_df = nxt_df.withColumn("date", lit(start_date.strftime("%Y-%m-%d")))
    
        origin_data = origin_data.union(nxt_df)
    
    print(dates)
    start_date += timedelta(days=1)


# In[35]:


origin_data = origin_data.withColumn("volume", regexp_extract("name", "\d+\.+\d+g", 0).alias("volume"))     .withColumn("volume", when(col("volume")=="", "1").otherwise(col("volume")))     .withColumn("quantity", regexp_extract("name", "x\d+", 0))     .withColumn("quantity", when(col("quantity") == "", "1개").otherwise(col("quantity")))     .withColumn("brand", regexp_extract("name", "^\S+", 0).alias("brand"))     #.withColumn("option", regexp_extract("name", "\S+$", 0).alias("option")) # volume과 겹쳐서 pass


# In[36]:


origin_data = origin_data.withColumn('discount_price', origin_data.new_price.cast(IntegerType()))     .withColumn('original_price', origin_data.old_price.cast(IntegerType()))     .withColumn('store', lit("coupang"))     .withColumn('link', origin_data.href)     .withColumn('image', origin_data.img_src)     .drop(origin_data.new_price)     .drop(origin_data.old_price)     .drop(origin_data.href)     .drop(origin_data.img_src)


# In[37]:


origin_data = origin_data.withColumn("p_id", concat(origin_data.store.substr(0, 1), origin_data.id)) .withColumn("o_id", col("id")).drop("id") .withColumn("discount_percent", round(((origin_data.original_price - origin_data.discount_price) / origin_data.original_price) * 100, 1)) .withColumn("product_name", regexp_replace(regexp_replace("name", "\([^)]*\)", ""), "\[[^]]*\]", "")) .withColumn("big_category", lit("")) .withColumn("small_category", lit("")) .drop(origin_data.name)


# In[38]:


category_id_dict = {'176476': "아이섀도", '176477': "마스카라", '176478': "아이브로우", '176479': "아이메이크업세트", '176480': "포인트리무버", '402904': "아이팔레트"}


# In[235]:


# for i in category_id_dict:
#     origin_data = origin_data.withColumn("big_category", when(col("link").substr(-6,6) == i, category_id_dict[i]).otherwise(col("big_category")))


# In[39]:


origin_data = origin_data.withColumnRenamed("p_id", "id")


# In[41]:


origin_data = origin_data.withColumn("volume_new", pyspark.sql.functions.split(col('volume'), "g")[0]) .drop(origin_data.volume) .drop(origin_data.original_price)


# In[42]:


origin_data = origin_data.withColumnRenamed("volume_new", "volume")


# In[44]:


origin_data = origin_data.withColumn('volume', origin_data.volume.cast(FloatType()))

coupang_df = origin_data.withColumn("cost_effect", round(origin_data.discount_price / origin_data.volume, 1)) .withColumn("cost_effect", when(col("cost_effect") == "", 0).otherwise(col("cost_effect"))) 


# In[308]:


coupang_df.write.format("json").save('coupang.json')
#js = coupang_df.toJSON().map(lambda x : json.loads(x)).collect()


# In[26]:


coupang_price = coupang_df.select(['id', 'date', 'discount_price', 'store'])
coupang_price.write.format("json").save("coupang_price")
#js = coupang_price.toJSON().map(lambda x : json.loads(x)).collect()

