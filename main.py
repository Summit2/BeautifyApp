from fastapi import FastAPI

app = FastAPI()

input

@app.post("/app/srgan")
async def srgan(input_image):
    return



@app.post("/app/waifu2x")
async def waifu2x(input_image):
    return



@app.post("/app/lanczos")
async def lanczos(input_image):
    return