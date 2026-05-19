(() => {
  const applyBrand = () => {
    const brand = document.querySelector(".brand");
    if (!brand) return;
    brand.innerHTML = `
      <img class="brand-logo-img" src="logo.svg?v=5" alt="Chilean Surname Audit emblem">
      <span class="brand-text-wrap">
        <span class="brand-title-text">Chilean Surname Audit</span>
        <span class="brand-subtitle-text">LLM class bias study</span>
      </span>
    `;

    const style = document.createElement("style");
    style.textContent = `
      .brand { min-width: 310px !important; display: flex !important; align-items: center !important; justify-content: flex-start !important; gap: 14px !important; }
      .brand-logo-img { width: 68px !important; height: 68px !important; display: block !important; object-fit: contain !important; background: transparent !important; flex: 0 0 auto !important; }
      .brand-text-wrap { display: flex !important; flex-direction: column !important; gap: 2px !important; line-height: 1.05 !important; }
      .brand-title-text { font-family: Inter, system-ui, sans-serif !important; font-size: 20px !important; font-weight: 800 !important; letter-spacing: -0.04em !important; color: #171411 !important; white-space: nowrap !important; }
      .brand-subtitle-text { font-family: Inter, system-ui, sans-serif !important; font-size: 10px !important; font-weight: 800 !important; letter-spacing: 0.18em !important; text-transform: uppercase !important; color: #7d3c1f !important; white-space: nowrap !important; }
      @media (max-width: 900px) {
        .brand { min-width: 260px !important; gap: 10px !important; }
        .brand-logo-img { width: 56px !important; height: 56px !important; }
        .brand-title-text { font-size: 17px !important; }
        .brand-subtitle-text { font-size: 9px !important; letter-spacing: 0.14em !important; }
      }
      @media (max-width: 560px) {
        .brand { min-width: 0 !important; }
        .brand-title-text { font-size: 15px !important; }
        .brand-subtitle-text { display: none !important; }
      }
    `;
    document.head.appendChild(style);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyBrand);
  } else {
    applyBrand();
  }
})();
