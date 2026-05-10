# 🛰️ 災情分析地圖系統

基於 AI 的衛星圖片災情分析系統

## 🚀 部署到 Render

### 步驟 1：推送到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/disaster-analysis-map.git
git branch -M main
git push -u origin main
```

### 步驟 2：在 Render 部署

1. 前往 [Render Dashboard](https://dashboard.render.com)
2. 點擊 **"New +" → "Blueprint"**
3. 選擇你的 GitHub 倉庫
4. 點擊 **"Apply"**
5. 等待 3-5 分鐘部署完成

### 步驟 3：訪問網站

部署完成後訪問：
- 🌐 前端：`https://your-app.onrender.com/static/frontend/index.html`
- 📚 API 文檔：`https://your-app.onrender.com/docs`

## 💻 本地開發

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動服務
python main.py

# 訪問
# http://localhost:8000/static/frontend/index.html
```

## 📁 專案結構

```
├── main.py              # FastAPI 後端
├── frontend/
│   └── index.html      # 前端頁面
├── requirements.txt    # Python 依賴
├── render.yaml         # Render 配置
└── README.md
```

## 🎯 功能

- 📤 上傳衛星圖片
- 🤖 AI 災情分析
- 🗺️ Leaflet 地圖展示
- 📊 災情統計摘要
