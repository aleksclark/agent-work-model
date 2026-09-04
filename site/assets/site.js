(function () {
  const root = document.documentElement;
  const stored = window.localStorage.getItem("awm-theme");
  if (stored === "light" || stored === "dark") {
    root.setAttribute("data-theme", stored);
  }

  function currentTheme() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function setTheme(theme) {
    root.setAttribute("data-theme", theme);
    window.localStorage.setItem("awm-theme", theme);
    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      const next = theme === "light" ? "dark" : "light";
      button.setAttribute("aria-label", "Switch to " + next + " mode");
    });
  }

  document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      setTheme(currentTheme() === "dark" ? "light" : "dark");
    });
  });
  setTheme(currentTheme());

  const nav = document.querySelector("[data-site-nav]");
  const backdrop = document.querySelector("[data-nav-backdrop]");
  const menuButtons = document.querySelectorAll("[data-nav-toggle]");
  const openButton = document.querySelector(".site-menu");
  const closeButton = document.querySelector(".site-nav-close");

  function setNav(open) {
    if (!nav) return;
    nav.classList.toggle("is-open", open);
    document.body.classList.toggle("site-nav-open", open);
    if (backdrop) backdrop.classList.toggle("is-open", open);
    menuButtons.forEach(function (button) {
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });
    window.requestAnimationFrame(function () {
      if (open && closeButton) closeButton.focus();
      if (!open && openButton) openButton.focus();
    });
  }

  menuButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      setNav(!nav.classList.contains("is-open"));
    });
  });
  if (backdrop) {
    backdrop.addEventListener("click", function () {
      setNav(false);
    });
  }
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") setNav(false);
  });

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      const value = button.getAttribute("data-copy") || "";
      if (!navigator.clipboard) return;
      navigator.clipboard.writeText(value).then(function () {
        const previous = button.getAttribute("data-label") || button.textContent;
        button.textContent = "Copied";
        window.setTimeout(function () {
          button.textContent = previous;
        }, 1200);
      });
    });
  });
})();
