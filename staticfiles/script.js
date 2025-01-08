document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const bookingId = event.target.getAttribute('data-id');
            if (confirm("Are you sure you want to cancel this booking?")) {
                fetch(`/bookings/delete/${bookingId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        showToast(data.message, 'success');
                        location.reload();
                    } else {
                        showToast(data.error, 'danger');
                    }
                })
                .catch(error => {
                    showToast('Something went wrong!', 'danger');
                    console.error('Error:', error);
                });
            }
        });
    });
});

/**
 * Function to show a Bootstrap Toast.
 * @param {string} message - The message to display.
 * @param {string} type - The type of toast ('success', 'danger', etc.).
 */
function showToast(message, type) {
    const toastContainer = document.querySelector('.toast-container');

    const toastHTML = `
        <div class="toast align-items-center text-bg-${type} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);

    const newToast = toastContainer.lastElementChild;
    const bootstrapToast = new bootstrap.Toast(newToast);
    bootstrapToast.show();

    newToast.addEventListener('hidden.bs.toast', () => {
        newToast.remove();
    });
}
