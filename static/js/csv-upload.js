/* ===========================================================
   AgroPrice — csv-upload.js
   Admin CSV upload UX: filename preview + submit spinner.
=========================================================== */

document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("csvFileInput");
  const fileNameLabel = document.getElementById("csvFileName");
  const uploadForm = document.getElementById("csvUploadForm");

  if (fileInput && fileNameLabel) {
    fileInput.addEventListener("change", function () {
      fileNameLabel.textContent = this.files.length
        ? this.files[0].name
        : "No file chosen";
    });
  }

  if (uploadForm) {
    uploadForm.addEventListener("submit", function () {
      toggleSpinner(true);
    });
  }
});
