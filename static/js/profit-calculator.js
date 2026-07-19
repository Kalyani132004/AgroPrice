/* ===========================================================
   AgroPrice — profit-calculator.js
   Live-updating preview + submit handling for the Revenue
   Calculator form.
=========================================================== */

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("profitCalculatorForm");
  if (!form) return;

  const previewEl = document.getElementById("livePreviewRevenue");
  const qtyInput = form.querySelector('[name="quantity"]');
  const priceInput = form.querySelector('[name="selling_price"]');

  function updatePreview() {
    if (!previewEl) return;
    const qty = parseFloat(qtyInput?.value || 0);
    const price = parseFloat(priceInput?.value || 0);
    const revenue = (qty * price) || 0;
    previewEl.textContent = `₹${revenue.toLocaleString("en-IN", { maximumFractionDigits: 2 })}`;
  }

  [qtyInput, priceInput].forEach((el) => el && el.addEventListener("input", updatePreview));
  updatePreview();

  form.addEventListener("submit", function () {
    toggleSpinner(true);
  });
});
