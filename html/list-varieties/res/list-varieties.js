const base_url = "https://vps-68d3ea17.vps.ovh.net"; // Replace with your actual base URL
const get_varieties_url = `${base_url}/varieties`;
const new_photo_url = `${base_url}/varieties/upload-image`;

// Fetch varieties data and populate the dropdown
async function fetchVarieties() {
    try {
    const response = await fetch(get_varieties_url);
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const varieties = await response.json();

    const varietySelect = document.getElementById("variety-select");
    varietySelect.innerHTML =
        '<option value="" disabled selected>Select a variety</option>';

    varieties.forEach(variety => {
        const option = document.createElement("option");
        option.value = variety.name; // Assuming 'name' is unique
        option.textContent = variety.name;
        option.dataset.photoUrl = variety.photo_url;
        option.dataset.shortDescr = variety.short_descr;
        option.dataset.bloomingTime = variety.blooming_time_days;
        varietySelect.appendChild(option);
    });

    varietySelect.addEventListener("change", updateVarietyDetails);
    } catch (error) {
        console.error("Error fetching varieties:", error);
    }
}

// Update fields based on selected variety (drop box item change)
function updateVarietyDetails() {
    const selectedOption = this.options[this.selectedIndex];
    if (!selectedOption) return;

    const photoUrl = selectedOption.dataset.photoUrl || "placeholder.jpg";
    const shortDescr = selectedOption.dataset.shortDescr || "";
    const bloomingTime = selectedOption.dataset.bloomingTime || "";

    document.getElementById("photo-preview").src = photoUrl;
    document.getElementById("short-descr").value = shortDescr;
    document.getElementById("blooming-time").value = bloomingTime;
}

function switchEditMode(editMode) {
    const shortDescrField = document.getElementById("short-descr");
    const bloomingTimeField = document.getElementById("blooming-time");
    const photoPreview = document.getElementById("photo-preview-container");
    const photoDragContainer = document.getElementById("photo-drag-container");
    const removeButton = document.getElementById("remove-btn");
    const editButton = document.getElementById("edit-btn");
    const cancelButton = document.getElementById("cancel-btn");
    const submitButton = document.getElementById("submit-btn");

    if (editMode) {
        // Update form to Edit mode
        shortDescrField.removeAttribute("readonly");
        bloomingTimeField.removeAttribute("readonly");
        photoPreview.style.display = "none";
        photoDragContainer.style.display = "block";
        // Switch buttons
        removeButton.style.display = "none";
        editButton.style.display = "none";
        cancelButton.style.display = "block";
        submitButton.style.display = "block";
    } else {
        // Reset form to View mode
        shortDescrField.setAttribute("readonly", true);
        bloomingTimeField.setAttribute("readonly", true);
        photoPreview.style.display = "block";
        photoDragContainer.style.display = "none";
        // Reset buttons
        removeButton.style.display = "block";
        editButton.style.display = "block";
        cancelButton.style.display = "none";
        submitButton.style.display = "none";
    }
}

function onEditButtonClick(event) {
    event.preventDefault();
    switchEditMode(true);
}

function onCancelButtonClick(event) {
    event.preventDefault();
    switchEditMode(false);
}

function onSubmitButtonClick(event) {
    const shortDescrField = document.getElementById("short-descr");
    const bloomingTimeField = document.getElementById("blooming-time");
    const photoPreview = document.getElementById("photo-preview-container");
    const photoDragContainer = document.getElementById("photo-drag-container");
    const removeButton = document.getElementById("remove-btn");
    const editButton = document.getElementById("edit-btn");

    event.preventDefault();
    // Submit the form (you can replace this with an actual submission process)
    const shortDescrValue = document.getElementById("short-descr").value;
    const bloomingTimeValue = document.getElementById("blooming-time").value;
    const selectedFile = document.getElementById("photo-input").files[0];

    console.log("Short Description:", shortDescrValue);
    console.log("Blooming Time:", bloomingTimeValue);
    console.log("Selected Photo:", selectedFile);

    uploadFiles(selectedFile, new_photo_url, null, null);

    if (selectedFile) {
        const reader = new FileReader();
        reader.onload = function (e) {
            photoPreview.src = e.target.result; // Preview the image
        };
        reader.readAsDataURL(selectedFile);
    } else {
        photoPreview.src = ""; // Fallback if no image is selected
    }
}

function onRemoveButtonClick(event) {
    console.log('onRemoveButtonClick()"');
}

// Example function to handle the new variety name
function process_new_variety(varietyName) {
    console.log(`Processing new variety: ${varietyName}`);
    // Add your logic to save the new variety here (e.g., send to server)
}
function closePromptBox() {
    promptBox = document.getElementById("prompt-box");
    promptClose = document.getElementById("prompt-close");

    promptBox.parentNode.removeChild(promptBox);
    promptClose.parentNode.removeChild(promptClose);
}

function varietyPrompt(msg) {
    return new Promise((resolve, reject) => {
        // Create modal wrapper
        const modalWrapper = document.createElement("div");
        modalWrapper.id = "prompt-modal-wrapper";

        // Create modal content
        const modalBox = document.createElement("div");
        modalBox.id = "prompt-box";

        // Modal content
        modalBox.innerHTML = `
        <p style="margin-bottom: 20px;">${msg}</p>
        <input type="text" id="new-variety-name" name="new-variety-name" style="width: 90%; margin-top: 10px; padding: 8px;" /><br><br>
        <button id="prompt-ok" style="background: #28a745; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer;">OK</button>
        <button id="prompt-cancel" style="background: #dc3545; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; margin-left: 10px;">Cancel</button>
        `;

        // Append modal to the wrapper
        modalWrapper.appendChild(modalBox);
        document.body.appendChild(modalWrapper);

        // Handle OK button
        document.getElementById("prompt-ok").onclick = function () {
            const inputValue = document.getElementById("new-variety-name").value.trim();
            closePromptWindow(); // Clean up the modal
            resolve(inputValue); // Resolve the promise with the input value
        };

        // Handle Cancel button
        document.getElementById("prompt-cancel").onclick = function () {
            closePromptWindow(); // Clean up the modal
            resolve(null); // Resolve the promise with null (user cancelled)
        };

        // Close function
        function closePromptWindow() {
            if (modalWrapper) {
                document.body.removeChild(modalWrapper);
            }
        }
    });
};

function process_new_variety(name) {
  console.log(`Processing new variety: ${name}`);
  // Add your server call or logic here
}

// Initialize the page when fully loaded
document.addEventListener('DOMContentLoaded',
    () => {
        document.getElementById("edit-btn").addEventListener("click", onEditButtonClick);
        document.getElementById("submit-btn").addEventListener("click", onSubmitButtonClick);
        document.getElementById("remove-btn").addEventListener("click", onRemoveButtonClick);
        document.getElementById("cancel-btn").addEventListener("click", onCancelButtonClick);
        document.getElementById("add-variety-button").addEventListener("click", async () => {
            const newVarietyName = await window.prompt("Enter the new variety name:");
            if (newVarietyName) {
                console.log(`New variety name: ${newVarietyName}`);
                // Call your process_new_variety function here
                process_new_variety(newVarietyName);
            } else {
                console.log("User cancelled the prompt.");
            }
        });

        const photoInput = document.getElementById('photo-input');
        const dragArea = document.getElementById('photo-dragarea');
        const uploadPreview = document.getElementById('upload-preview');
        const fileInput = document.getElementById('photo-input');

        // Trigger file input when clicking the drag area
        dragArea.addEventListener('click', () => {
            photoInput.click();
        });

        dragArea.addEventListener('dragenter', event => {
            event.preventDefault();
            // dragArea.classList.add('highlight');
        });
        // Handle file input change
        photoInput.addEventListener('change', (event) => {
            handleFile(event.target.files[0]);
        });

        // Allow drag & drop functionality
        dragArea.addEventListener('dragover', (event) => {
            event.preventDefault();
            dragArea.style.backgroundColor = '#e6e6e6';
        });

        dragArea.addEventListener('dragleave', () => {
            dragArea.style.backgroundColor = '#f9f9f9';
            // dragArea.classList.remove('highlight');
        });

        dragArea.addEventListener('drop', (event) => {
            event.preventDefault();
            dragArea.style.backgroundColor = 'rgba(149, 157, 165, 0.65)';
            // dragArea.classList.remove('highlight');
            const file = event.dataTransfer.files[0];
            if (file) {
                // Update the file input's files property
                const dataTransfer2 = new DataTransfer();
                dataTransfer2.items.add(file);
                fileInput.files = dataTransfer2.files;
                // NOTE : no dataTransfer2, use dataTransfer's file directly ?
            }
            handleFile(file);
        });

        // Function to handle file selection and preview
        function handleFile(file) {
            if (file && (file.type === 'image/jpeg' || file.type === 'image/png')) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    uploadPreview.src = event.target.result;
                    uploadPreview.style.display = 'block'; // Show the preview
                };
                reader.readAsDataURL(file);
            } else {
                alert('Please upload a valid image file (JPEG or PNG).');
            }
        }

        window.prompt = varietyPrompt;
        // fetchVarieties();
    }
);
// }
