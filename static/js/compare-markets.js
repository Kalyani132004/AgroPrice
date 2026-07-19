/* ===========================================================
   AgroPrice — compare-markets.js
=========================================================== */

document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("compareCropSelect");
  if (!select) return;

  select.addEventListener("change", function () {
    const crop = this.value;
    if (!crop) return;
    const url = new URL(window.location.href);
    url.searchParams.set("crop", crop);
    window.location.href = url.toString();
  });
});
