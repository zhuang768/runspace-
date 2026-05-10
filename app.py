from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import torch
from torchvision import models, transforms

app = FastAPI()

# 載入預訓練模型（啟動時只做一次）
model = models.resnet18(pretrained=True)
model.eval()

# ImageNet 前處理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# ImageNet 標籤
labels = open("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt").read().splitlines()

@app.get("/")
def home():
    return {"message": "Satellite AI running with REAL model 🚀"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    img_t = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img_t)
        _, predicted = outputs.max(1)
        label = labels[predicted.item()]

    return {
        "filename": file.filename,
        "prediction": label
    }
