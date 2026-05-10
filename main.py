from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import random
from PIL import Image
import io
from typing import List, Dict

app = FastAPI(
    title="災情分析 AI Backend",
    description="接收衛星圖片，使用 AI 分析災情",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 提供靜態文件服務（前端）
app.mount("/static", StaticFiles(directory="."), name="static")


def simulate_ai_analysis(width: int, height: int) -> List[Dict]:
    """模擬 AI 災情檢測"""
    disaster_types = [
        {"type": "火災", "severity": "高", "icon": "🔥", "color": "#e53935"},
        {"type": "水災", "severity": "中", "icon": "🌊", "color": "#1e88e5"},
        {"type": "建築損毀", "severity": "高", "icon": "🏚️", "color": "#d32f2f"},
        {"type": "道路阻斷", "severity": "中", "icon": "🚧", "color": "#f57c00"},
        {"type": "土石流", "severity": "高", "icon": "⛰️", "color": "#6d4c41"},
        {"type": "植被破壞", "severity": "低", "icon": "🌳", "color": "#689f38"},
    ]
    
    num_disasters = random.randint(4, 10)
    disasters = []
    lat_range = (23.5, 24.5)
    lon_range = (120.5, 121.5)
    
    for i in range(num_disasters):
        disaster = random.choice(disaster_types)
        disasters.append({
            "id": i + 1,
            "lat": round(random.uniform(*lat_range), 6),
            "lon": round(random.uniform(*lon_range), 6),
            "type": disaster["type"],
            "severity": disaster["severity"],
            "icon": disaster["icon"],
            "color": disaster["color"],
            "description": f"AI 檢測到{disaster['type']}區域",
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
