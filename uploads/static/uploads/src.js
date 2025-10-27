// Elements
const fileInput = document.getElementById('fileInput');
const customUploadBtn = document.getElementById('customUploadBtn');
const initError = document.getElementById('initUploadError');

const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg']; // Acceptable file types

// Event listeners
customUploadBtn.addEventListener('click', () => {
    fileInput.click(); // trigger file upload
});

fileInput.addEventListener('change', () => {
    const file = fileInput.files[0]; // Set singular file

    if (!file) return;

    if (!allowedTypes.includes(file.type)) {
        initError.style.opacity = 1
        fileInput.value = ''; // Clear the input
        console.log("We can't use this file sorry");
        return;
    }

    // ✅ Valid file — proceed to next screen
    initError.style.opacity = 0
    console.log("Acceptable");
});
