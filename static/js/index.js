function closeAlert(button) {
  let alertBox = button.closest(".alert-message");
  if (alertBox) {
    alertBox.classList.remove("opacity-100");
    alertBox.classList.add("opacity-0", "-translate-y-4"); // Transition douce
    setTimeout(() => alertBox.remove(), 300); // Suppression après animation
  }
}

function autoDismissAlerts() {
  document.querySelectorAll(".alert-message").forEach((alert) => {
    setTimeout(() => {
      alert.classList.remove("opacity-100");
      alert.classList.add("opacity-0", "-translate-y-4");
      setTimeout(() => alert.remove(), 300);
    }, 3000); // Attendre 3 secondes avant disparition
  });
}

// S'assurer que HTMX recharge bien les messages
document.body.addEventListener("htmx:afterSwap", () => {
  setTimeout(autoDismissAlerts, 100); // Laisser HTMX injecter avant d'exécuter
});

// Exécuter au chargement initial
document.addEventListener("DOMContentLoaded", autoDismissAlerts);
