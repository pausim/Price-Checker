# Price Checker

This project provides solution how to scrape prices from eshops and receive email alerts once they are below predefined threshold.

## How it works?

1. Data is scraped by Python framework scrapy
2. Scraped data is loaded to PostgreSQL by Apache Spark
3. Today's records are checked and mail is sent if price is lower than the preferred value (Python)

All these steps are triggered by scheduled DAG of Apache Airflow:

![Image of Apache Airflow DAG](https://github.com/pausim/Price-Checker/blob/master/Images/airflow_dag.png)


