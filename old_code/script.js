// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();

    const targetId = this.getAttribute("href").substring(1);
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
      window.scrollTo({
        top: targetElement.offsetTop - 10, // Adjust for header height
        behavior: "smooth",
      });
    }
  });
});

// JavaScript (script.js)
document.addEventListener("DOMContentLoaded", function () {
  const imageInput = document.getElementById("imageInput");
  const openCameraButton = document.getElementById("openCameraButton");
  const cameraModal = document.getElementById("cameraModal");
  const cameraFeed = document.getElementById("cameraFeed");
  const takePictureButton = document.getElementById("takePictureButton");
  const capturedImage = document.getElementById("capturedImage");

  // Hide the camera modal by default
  cameraModal.style.display = "none";

  // Function to handle image input change
  imageInput.addEventListener("change", function () {
    const file = imageInput.files[0];
    if (file) {
      const imageURL = URL.createObjectURL(file);
      capturedImage.src = imageURL;
    }
  });

  // Function to open the camera modal
  openCameraButton.addEventListener("click", function () {
    // Show the camera modal
    cameraModal.style.display = "block";

    // Access the device camera and show the feed
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (stream) {
        cameraFeed.srcObject = stream;
      })
      .catch(function (err) {
        console.error("Error accessing camera:", err);
        cameraModal.style.display = "none"; // Hide modal on error
      });
  });

  // Function to capture an image from the camera
  takePictureButton.addEventListener("click", function () {
    // Create a canvas for capturing the image
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    canvas.width = 400; // Adjust width as needed
    canvas.height = 500; // Adjust height as needed
    context.drawImage(cameraFeed, 0, 0, canvas.width, canvas.height);

    // Display the captured image
    const imageURL = canvas.toDataURL("image/jpeg");
    capturedImage.src = imageURL;

    // Hide the camera modal
    cameraModal.style.display = "none";

    // Stop the camera feed
    cameraFeed.srcObject.getTracks().forEach((track) => track.stop());
  });
});
