
#uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

@app.post("/grayscale")
async def grayscale(image: UploadFile = File(...)):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data)).convert("L")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/resize")
async def resize(image: UploadFile = File(...), width: int = 100, height: int = 100):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data))
    img = img.resize((width, height))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/rotate")
async def rotate(image: UploadFile = File(...), angle: int = 90):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data))
    img = img.rotate(angle)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
