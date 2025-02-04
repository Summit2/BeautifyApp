from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

app = FastAPI()

def apply_lanczos(img):
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)
    return img

def apply_bicubic(img):
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return img

def apply_nearest(img):
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    return img

def process_image(file, transform_func):
    try:
        
        img = Image.open(file.file)
        img_array = np.array(img)

        img_transformed = transform_func(img_array)
        img_transformed_pil = Image.fromarray(img_transformed)
        
        
        img_stream = BytesIO()
        img_transformed_pil.save(img_stream, format="PNG")
        img_stream.seek(0)
        
        return StreamingResponse(img_stream, media_type="image/png")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process image")

@app.post("/lanczos/")
async def lanczos_transform(file: UploadFile = File(...)):
    return process_image(file, apply_lanczos)

@app.post("/bicubic/")
async def bicubic_transform(file: UploadFile = File(...)):
    return process_image(file, apply_bicubic)

@app.post("/nearest/")
async def nearest_transform(file: UploadFile = File(...)):
    return process_image(file, apply_nearest)
