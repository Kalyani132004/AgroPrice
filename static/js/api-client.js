/* ===========================================================
   AgroPrice — api-client.js
   Single fetch() wrapper reused by every other JS module.
   Handles CSRF token injection + JSON parsing + error toasts.
=========================================================== */

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

const API_BASE = "/api/v1";

async function apiRequest(path, { method = "GET", body = null, isForm = false } = {}) {
  const headers = {};
  if (!isForm) headers["Content-Type"] = "application/json";
  const csrftoken = getCookie("csrftoken");
  if (csrftoken) headers["X-CSRFToken"] = csrftoken;

  try {
    const response = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      credentials: "same-origin",
      body: body ? (isForm ? body : JSON.stringify(body)) : null,
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      const message = data.error || data.detail || "Something went wrong. Please try again.";
      if (typeof showToast === "function") showToast(message, "error");
      return { ok: false, status: response.status, data };
    }
    return { ok: true, status: response.status, data };
  } catch (err) {
    if (typeof showToast === "function") showToast("Network error — please check your connection.", "error");
    return { ok: false, status: 0, data: {} };
  }
}

/* Convenience wrappers */
const AgroAPI = {
  getCrops: (q = "") => apiRequest(`/crops/${q ? "?q=" + encodeURIComponent(q) : ""}`),
  getCropDetail: (id) => apiRequest(`/crops/${id}/`),
  getTodayPrices: () => apiRequest("/prices/today/"),
  getPriceHistory: (crop, days = 30) => apiRequest(`/prices/history/?crop=${encodeURIComponent(crop)}&days=${days}`),
  searchPrices: (q) => apiRequest(`/prices/search/?q=${encodeURIComponent(q)}`),
  compareMarkets: (crop) => apiRequest(`/prices/compare/?crop=${encodeURIComponent(crop)}`),
  getTrend: (crop, days = 30) => apiRequest(`/analytics/trend/?crop=${encodeURIComponent(crop)}&days=${days}`),
  calculateProfit: (payload) => apiRequest("/analytics/profit/", { method: "POST", body: payload }),
};
