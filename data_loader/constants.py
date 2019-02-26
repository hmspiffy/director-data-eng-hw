"""
Constants used in data loader
"""

# Data Reader
S3 = 's3'
BUCKET = 'Bucket'
SOURCE_BUCKET = 'hinge-homework'
# We're using a secondary bucket to copy files into when they are processed
# PROCESSED_BUCKET = 'homework-processed'
PROCESSED_BUCKET = 'homework-processed-test'
S3_CONTENTS = 'Contents'
OBJECT_SIZE = 'Size'
PATH_KEY = 'Key'
DATA_PATH = 'director-data-engineering/ratings/'
BODY = 'Body'


# Helper - Using PascalCase for consistency with Boto3
UTF8 = 'utf-8'
TAB = '\t'
TIMESTAMP_FIELD = 'Timestamp'
PLAYER_ID_FIELD = 'PlayerId'
SUBJECT_ID_FIELD = 'SubjectId'
RATING_TYPE_FIELD = 'RatingType'

# Rating Types
ALLOWED_RATINGS = '012345'
SKIP = 'skip'
LIKE = 'like'
COMMENT = 'comment'
REMOVE = 'remove'
BLOCK = 'block'
REJECT = 'reject'
REPORT = 'report'
MATCH = 'match'
