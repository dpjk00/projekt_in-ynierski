// Function to attach event listener for image upload and preview
function attachFileInputListener(inputElement, previewElement) {
  inputElement.addEventListener('change', function(event) {
      const file = event.target.files[0];
      if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
              previewElement.style.backgroundImage = `url(${e.target.result})`;
              previewElement.innerHTML = '';  // Remove "Click to Add Image" text
          };
          reader.readAsDataURL(file);
      }
  });

  // Add click event to the preview to trigger file selection
  previewElement.addEventListener('click', function() {
      inputElement.click();
  });
}

// Attach listener to the input field on document load
document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('id_image');
  const preview = document.getElementById('image-preview');
  attachFileInputListener(input, preview);

  // Handle form submission via AJAX
  const form = document.getElementById('image-upload-form');
  form.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent default form submission
      const formData = new FormData(form);

      fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
          }
      })
      .then(response => response.json())
      .then(data => {
          // If the upload was successful, update the image preview
          if (data.success) {
              const img = document.createElement('img');
              img.src = data.image_url; // Assuming the server returns the image URL
              img.width = 100;
              img.height = 100;
              document.getElementById('uploaded-images').appendChild(img);
              // Reset the input for the next upload
              form.reset();
              preview.style.backgroundImage = ''; // Reset preview
              preview.innerHTML = '<span>Click to Add Image</span>'; // Reset text
          } else {
              alert('Image upload failed.');
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
  });
});
