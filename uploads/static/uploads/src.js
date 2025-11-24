console.log("Alive!");

fetch('../../static/uploads/mockData.json') // Fetch mock data to use locally until we can connect to backend
  .then(res => res.json())
  .then(data => {
    console.log(data);
  })
  .catch(err => console.error("Error loading mock data:", err));

// Elements
const fileInput = document.getElementById('fileInput');
const customUploadBtn = document.getElementById('customUploadBtn');
const initError = document.getElementById('initUploadError');

const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg']; // Acceptable file types

// Upload Card
customUploadBtn.addEventListener('click', () => {
    fileInput.click(); // trigger file upload
});

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];

    if (!file) return;

    if (!allowedTypes.includes(file.type)) {
        initError.style.opacity = 1;
        fileInput.value = '';
        console.log("We can't use this file sorry");
        return;
    }

    initError.style.opacity = 0;
    console.log("Acceptable");

    const previewURL = URL.createObjectURL(file);
    const previewArea = document.getElementById('upload-prev-right')

    document.getElementById('filenamedis').textContent = `Uploaded File: ${file.name}`;
    
    if (file.type.startsWith('image/')) {
        previewArea.innerHTML = `<img src="${previewURL}" alt="Preview" style="max-width:100%; max-height:100%;">`;
    } else if (file.type === 'application/pdf') {
        previewArea.innerHTML = `<iframe src="${previewURL}" width="100%" height="100%"></iframe>`;
    } else {
        previewArea.innerHTML = `<p>Preview not available.</p>`;
    }

    showFilePreview();
});

// Upload Preview
let changeFile = document.getElementById('changefile');
const previewContainer = document.getElementById('upload-prev');

function showFilePreview() {
    previewContainer.style.display = 'flex';
    document.getElementById('upload-card').style.display = 'none';
}
changeFile.addEventListener('click', () => {
    document.getElementById('upload-card').style.display = 'flex';
    previewContainer.style.display = 'none';
    URL.revokeObjectURL(previewURL);
});