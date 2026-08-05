import boto3
from botocore.exceptions import ClientError
def create_bucket(bucket_name,AWS_REGION):
    try:
        
        s3 = boto3.client('s3',region_name=AWS_REGION)
        if AWS_REGION == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
            )
        print(f"Created: {bucket_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket already exists: {bucket_name}")
        else:
            print(f" Error creating {bucket_name}: {e}")
