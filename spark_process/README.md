### Spark Version
3.1.2 : comment_analysis.py<br>
2.4.8 : coupang_preprocess.py, product_info_process.py

Run on Spark Cluster
```
spark-submit ${pyspark file} --master yarn --deploy-mode cluster --executor-memory 512m --driver-memory 512m
```
