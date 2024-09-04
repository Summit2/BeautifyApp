package main

import (
	"bytes"
	"image"
	"image/png"
	"net/http"

	"github.com/disintegration/imaging"
	"github.com/gin-gonic/gin"
)

func applyLanczos(img image.Image) image.Image {
	return imaging.Resize(img, img.Bounds().Dx()*2, img.Bounds().Dy()*2, imaging.Lanczos)
}

func applyBicubic(img image.Image) image.Image {
	return imaging.Resize(img, img.Bounds().Dx()*2, img.Bounds().Dy()*2, imaging.CatmullRom)
}

func applyNearest(img image.Image) image.Image {
	return imaging.Resize(img, img.Bounds().Dx()*2, img.Bounds().Dy()*2, imaging.NearestNeighbor)
}

func processImage(c *gin.Context, transformFunc func(image.Image) image.Image) {
	file, _, err := c.Request.FormFile("image")
	if err != nil {
		c.String(http.StatusBadRequest, "No file part")
		return
	}

	img, _, err := image.Decode(file)
	if err != nil {
		c.String(http.StatusBadRequest, "Invalid image file")
		return
	}

	img = transformFunc(img)

	buf := new(bytes.Buffer)
	if err := png.Encode(buf, img); err != nil {
		c.String(http.StatusInternalServerError, "Failed to encode image")
		return
	}

	c.Data(http.StatusOK, "image/png", buf.Bytes())
}

func main() {
	r := gin.Default()

	r.POST("/lanczos", func(c *gin.Context) {
		processImage(c, applyLanczos)
	})

	r.POST("/bicubic", func(c *gin.Context) {
		processImage(c, applyBicubic)
	})

	r.POST("/nearest", func(c *gin.Context) {
		processImage(c, applyNearest)
	})

	r.Run("127.0.0.1:8000")
}
