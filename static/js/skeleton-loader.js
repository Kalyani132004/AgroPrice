/* ===========================================================
   AgroPrice — skeleton-loader.js
   Utility to show skeleton placeholders while async content loads.
=========================================================== */

function showSkeleton(containerId, count = 3) {
  const container = document.getElementById(containerId);
  if (!container) return;
  let html = "";
  for (let i = 0; i < count; i++) {
    html += `
      <div class="card-agro p-3 mb-3">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text" style="width: 70%;"></div>
      </div>`;
  }
  container.innerHTML = html;
}

function clearSkeleton(containerId) {
  const container = document.getElementById(containerId);
  if (container) container.innerHTML = "";
}
