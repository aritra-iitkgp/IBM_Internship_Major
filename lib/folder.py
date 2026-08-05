import boto3
def create_folder(bucket, folder,AWS_REGION):
    try:
        s3 = boto3.client('s3',region_name = AWS_REGION )
        s3.put_object(Bucket=bucket, Key=folder)
        print(f"Folder created: s3://{bucket}/{folder}")
    except:
        pass