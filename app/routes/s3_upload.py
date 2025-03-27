from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
import uuid
import boto3
import os
import requests

router = APIRouter()

# Optional: protect with auth if needed
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION", "us-east-1")

if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME]):
    raise RuntimeError("Missing AWS credentials or bucket info")

# S3 client
s3 = boto3.client(
    "s3",
    region_name=S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def get_presigned_upload_url_util(filename: str):
    ext = filename.split(".")[-1].lower()
    key = f"profile_pictures/{uuid.uuid4()}.{ext}"

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": S3_BUCKET_NAME,
            "Key": key,
            "ContentType": f"image/{ext}",
        },
        ExpiresIn=3600,
    )

    return {
        "upload_url": url,
        "file_url": f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{key}",
    }

@router.get("/upload-url/")
def get_presigned_upload_url(filename: str = Query(..., min_length=1)):
    return get_presigned_upload_url_util(filename)

@router.post("/proxy-upload/")
async def proxy_upload_file(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    if ext not in {"jpg", "jpeg", "png", "webp"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    print(file.filename)
    # 🚫 Instead of HTTP call, call directly:
    data = get_presigned_upload_url_util(file.filename)
    print(data)
    # Upload the file using the signed URL
    contents = await file.read()
    print(ext)
    upload_resp = requests.put(
        data["upload_url"],
        data=contents,
        headers={"Content-Type":  f"image/{ext}"}
    )
    print(upload_resp)
    if upload_resp.status_code != 200:
        raise HTTPException(status_code=500, detail="Upload to S3 failed")

    return {"file_url": data["file_url"]}