from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Satellite AI is running 🚀"}
