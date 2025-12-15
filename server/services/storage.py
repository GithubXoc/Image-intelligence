from fastapi import UploadFile
from dotenv import load_dotenv

import boto3
import os

load_dotenv()

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")

s3_client = boto3.client("s3", region_name=AWS_REGION, 
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def upload_file_to_s3(file_location: str, file_name: str, file: UploadFile, is_analyzed: bool) -> str:
    try:
        extra_args = {'ContentType': file.content_type}
        
        is_analyzed_str = 'true' if is_analyzed else 'false'
        extra_args['Tagging'] = f'analyze={is_analyzed_str}'
        
        s3_client.upload_fileobj(
            Fileobj=open(file_location, "rb"),
            Bucket=BUCKET_NAME,
            Key=file_name,
            ExtraArgs=extra_args
        )
        s3_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
        return s3_url
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        raise e