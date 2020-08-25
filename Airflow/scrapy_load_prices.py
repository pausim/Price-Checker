from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

args = {
  'owner': 'airflow',
  'start_date': datetime(2020, 7, 29),
  'provide_context': True
}

dag = DAG(
  dag_id = 'scrapy_load_prices',
  default_args = args,
  schedule_interval = '36 16 * * *',
  catchup = False
)

task1 = BashOperator(
    task_id='remove_old_price_file',
    bash_command='rm /home/paulius/PycharmProjects/scrape_prices/scrape_prices/prices.jl',
    dag=dag
)

task2 = BashOperator(
    task_id='scrape_senukai',
    bash_command="""cd /home/paulius/PycharmProjects/scrape_prices/scrape_prices/; \
    scrapy crawl senukai -o prices.jl""",
    dag=dag
)

task3 = BashOperator(
    task_id='scrape_ikea',
    bash_command="""cd /home/paulius/PycharmProjects/scrape_prices/scrape_prices/; \
    scrapy crawl ikea -o prices.jl""",
    dag=dag
)

task4 = BashOperator(
    task_id='spark_load_to_postgres',
    bash_command="""cd /home/paulius/Documents/spark-2.4.5-bin-hadoop2.7/; \
    bin/spark-submit --driver-class-path /home/paulius/Documents/postgresql-42.2.12.jar \
    --jars /home/paulius/Documents/postgresql-42.2.12.jar --master local \
    --class load_prices_to_postgres \
    /home/paulius/IdeaProjects/item_prices/target/scala-2.12/item_prices_2.12-0.1.jar \
    /home/paulius/PycharmProjects/scrape_prices/scrape_prices/ prices.jl""",
    dag=dag
)

task5 = BashOperator(
    task_id='email_alert',
    bash_command="""cd /home/paulius/PycharmProjects/scrape_prices/; \
    python mail_alert.py""",
    dag=dag
)

task1 >> task2 >> task3 >> task4 >> task5
