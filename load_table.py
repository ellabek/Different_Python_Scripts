from google.cloud import bigquery

def load_data_from_file(dataset_id, table_id, source_file_name, project):
    bigquery_client = bigquery.Client(project)
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    with open(source_file_name, 'rb') as source_file:
        # This example uses CSV, but you can use other formats.
        # See https://cloud.google.com/bigquery/loading-data
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = 'text/csv'
        job_config.skip_leading_rows = 1
        job_config.autodetect = True
        job_config.max_bad_records = 1
        job = bigquery_client.load_table_from_file(
            source_file, table_ref, job_config=job_config)

    job.result()  # Waits for job to complete

    print('Loaded {} rows into {}:{}.'.format(
        job.output_rows, dataset_id, table_id))


def main():
	
	#fill in credentials
    project = ""
    dataset_id = ""
    table_id = ""

    source_file_name = r'' #csv file
    load_data_from_file(dataset_id, table_id, source_file_name, project)


main()