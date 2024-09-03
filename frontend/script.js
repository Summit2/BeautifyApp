async function transformImages() {
    const uploadInput = document.getElementById('upload');
    if (uploadInput.files.length === 0) {
        alert("Please upload an image first.");
        return;
    }

    await Promise.all([
        transformImage('bicubic', 'bicubicOutput'),
        transformImage('lanczos', 'lanczosOutput'),
        transformImage('nearest', 'nearestOutput')
    ]);
}

async function transformImage(endpoint, outputElementId) {
    const url = `http://127.0.0.1:8000/${endpoint}/`; // Ensure trailing slash
    const formData = new FormData();
    formData.append('image', document.getElementById('upload').files[0]);

    const response = await fetch(url, {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const blob = await response.blob();
        const imgUrl = URL.createObjectURL(blob);
        document.getElementById(outputElementId).src = imgUrl;

        const downloadButtonId = outputElementId + 'Download';
        document.getElementById(downloadButtonId).style.display = 'inline-block';
        document.getElementById(downloadButtonId).href = imgUrl;
        document.getElementById(downloadButtonId).download = `${outputElementId}.png`;
    } else {
        alert("An error occurred while processing the image.");
    }
}

function downloadImage(outputElementId) {
    const imgElement = document.getElementById(outputElementId);
    const link = document.createElement('a');
    link.href = imgElement.src;
    link.download = `${outputElementId}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
