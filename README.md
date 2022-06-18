# Online Cosmetics Price Comparison

[ 대표 이미지 ]

## Project Description

온라인 화장품 소비가 증가하는 중이고 코로나19 완화로 화장품 판매가 증가할 것으로 예상된다. <br>
이에 온라인 화장품 판매 플랫폼을 통합하여 가격 변동 추이, 화장품 키워드 추출 및 유사 화장품을 추천하는 웹페이지를 구축했다.

## Installing

```
$ git clone https://github.com/philip-lee-khu/2022-01-PROJECT-GROUP4.git
```

## Running

- Web page

```
code
```

## Data Processing

### Data Acquisition

1. Data Crawling

- Coupang

- Musinsa

- Oliveyoung

### Data Storage

- HDFS

```
hdfs dfs -put {$filename} /input
hdfs dfs -ls /input
```

### Data Analysis

- Using Pyspark

```
spark-submit ${pyspark file} --master yarn --deploy-mode cluster --executor-memory 512m --driver-memory 512m
```

### Web Page

[ Structure Image]

- MongoDB

### Final Structure

[ Structure Image ]

## Demo

[ 세부 기능 이미지 - 검색, 가격 변동 그래프, 유사 상품 추천 등 ] <br>
http://3.34.179.67:8080/

## Scrum

[ Notion Home Image ]

### Notion

[notion link](https://sprinkle-rodent-a50.notion.site/Online-Cosmetics-Price-Comparison-204ec4397cac49cf8ea07e735db09b6f)
