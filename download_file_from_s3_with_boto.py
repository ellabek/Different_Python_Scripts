import boto
import sys, os
from boto.s3.key import Key
from boto.exception import S3ResponseError

DOWNLOAD_LOCATION_PATH =""
BUCKET_NAME = "bd-public"
AWS_ACCESS_KEY_ID= ""
AWS_ACCESS_SECRET_KEY = ""
conn  = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_KEY)
bucket = conn.get_bucket(BUCKET_NAME)

#goto through the list of files
bucket_list = bucket.list()

for l in bucket_list:
    key_string = str(l.key)

    s3_path = DOWNLOAD_LOCATION_PATH + key_string

    try:
        print ("Current File is ", s3_path)
        l.get_contents_to_filename(s3_path)
    except (OSError, S3ResponseError) as e:
        pass
        #check if the file has been downloaded locally
        if not os.path.exists(s3_path):
            try:
                os.makedirs(s3_path)
            except OSError as exc:
                import errno

                if exc.errno != errno.EEXIST:
                    raise