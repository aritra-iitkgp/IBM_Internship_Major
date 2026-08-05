import boto3
from io import BytesIO
import pandas as pd

def read_from_s3(bucket_name, s3_key,AWS_REGION):
    try:
        s3 = boto3.client('s3',region_name = AWS_REGION)
        response = s3.get_object(Bucket=bucket_name, Key=s3_key)
        print("File Found")
        file_content = response['Body'].read()

        if s3_key.lower().endswith('.xlsx'):
            df = pd.read_excel(BytesIO(file_content))

        elif s3_key.lower().endswith('.csv'):
            df = pd.read_csv(BytesIO(file_content))
        else:
            df = pd.read_excel(BytesIO(file_content))  # default

        print(f"Successfully loaded: s3://{bucket_name}/{s3_key}")
        print(f"Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None