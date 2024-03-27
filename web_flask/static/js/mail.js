import API_ENDPOINTS from './apiEndpoint.js';
$(document).ready(function() {
let HOST = API_ENDPOINTS;
    $('#sendMessage').on('click', function(event) {
        event.preventDefault();

        let level = $('#level').val();
        let notPaid = $('#not_paid').val();
        let message = $('#message').val();

        // Validate if any field is empty
        if (!level || !notPaid || !message) {
            Swal.fire({
                title: "Error!",
                text: "Please fill in all fields.",
                icon: "error",
                confirmButtonColor: "#d33",
                confirmButtonText: "OK"
            });
            return;
        }


        Swal.fire({
            title: "Are you sure?",
            text: "Do you want to send this message?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Yes, submit it!"
        }).then((willSend) => {
            if (willSend.isConfirmed) {
                let formData = {
                    level: level,
                    not_paid: notPaid,
                    message: message
                };

                $.ajax({
                    type: 'POST',
                    url: HOST + 'mail',
                    data: JSON.stringify(formData),
                    contentType: 'application/json',
                    success: function(response) {
                        Swal.fire({
                            title: "Form Submitted!",
                            text: "Message sent successfully.",
                            icon: "success",
                            confirmButtonColor: "#3085d6",
                            confirmButtonText: "OK"
                        });
                        form.reset();
                    },
                    error: function(xhr, status, error) {
                        let errorMessage = "An error occurred.";
                        if (xhr.responseJSON && xhr.responseJSON.error) {
                            errorMessage = xhr.responseJSON.error;
                        }

                        Swal.fire({
                            title: "Error!",
                            text: errorMessage,
                            icon: "error",
                            confirmButtonColor: "#d33",
                            confirmButtonText: "OK"
                        });
                    }
                });
            } else {
                Swal.fire("Message not sent!");
            }
        });
    });
});
