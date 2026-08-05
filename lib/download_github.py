import requests
import os
from io import BytesIO
import boto3
def download_from_github(repo_url,S3_SOURCE_BUCKET,S3_PREFIX,AWS_REGION,branch="dev"):
    try:
      s3 = boto3.client('s3',region_name = AWS_REGION )
      if "github.com" in repo_url:
          repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
          repo_url = f"{repo_url}/{branch}"

      print(f"Fetching files from: {repo_url}")


      files_to_download = [
          "Files/Data/Telco-Customer-Churn.csv"
      ]

      uploaded_files = []

      for file_path in files_to_download:
          raw_url = f"{repo_url}/{file_path}"
          print(f"Downloading: {raw_url}")

          response = requests.get(raw_url)
          print(f"Status Code: {response.status_code}")
          if response.status_code == 200:
              file_name = os.path.basename(file_path)
              s3_key = S3_PREFIX + file_name


              s3.upload_fileobj(BytesIO(response.content), S3_SOURCE_BUCKET, s3_key)

              print(f"Uploaded: {file_name} → s3://{S3_SOURCE_BUCKET}/{s3_key}")
              uploaded_files.append(file_name)
          else:
              print(f"Failed to download: {file_path}")

      return uploaded_files
    except Exception as e:
      print(e)
      print("Failed to fetch files from github")