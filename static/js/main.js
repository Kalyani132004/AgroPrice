/* ===========================================================
   AgroPrice — main.js
   Shared UI behavior: navbar scroll shadow, toast helper,
   loading spinner helper, mobile nav.
=========================================================== */

document.addEventListener("DOMContentLoaded", function () {
  // Sticky navbar shadow on scroll
  const navbar = document.querySelector(".navbar-agro");
  if (navbar) {
    window.addEventListener("scroll", function () {
      navbar.classList.toggle("scrolled", window.scrollY > 8);
    });
  }

  // Auto-init any Bootstrap tooltips
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggerList.forEach((el) => new bootstrap.Tooltip(el));

  // Auto-dismiss Django messages rendered as toasts
  document.querySelectorAll(".toast-agro").forEach((el) => {
    const toast = new bootstrap.Toast(el, { delay: 4000 });
    toast.show();
  });
});

/** Show a Bootstrap toast dynamically (used by JS-driven interactions). */
function showToast(message, type = "success") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const bg = { success: "bg-success", error: "bg-danger", info: "bg-info", warning: "bg-warning" }[type] || "bg-success";
  const toastEl = document.createElement("div");
  toastEl.className = `toast toast-agro align-items-center text-white ${bg} border-0`;
  toastEl.setAttribute("role", "alert");
  toastEl.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>`;
  container.appendChild(toastEl);
  const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
  toast.show();
  toastEl.addEventListener("hidden.bs.toast", () => toastEl.remove());
}

/** Toggle the full-page loading spinner overlay. */
function toggleSpinner(show) {
  const overlay = document.getElementById("spinnerOverlay");
  if (overlay) overlay.classList.toggle("active", show);
}

/** Simple debounce helper used by live search inputs. */
function debounce(fn, delay = 350) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
