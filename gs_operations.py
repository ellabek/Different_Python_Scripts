from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from settings import gs_schema
from subprocess import call

credentials = GoogleCredentials.get_application_default()
service = discovery.build('storage', 'v1', credentials=credentials)

def get_from_gs_schema():
    call('gsutil cp {} {}'.format(gs_schema,'./schema.json'), shell=True)
