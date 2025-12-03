console.log("Alive!");

fetch('../../static/uploads/mockData.json')
  .then(res => res.json())
  .then(data => {
    console.log(data);
  })
  .catch(err => console.error("Error loading mock data:", err));

// Elements
const fileInput = document.getElementById('fileInput');
const customUploadBtn = document.getElementById('customUploadBtn');
const initError = document.getElementById('initUploadError');

const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg'];

let selectedFile = null;   // <--- define early

// Upload Card
customUploadBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    selectedFile = file;  // <--- add this

    if (!file) return;

    if (!allowedTypes.includes(file.type)) {
        initError.style.opacity = 1;
        fileInput.value = '';
        return;
    }

    initError.style.opacity = 0;

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

/*
// --- Original frontend team code disabled ---
// This refers to previewURL which is out of scope and causes errors.
changeFile.addEventListener('click', () => {
    document.getElementById('upload-card').style.display = 'flex';
    previewContainer.style.display = 'none';
    URL.revokeObjectURL(previewURL);
});
*/

// BACKEND-INTEGRATION — Upload file + redirect
// --- FIXED CHANGE-FILE BUTTON FUNCTIONALITY ---
changeFile.addEventListener('click', () => {

    console.log("CHANGE FILE CLICKED!");
    
    // Hide preview card
    previewContainer.style.display = 'none';

    // Show original upload card
    document.getElementById('upload-card').style.display = 'flex';

    // Reset file input
    fileInput.value = "";
    selectedFile = null;

    // Clear preview area
    document.getElementById('upload-prev-right').innerHTML = "";

    // Reset filename display
    document.getElementById('filenamedis').textContent = "Filename";

    console.log("Ready for a new file.");
});



const continueBtn = document.querySelector('#upload-prev-left button:nth-of-type(2)');

continueBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        alert("No file selected!");
        return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch("/uploads/process/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCSRFToken()
            }
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = `/uploads/summary/${data.file_id}/`;
        } else {
            alert(data.error || "Upload failed");
        }

    } catch (err) {
        console.error(err);
        alert("Error connecting to server");
    }
});

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith('csrftoken=')) {
            return cookie.substring('csrftoken='.length);
        }
    }
    return "";
}
