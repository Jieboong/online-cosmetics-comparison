# Online Cosmetics Price Comparison

![image](https://user-images.githubusercontent.com/47781507/174441774-18d2c307-9e1c-427c-9f1d-6b9d289f65e7.png)

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

📍 <b>Data Crawling</b>

![image](https://user-images.githubusercontent.com/47781507/174441677-6b31796c-c271-4838-a167-9188f81f97a8.png)

- Coupang (43MB)
  - Language: Python
  - Libraries: `BeautifulSoup`, `requests`, `pandas`, `re`
  - 각 카테고리(Depth 2까지 - 대분류, 소분류) 별 모든 페이지 링크에 `requests`로 접근하여 상품 정보 parsing

---

![image](https://user-images.githubusercontent.com/47781507/174441644-4a5524aa-616c-4b80-8b0a-0e0af2a911f6.png)

- Musinsa (110MB)
  - Language: Python
  - Libraries: `BeautifulSoup`, `requests`, `json`, `multiprocessing`, `contextlib`
  - json 형식으로 모든 상품 링크 저장
  - 각 링크에 `requests`로 접근하여 상품 정보 parsing
  - `multiprocessing`으로 크롤링 속도 개선

---

![image](https://user-images.githubusercontent.com/47781507/174441656-32215742-8d0a-4a11-a3b7-e92873144bb4.png)

- Olive Young (112MB)

  - Language: Python
  - Libraries: `BeautifulSoup`, `selenium`, `requests`, `json`
  - 각 카테고리 `selenium`으로 접근하여 json 형식으로 저장
  - 상품 데이터만으로 용량이 부족하여 후기가 가장 활성화된 올리브영에서 comment 정보 parsing

- Olive Young Comment (582MB)
  - Language : Python
  - Libraries : 'selenium', 'json'
  - 각 카테고리 상위 품목을 'selenium'으로 접근해 상품 번호와 줄글 리뷰 저장
  - 크롤링 시간 고려해 각 상품당 최대 300개의 리뷰 크롤링

📍 <b>Distributing Crawler</b>

- Server: AWS EC2 instance
- Crontab 활용하여 매일 crawling

```
# 0 0 * * * python3 /home/musinsa/app.py
# 0 0 * * * python3 /home/ubuntu/olive_crawl/olive_crawl.py
# 0 0 * * * python3 /home/coupang/crawl.py
```

### 2. Data Storage

- 모든 크롤링 결과 파일: hdfs:///input에 저장

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

- 상품 크롤링 결과 파일
  - 정규식 활용(`regexp_extract`, `regexp_replace`)하여 상품명 | 브랜드 | 용량 등 분리
  - 할인율과 가성비(단위 용량 당 가격) 계산
  - 불필요한 column 제거
  - Column명 통일
    <br>
- 올리브영 리뷰 크롤링 결과 파일
  - 목표: 각 상품별 가장 많이 쓰인 단어 추출
  - 특수 문자 제거, `split`으로 review 정보 분리
  - 단어 수 계산 후 count 기준으로 정렬
  - Blank word, Stop word, Brand/Category명 제거

### 4. Web Page

![image](https://user-images.githubusercontent.com/47781507/174441800-a4967ab7-e887-4a28-96bb-a0c409dfc762.png)

- Language: Javascript
- Front-End: React, Tailwind CSS
- Back-End: Express.js
- Database: MongoDB

### Final Structure

![image](https://user-images.githubusercontent.com/47781507/174441812-5f0a0591-87a9-4e3f-a28f-f2679e49c2d3.png)

## Demo

🔗 [Webpage link](http://3.34.179.67:8080/)

![image](https://user-images.githubusercontent.com/47781507/174441844-6ea4a136-f325-48a9-affe-2aabd6d3f339.png)

> 메인페이지(검색)

![image](https://user-images.githubusercontent.com/47781507/174441825-8b8e2bb6-fd6a-4203-8d0e-6780b19b1a8f.png)

> 상세페이지(화장품 키워드, 가격 변동 그래프, 유사 화장품 추천)

## Scrum

### Notion

![image](https://user-images.githubusercontent.com/47781507/174441980-83abe3e0-f044-4f76-8af7-4c76de080c2c.png)

- 매주 목요일 오후 3시 Google Meet 회의, Notion에 진행 상황 기록 <br>
  🔗 [Notion link](https://sprinkle-rodent-a50.notion.site/Online-Cosmetics-Price-Comparison-204ec4397cac49cf8ea07e735db09b6f)
