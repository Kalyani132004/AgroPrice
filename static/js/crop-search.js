/* ===========================================================
   AgroPrice — crop-search.js
   Live crop search (navbar + crop list page) with debounce.
=========================================================== */

document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("cropSearchInput");
  const resultsBox = document.getElementById("cropSearchResults");
  if (!input || !resultsBox) return;

  const runSearch = debounce(async function () {
    const query = input.value.trim();
    if (query.length < 2) {
      resultsBox.innerHTML = "";
      resultsBox.classList.add("d-none");
      return;
    }

    resultsBox.classList.remove("d-none");
    resultsBox.innerHTML = `<div class="p-3"><span class="spinner-agro"></span> Searching...</div>`;

    const res = await AgroAPI.searchPrices(query);
    if (!res.ok || !res.data.results || res.data.results.length === 0) {
      resultsBox.innerHTML = `<div class="p-3 text-muted-soft small">No crops found for "${query}"</div>`;
      return;
    }

    resultsBox.innerHTML = res.data.results
      .map(
        (crop) => `
        <a href="/crops/${crop.id}/" class="d-block px-3 py-2 text-decoration-none text-dark border-bottom">
          <strong>${crop.name}</strong>
          <span class="text-muted-soft small ms-2">${crop.category}</span>
        </a>`
      )
      .join("");
  }, 300);

  input.addEventListener("input", runSearch);
  document.addEventListener("click", (e) => {
    if (!resultsBox.contains(e.target) && e.target !== input) {
      resultsBox.classList.add("d-none");
    }
  });
});
