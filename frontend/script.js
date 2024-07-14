async function transformImage(endpoint) {
    const uploadInput = document.getElementById('upload');
    if (uploadInput.files.length === 0) {
        alert("Please upload an image first.");
        return;
    }

    const formData = new FormData();
    formData.append('image', uploadInput.files[0]);

    let url = `http://127.0.0.1:8000/${endpoint}`;

    if (endpoint === 'resize') {
        url += '?width=200&height=200';
    } else if (endpoint === 'rotate') {
        url += '?angle=45';
    }

    const response = await fetch(url, {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        document.getElementById('output').src = url;
    } else {
        alert("An error occurred while processing the image.");
    }
}
