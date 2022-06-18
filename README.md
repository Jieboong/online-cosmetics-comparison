# Online Cosmetics Price Comparison

[ 대표 이미지 ]

## Project Description

> 코로나19 마스크 규제 완화로 온라인 화장품 소비 증가 추세 예상 <br>
> 온라인 화장품 판매 플랫폼을 통합하여 가격 변동 추이, 화장품 키워드 추출 및 유사 화장품을 추천하는 웹페이지 구축

## Installing

```
$ git clone https://github.com/philip-lee-khu/2022-01-PROJECT-GROUP4.git
```

## Running

- Web page

```
## Run Server at kbeauty_api
webapp/kbeauty_api$ node app.js

## Run Web Page at kbeauty
webapp/kbeauty$ npm install
webapp/kbeauty$ npm start
```

## Data Processing

### 1. Data Acquisition

- Data Crawling

  - Coupang
    [ 카테고리 이미지 ]
    [ 마스카라 Elements 예시 ]

    - 언어: Python
    - 주요 라이브러리: `BeautifulSoup`, `requests`, `pandas`, `re`
    - 각 카테고리(Depth 2까지 - 대분류, 소분류) 별 모든 페이지 링크에 `requests`로 접근하여 상품 정보 parsing

  - Musinsa

    - 언어: Python
    - 주요 라이브러리: `BeautifulSoup`, `requests`, `json`, `multiprocessing`, `contextlib`
    - json 형식으로 모든 상품 링크 저장
    - 각 링크에 `requests`로 접근하여 상품 정보 parsing
    - `multiprocessing`으로 크롤링 속도 개선

  - Olive Young
    - 언어: Python
    - 주요 라이브러리: `BeautifulSoup`, `selenium`, `requests`, `json`
    - 각 카테고리 `selenium`으로 접근하여 json 형식으로 저장
    - 상품 데이터만으로 용량이 부족하여 후기가 가장 활성화된 올리브영에서 comment 정보 parsing

  - Olive Young Comment
    - 언어 : Python
    - 주요 라이브러리 : 'selenium', 'json'
    - 각 카테고리 상위 품목을 'selenium'으로 접근해 상품 번호와 줄글 리뷰 저장
    - 크롤링 시간 고려해 각 상품당 최대 300개의 리뷰 크롤링


### 2. Data Storage

- HDFS Cluster Settings
```
hadoop namenode -format
./sbin/start-all.sh
```
- HDFS put files
```
hdfs dfs -put {$filename} /input
hdfs dfs -ls /input
```

### 3. Data Analysis

- Using Pyspark

```
spark-submit ${pyspark file} --master yarn --deploy-mode cluster --executor-memory 512m --driver-memory 512m
```

### 4. Web Page

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
