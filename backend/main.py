
#uvicorn main:app --reload

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image, ImageFilter
import io

app = FastAPI()

# Placeholder transformations for demonstration purposes
def apply_waifu2x(img: Image.Image) -> Image.Image:
    # Placeholder for waifu2x logic
    return img.filter(ImageFilter.SMOOTH)

def apply_lanczos(img: Image.Image) -> Image.Image:
    return img.resize((img.width * 2, img.height * 2), Image.LANCZOS)

def apply_srgan(img: Image.Image) -> Image.Image:
    # Placeholder for SRGAN logic
    return img.resize(img.width * 0,1, img.height * 2)

@app.post("/waifu2x/")
async def waifu2x(image: UploadFile = File(...)):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data))
    img = apply_waifu2x(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/lanczos/")
async def lanczos(image: UploadFile = File(...)):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data))
    print(img)
    img = apply_lanczos(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/srgan/")
async def srgan(image: UploadFile = File(...)):
    image_data = await image.read()
    img = Image.open(io.BytesIO(image_data))
    img = apply_srgan(img)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
