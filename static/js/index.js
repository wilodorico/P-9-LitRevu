document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll("#alert-message");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.remove("opacity-100");
      alert.classList.add("opacity-0", "-translate-y-4"); // Opacité à 0 et montée vers le haut
      setTimeout(() => {
        alert.remove(); // Supprimer l'alerte du DOM après la transition
      }, 300); // Attendre que la transition se termine avant de supprimer l'élément
    }, 3000); // Délai de 3 secondes avant de commencer la disparition
  });
});
