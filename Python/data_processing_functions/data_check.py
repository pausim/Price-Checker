import psycopg2
import pandas as pd
from datetime import datetime
from data_processing_functions.config import config

today_date = datetime.today().strftime('%Y-%m-%d')


def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # read connection parameters
        params = config("postgresql")

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def create_pandas_table(sql_query, database_connection=connect()):
    """Returns pandas dataframe from DB table"""
    cur = database_connection.cursor()
    table = pd.read_sql_query(sql_query, database_connection)
    cur.close()
    database_connection.close()
    return table


def make_timestamp_column(df, column_name):
    """Converts dataframe column to timestamp type"""
    df[column_name] = df[column_name].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))


def check_price(dataframe, item_name, price):
    """Filters out rows which are not of today and which do not meet price criteria

    Args:
        dataframe (pandas.DataFrame): full dataframe from DB table
        item_name (str): essential part of the item name which is needed to identify the item
        price (float): preferred price (for this price customer is willing to buy)
    """
    df = dataframe[(dataframe['name'].str.contains(item_name)) & (dataframe['price'] < price)
                   & (dataframe['load_date'] == today_date)]

    if df.empty:
        print('No {0} for such price ({1})!'.format(item_name, str(price)))

    else:
        df.columns = ['Item Name', 'Price', 'URL', 'Check Date']
        return df
