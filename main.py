from fastapi import FastAPI, HTTPException
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
print(dir(YouTubeTranscriptApi))
print(YouTubeTranscriptApi.fetch)

app = FastAPI()

class VideoInput(BaseModel):
    video_id: str

@app.post("/get-transcript", operation_id="get_transcript")
async def get_transcript(data: VideoInput):
    try:
        api = YouTubeTranscriptApi()
        result = api.fetch(data.video_id, languages=["ko", "en"])
        raw_list = result.to_raw_data()  # ← 핵심 수정 포인트
        full_text = " ".join(item["text"] for item in raw_list)
        return {"transcript": full_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# MCP 등록 (3줄)
mcp = FastApiMCP(app, name="Transcript MCP", description="Extract subtitles from YouTube videos")
mcp.mount()