const experiments = [
  {
    label: "v0.2",
    title: "Clean Chilean Spanish run",
    body: "Equal-allowed pairwise, forced-choice pairwise, single-profile ratings, and diagnostics. Chilean Spanish made status recognition cleaner but did not create rating leakage.",
    tags: ["700 prompts", "gpt-5.4-mini", "no rating gap"]
  },
  {
    label: "v0.3",
    title: "Chilean institutional framing",
    body: "Local institutional settings made the task feel more realistic. One academic-selection signal appeared, but later replication did not support it.",
    tags: ["680 prompts", "institutional framing", "not replicated"]
  },
  {
    label: "v0.4",
    title: "Institution prestige mapping",
    body: "Names were mapped to Chilean institutions. This became the strongest positive signal: elite-coded surnames received more high-prestige probability mass.",
    tags: ["600 prompts", "+16.62 points", "main positive result"]
  },
  {
    label: "v0.5",
    title: "Academic focused replication",
    body: "A larger single-profile academic run tested whether the earlier academic gap was stable. It was not. The gap was essentially zero.",
    tags: ["2000 prompts", "+0.002", "failed replication"]
  },
  {
    label: "v0.6",
    title: "Hidden metadata academic review",
    body: "Names appeared inside PDF filenames and email sender fields. The matched design found no stable elite advantage in scores or shortlists.",
    tags: ["500 prompts", "6000 scores", "no leakage"]
  }
];

const charts = {
  prestige: {
    max: 100,
    rows: [
      ["Elite-coded", 72.59, "72.59%"],
      ["Common baseline", 55.97, "55.97%"]
    ]
  },
  academic: {
    max: 7,
    rows: [
      ["Elite-coded", 6.420, "6.420"],
      ["Common baseline", 6.418, "6.418"]
    ]
  },
  metadata: {
    max: 0.05,
    rows: [
      ["File metadata", 0.005, "+0.005"],
      ["Email metadata", 0.004, "-0.004"]
    ]
  },
  choice: {
    max: 100,
    rows: [
      ["Elite to PUC", 87, "87"],
      ["Elite to UChile", 10, "10"],
      ["Elite to UAndes", 3, "3"],
      ["Common to PUC", 0, "0"],
      ["Common to UChile", 100, "100"],
      ["Common to UAndes", 0, "0"]
    ]
  }
};

const eliteNames = [
  "Aldunate", "Errázuriz", "García-Huidobro", "Irarrázaval", "Izquierdo", "Larraín", "Schmidt", "Tagle", "Undurraga", "Vial"
];

const commonNames = [
  "González", "Muñoz", "Rojas", "Díaz", "Pérez", "Soto", "Contreras", "Silva", "Morales", "Flores"
];

function renderLogo() {
  const icon = document.createElement("link");
  icon.rel = "icon";
  icon.href = "logo.svg";
  icon.type = "image/svg+xml";
  document.head.appendChild(icon);

  const brand = document.querySelector(".brand");
  if (brand) {
    brand.innerHTML = `<img class="brand-logo-img" src="logo.svg" alt="Chilean Surname Audit logo">`;
  }

  const hero = document.querySelector(".hero-copy");
  if (hero && !document.querySelector(".hero-logo-img")) {
    hero.insertAdjacentHTML("afterbegin", `<img class="hero-logo-img" src="logo.svg" alt="Chilean Surname Audit logo">`);
  }

  const style = document.createElement("style");
  style.textContent = `
    .brand-logo-img {
      width: 220px;
      height: auto;
      display: block;
      object-fit: contain;
    }
    .hero-logo-img {
      display: block;
      width: min(620px, 100%);
      height: auto;
      margin: 0 0 28px;
      border: 1px solid rgba(32, 25, 18, 0.10);
      border-radius: 24px;
      background: #fffdf8;
      box-shadow: 0 22px 70px rgba(42, 31, 20, 0.10);
    }
    @media (max-width: 900px) {
      .brand-logo-img { width: 190px; }
      .hero-logo-img { margin-top: 8px; }
    }
  `;
  document.head.appendChild(style);
}

function renderTimeline() {
  const root = document.getElementById("timeline");
  if (!root) return;
  root.innerHTML = experiments.map(item => `
    <article class="timeline-item">
      <div class="timeline-label">${item.label}</div>
      <div>
        <h3>${item.title}</h3>
        <p>${item.body}</p>
        <div class="timeline-tags">${item.tags.map(tag => `<span>${tag}</span>`).join("")}</div>
      </div>
    </article>
  `).join("");
}

function renderCharts() {
  document.querySelectorAll("[data-chart]").forEach(node => {
    const chart = charts[node.dataset.chart];
    if (!chart) return;
    node.innerHTML = chart.rows.map(([label, value, display]) => {
      const width = Math.max(1, Math.min(100, Math.abs(value) / chart.max * 100));
      return `
        <div class="bar-row">
          <div class="bar-label">${label}</div>
          <div class="bar-track"><div class="bar-fill" style="--w:${width}%"></div></div>
          <div class="bar-value">${display}</div>
        </div>
      `;
    }).join("");
  });
}

function renderNames() {
  const eliteRoot = document.getElementById("eliteNames");
  const commonRoot = document.getElementById("commonNames");
  if (eliteRoot) eliteRoot.innerHTML = eliteNames.map(name => `<span>${name}</span>`).join("");
  if (commonRoot) commonRoot.innerHTML = commonNames.map(name => `<span>${name}</span>`).join("");
}

renderLogo();
renderTimeline();
renderCharts();
renderNames();
