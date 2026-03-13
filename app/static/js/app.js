window.renderLineChart = function(id, cfg) {
  const el = document.getElementById(id);
  if (!el) return;
  new Chart(el, {
    type: 'line',
    data: {
      labels: cfg.labels,
      datasets: cfg.series.map((s, idx) => ({
        label: s.label,
        data: s.data,
        tension: 0.35,
        fill: false,
        borderWidth: 2
      }))
    },
    options: { responsive: true, maintainAspectRatio: false }
  });
};
window.renderBarChart = function(id, cfg) {
  const el = document.getElementById(id);
  if (!el) return;
  new Chart(el, {
    type: 'bar',
    data: {
      labels: cfg.labels,
      datasets: [{ label: cfg.label, data: cfg.values, borderWidth: 1 }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });
};
