/**
 * main.js
 * 
 * Handles dynamic UI modifications, delete modal route injections,
 * and flash warning closures.
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Configure Dynamic Delete Confirmation Modal Action
    const deleteModal = document.getElementById("deleteConfirmModal");
    if (deleteModal) {
        deleteModal.addEventListener("show.bs.modal", (event) => {
            // Button that triggered the modal
            const button = event.relatedTarget;
            
            // Extract attributes from dataset parameters
            const studentId = button.getAttribute("data-student-id");
            const studentName = button.getAttribute("data-student-name");
            
            // Update the modal text details
            const detailsText = document.getElementById("delete-student-details");
            if (detailsText) {
                detailsText.textContent = `${studentName} (${studentId})`;
            }
            
            // Inject correct POST action path to the modal form
            const deleteForm = document.getElementById("delete-student-form");
            if (deleteForm) {
                deleteForm.action = `/students/delete/${studentId}`;
            }
        });
    }

    // 2. Automate Flash Dismissal Warnings
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach((alert) => {
        setTimeout(() => {
            const closeBtn = alert.querySelector(".btn-close");
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000); // 5 seconds fade out
    });
});
