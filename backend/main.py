from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io

app = FastAPI()

def apply_lanczos(img: Image.Image) -> Image.Image:
    return img.resize((img.width * 2, img.height * 2), Image.LANCZOS)

def apply_bicubic(img: Image.Image) -> Image.Image:
    return img.resize((img.width * 2, img.height * 2), Image.BICUBIC)

def apply_nearest(img: Image.Image) -> Image.Image:
    return img.resize((img.width * 2, img.height * 2), Image.NEAREST)

@app.post("/lanczos/")
async def lanczos_endpoint(image: UploadFile = File(...)):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data))
    img = apply_lanczos(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/bicubic/")
async def bicubic_endpoint(image: UploadFile = File(...)):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data))
    img = apply_bicubic(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/nearest/")
async def nearest_endpoint(image: UploadFile = File(...)):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data))
    img = apply_nearest(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
