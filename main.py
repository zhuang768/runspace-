from fastapi import FastAPI, File, UploadFile
import requests
import os

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")

@app.get("/")
def home():
    return {"service":"AI Backend","version":"1.0.0","status":"running"}


def call_ai_model(image_bytes):
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    
    response = requests.post(
        API_URL,
        headers=headers,
        data=image_bytes
    )
    
    return response.json()


# ⭐ 這個就是 upload endpoint
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = call_ai_model(image_bytes)
    return result            "description": f"AI 檢測到{disaster['type']}區域",
            "confidence": round(random.uniform(0.75, 0.98), 2)
        })
    
    return disasters


# ==================== API 端點 ====================

@app.get("/")
async def root():
    """根路徑"""
    return {
        "service": "災情分析 AI Backend",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/api/analyze")
async def analyze_disaster(file: UploadFile = File(...)):
    """分析衛星圖片中的災情"""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="請上傳圖片文件")
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # AI 分析
        disasters = simulate_ai_analysis(image.size[0], image.size[1])
        
        summary = {
            "total": len(disasters),
            "high_severity": len([d for d in disasters if d["severity"] == "高"]),
            "medium_severity": len([d for d in disasters if d["severity"] == "中"]),
            "low_severity": len([d for d in disasters if d["severity"] == "低"])
        }
        
        return JSONResponse({
            "success": True,
            "message": "AI 分析完成",
            "image_info": {
                "filename": file.filename,
                "size": f"{image.size[0]}x{image.size[1]}",
                "format": image.format or "Unknown"
            },
            "disasters": disasters,
            "summary": summary
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失敗: {str(e)}")


@app.get("/api/health")
async def health_check():
    """健康檢查"""
    return {"status": "healthy", "service": "災情分析 AI Backend"}

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
