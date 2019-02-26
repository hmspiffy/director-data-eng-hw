"""
Defines a class for DataReader that handles the reading of files from s3 buckets
"""

import os
import boto3
from data_loader.constants import (
    S3,
    BODY,
    BUCKET,
    PATH_KEY,
    DATA_PATH,
    S3_CONTENTS,
    OBJECT_SIZE,
    SOURCE_BUCKET,
    PROCESSED_BUCKET,
)
from data_loader.helper import (
    get_with_size_path
)


class DataReader:
    """
    This class fetches the list of files from S3 Bucket
    """

    def __init__(self):
        """
        Initializes the DataReader with the attributes
        """
        self.client = boto3.client(
            S3,
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )

    def list_all_objects(self):
        """
        Fetch the full list of objects in the s3 bucket
        """
        all_objects = self.client.list_objects(Bucket=SOURCE_BUCKET)
        return all_objects[S3_CONTENTS]

    def list_processed_files(self):
        """
        Fetch the list of objects processed in the target s3 bucket
        """
        processed_objects = self.client.list_objects(Bucket=PROCESSED_BUCKET)
        return get_with_size_path(
            processed_objects[S3_CONTENTS])

    def list_unprocessed_objects(self):
        """
        Fetch the list of objects not yet processed in the s3 bucket
        """

    def list_source_data_files(self):
        """
        Fetch the list of data files from the source s3 bucket
        """
        return get_with_size_path(self.list_all_objects())

    def copy_to_processed_bucket(self, object_to_read):
        """
        Copies a file into the processed bucket
        """
        object_key = object_to_read[PATH_KEY]
        copy_source = {
            BUCKET: SOURCE_BUCKET,
            PATH_KEY: object_key
        }
        return self.client.copy_object(
            Bucket=PROCESSED_BUCKET,
            CopySource=copy_source,
            Key=object_key)

    def get_file(self, object_to_read):
        """
        Return a pointer to the file
        """
        object_key = object_to_read[PATH_KEY]
        object_to_get = self.client.get_object(
            Bucket=SOURCE_BUCKET,
            Key=object_key)
        return object_to_get[BODY]
