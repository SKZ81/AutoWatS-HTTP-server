function updateStatusMessage(status, message) {
  if (status != null)
      status.textContent = message;
}

function updateProgressBar(progressBar, value) {
  const percent = value * 100;
  if (progressBar != null)
      progressBar.value = Math.round(percent);
}

function uploadFiles(files, url, status, progressBar) {
    const method = 'POST';
    const fileInput = document.getElementById('photo-input');
    const file = fileInput.files[0];
    const xhr = new XMLHttpRequest();
    const data = new FormData();

    data.append('photo', file); // 'photo' is the key for the file
    data.append('filename', file.name); // 'filename' is the key for the file name

    xhr.upload.addEventListener('progress', event => {
        updateStatusMessage(status, `⏳ Uploaded ${event.loaded} bytes of ${event.total}`);
        updateProgressBar(progressBar, event.loaded / event.total);
    });
    xhr.addEventListener('loaded', () => {
        if (xhr.status === 200) {
            updateStatusMessage(status, '✅ Success');
            // renderFilesMetadata(fileInput.files);
        } else {
            updateStatusMessage('❌ Error');
        }

        updateProgressBar(0);
    });

    xhr.open(method, url);
    xhr.send(data);
}
