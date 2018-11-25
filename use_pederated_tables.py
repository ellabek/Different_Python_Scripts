from google.cloud import bigquery
from datetime import datetime, timedelta
import pandas as pd
from settings import *

#fill in the GCP project name
client = bigquery.Client(project='') 

def delete_external_table(dataset,table):

    table_ref = client.dataset(dataset).table(table)
    try:
        client.delete_table(table_ref)
    except Exception:
        print("problem with deleting the table, check if it exists")
        return

    print('Table {}.{} deleted.'.format(dataset, table))

def create_external_table(dest_dataset,dest_table,gs_path):

    dataset_ref = client.dataset(dest_dataset)
    table_ref = bigquery.TableReference(dataset_ref, dest_table)
    table = bigquery.Table(table_ref)

    external_config = bigquery.ExternalConfig('CSV')
    external_config.autodetect = True
    external_config.max_bad_records = 100000000

    source_uris = [gs_path]
    external_config.source_uris = source_uris
    table.external_data_configuration = external_config

    client.create_table(table)
    print('Table {}.{} created.'.format(dest_dataset, dest_table))
