document.addEventListener("DOMContentLoaded", function () {
  // Theme switch logic
  const themeLinks = document.querySelectorAll(".theme-select");

  themeLinks.forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const selectedTheme = this.getAttribute("data-theme");

      // Set theme in Flask session
      fetch(`/set-theme/${selectedTheme}`, {
        method: "GET"
      }).then(() => {
        location.reload(); // Reload to apply new session theme
      });
    });
  });

  // Toggle visibility of "Delete Selected" form
  const checkboxes = document.querySelectorAll('.task-checkbox');
  const deleteSelectedForm = document.getElementById('deleteSelectedForm');
  const selectedTasksInput = document.getElementById('selectedTasksInput');

  if (checkboxes.length && deleteSelectedForm) {
    function toggleDeleteSelectedButton() {
      const selected = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);

      if (selected.length > 0) {
        deleteSelectedForm.classList.remove('d-none');
        selectedTasksInput.value = selected.join(',');
      } else {
        deleteSelectedForm.classList.add('d-none');
        selectedTasksInput.value = '';
      }
    }

    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', toggleDeleteSelectedButton);
    });

    // Initial check in case anything pre-checked
    toggleDeleteSelectedButton();
  }
});
