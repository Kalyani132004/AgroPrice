/* ===========================================================
   AgroPrice — charts.js
   Reusable Chart.js initializers (line/bar/pie) themed to the
   agri-green palette. Call these from page-specific templates.
=========================================================== */

const CHART_COLORS = {
  primary: "#2E7D32",
  secondary: "#66BB6A",
  accent: "#FFC107",
  grid: "#E3E9E1",
  text: "#6B7A70",
};

const PIE_PALETTE = ["#2E7D32", "#66BB6A", "#FFC107", "#0288D1", "#8D6E63", "#AB47BC", "#EF5350", "#26A69A"];

function baseChartOptions(extra = {}) {
  return Object.assign(
    {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: CHART_COLORS.text, font: { family: "Inter" } } },
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: CHART_COLORS.text } },
        y: { grid: { color: CHART_COLORS.grid }, ticks: { color: CHART_COLORS.text } },
      },
    },
    extra
  );
}

function renderLineChart(canvasId, labels, data, label = "Price (₹)") {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label,
          data,
          borderColor: CHART_COLORS.primary,
          backgroundColor: "rgba(46,125,50,0.08)",
          tension: 0.35,
          fill: true,
          pointRadius: 3,
          pointBackgroundColor: CHART_COLORS.secondary,
        },
      ],
    },
    options: baseChartOptions(),
  });
}

function renderBarChart(canvasId, labels, data, label = "Count") {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label,
          data,
          backgroundColor: CHART_COLORS.secondary,
          borderRadius: 6,
          maxBarThickness: 42,
        },
      ],
    },
    options: baseChartOptions({ plugins: { legend: { display: false } } }),
  });
}

function renderPieChart(canvasId, labels, data) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  return new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [{ data, backgroundColor: PIE_PALETTE, borderWidth: 2, borderColor: "#fff" }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: "bottom", labels: { color: CHART_COLORS.text, boxWidth: 12 } } },
    },
  });
}
