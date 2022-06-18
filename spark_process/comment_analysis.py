#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.conf import SparkConf
from pyspark.sql.types import StructType, StringType, ArrayType, IntegerType, StructField, LongType
from pyspark.sql.functions import concat, split, col, when, lit, count,collect_list, filter
from pyspark.sql.functions import regexp_replace,regexp_extract, udf, explode, struct, slice
import datetime

sc = SparkSession.builder.appName("oliiveSpark").getOrCreate()


# In[3]:


schema = StructType().add("id", StringType())\
.add("comment", StringType())


# In[4]:


comment = sc.read.schema(schema).csv("hdfs://localhost:9000/input/review.csv")


# In[5]:


comment = comment.withColumn("revised_comment", regexp_replace("comment", "[^A-Za-z0-9가-힣]", ' ')).drop('comment')


# In[6]:


sq = SQLContext(sc)


# In[7]:


comment.createOrReplaceTempView("comment")

merged = sq.sql("SELECT id, concat_ws('', collect_list(revised_comment)) as comment FROM comment group by id")


# In[8]:


tokenized = merged.withColumn("comment", split("comment", " "))


# In[9]:


tokenized.printSchema()


# In[10]:


token_count = tokenized.select("id", explode("comment").alias("token"))\
.groupBy("id", "token")\
.count()\
.groupBy("id")\
.agg(collect_list(struct(col("token"), col("count"))).alias("text"))


# In[11]:


sorted_token = token_count.sort(token_count.text.count.desc())


# In[10]:


sorted_token.show()


# In[11]:


token_count.printSchema()


# In[16]:


olive = sc.read.json("olive_20220612.json")


# In[31]:


def def_sort(x) : 
    return sorted(x, key=lambda x :x[1], reverse = True)

udf_sort = udf(def_sort, ArrayType(StructType([StructField("token", StringType()),StructField("count",LongType())])))

sorted_t = token_count.select("id", udf_sort(col("text")).alias("text"))


# In[30]:


sorted_t.show()


# In[43]:


option = ["저는","제품", "선물을", "이건", "저의", "저희","요즘", "본인", "원래", "했습니다", "이다", "사용", "후기", "이거", "좀","잘", "너무", "것", "같아요", "이", "가", "은", "는", "더", "많이", "쓰고"]
stop_words = olive.rdd.flatMap(lambda x : [x.brand, x.big_category, x.small_category]).collect()
stop_words.extend(option)

is_none = lambda x : x != ''
is_stop = lambda x : ~(x.isin(stop_words))


res = sorted_t\
.withColumn("removed", filter(col("text.token"), is_none))\
.withColumn("token", filter(col("removed"), is_stop))\
.withColumn("token", slice(col("token"), 1, 10))\
.drop("text")\
.drop("removed")


# In[44]:


joined = res.join(olive, res.id == olive.id)
joined = joined.dropDuplicates(['id'])
final = joined.select(['name','comment.id', 'token'])


# In[45]:


final.show()


# In[46]:


final.write.json("analysls")


# In[ ]:




