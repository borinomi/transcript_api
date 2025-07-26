import os
import tadata_sdk
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request  # ✅ Request 추가
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi

# 🔒 Swagger UI 및 OpenAPI 비활성화
app = FastAPI(title="My YT API", version="1.0.0")#, docs_url=None, redoc_url=None, openapi_url=None)

load_dotenv()
API_KEY = os.getenv("API_KEY")
YOUR_TADATA_API_KEY = os.getenv("YOUR_TADATA_API_KEY")
BASE_URL = os.getenv("YOUR_APIS_BASE_URL")

print("expected key:", API_KEY)

class VideoInput(BaseModel):
    video_id: str

@app.post("/get-transcript", operation_id="get_transcript")
async def get_transcript(data: VideoInput, request: Request):  # ✅ 여기도 request 추가
    # 🔐 API 키 인증
    client_key = request.headers.get("x-api-key")
    print("received key:", client_key)
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

    try:
        api = YouTubeTranscriptApi()
        result = api.fetch(data.video_id, languages=["ko", "en"])
        raw_list = result.to_raw_data()  # ← 핵심 수정 포인트
        full_text = " ".join(item["text"] for item in raw_list)
        return {"transcript": full_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Deploy the FastAPI app directly
result = tadata_sdk.deploy(
    fastapi_app=app,
    api_key=YOUR_TADATA_API_KEY,
    base_url=BASE_URL,
    name="My YT API"
)