document.addEventListener("DOMContentLoaded", function () {
  // mobile menu toggle
  var toggle = document.getElementById("navToggle");
  var menu = document.getElementById("navMenu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      menu.classList.toggle("open");
    });
  }

  // Automatically hide alert messages after 5 seconds
  document.querySelectorAll(".alert[data-autohide]").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity .5s";
      el.style.opacity = "0";
      setTimeout(function () { el.remove(); }, 500);
    }, 5000);
  });

  // Ask for confirmation before submitting any form that has a data-confirm attribute
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm(form.getAttribute("data-confirm"))) {
        e.preventDefault();
      }
    });
  });
});
