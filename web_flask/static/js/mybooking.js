import API_ENDPOINTS from './apiEndpoint.js';
document.getElementById('quickPayBtn').addEventListener('click', function() {
var HOST = API_ENDPOINTS;
    var booking_id = $(this).data('book-id');
    var paymentReference = 'PAYREF_' + Math.floor((Math.random() * 1000000000) + 1);

    // Fetch payment info for the booking ID
    $.ajax({
        url: HOST + "paymentInfo/" + booking_id,
        method: 'GET',
        success: function(response) {
            var paymentDetails = response.booking_info;

            const swalWithInput = Swal.mixin({
                input: 'number',
                inputAttributes: {
                    autocapitalize: 'off',
                    placeholder: 'Enter amount to pay',
                    step: '0.01'
                },
                confirmButtonText: 'Proceed',
                showCancelButton: true,
                cancelButtonText: 'Cancel',
                showLoaderOnConfirm: true,
                preConfirm: (amount) => {
                    if (!amount || amount <= 0) {
                        Swal.showValidationMessage(`Please enter a valid amount.`);
                    }
                    return amount;
                },
                allowOutsideClick: () => !Swal.isLoading()
            });

            swalWithInput.fire({
                title: 'Payment Details',
                html: `<div>Amount to be paid: ${paymentDetails.room_type_price}</div>
                       <div>Amount already paid: ${paymentDetails.paid}</div>`,
                icon: 'info'
            }).then((result) => {
                if (result.isConfirmed) {
                    var amountToPay = result.value;

                    var handler = PaystackPop.setup({
                        key: 'pk_test_4ccdf50310beaaefdde4febbcef5fee8fbbd7011',
                        email: paymentDetails.student_email,
                        amount: parseFloat(amountToPay) * 100,
                        currency: 'GHS',
                        ref: paymentReference,
                        metadata: {
                            custom_fields: [
                                {
                                    display_name: paymentDetails.student_name,
                                    variable_name: paymentDetails.room_name,
                                    value: paymentDetails.booking_id
                                }
                            ]
                        },
                        callback: function(response){
                            $.ajax({
                                url: HOST + "payment",
                                method: 'POST',
                                data: JSON.stringify({
                                    booking_id: booking_id,
                                    amount: parseFloat(amountToPay),
                                    student_id: paymentDetails.student_id,
                                    reference_id: response.reference,
                                    room_type_price: paymentDetails.room_type_price,
                                }),
                                contentType: 'application/json',
                                success: function(response) {
                                    Swal.fire({
                                        title: 'Success!',
                                        text: 'Payment recorded successfully.',
                                        icon: 'success'
                                    });
                                },
                                error: function(xhr, status, error) {
                                    var errorMessage = "An error occurred.";
                                    if (xhr.responseJSON && xhr.responseJSON.error) {
                                        errorMessage = xhr.responseJSON.error;
                                    }
                                    Swal.fire({
                                        title: 'Error',
                                        text: errorMessage,
                                        icon: 'error'
                                    });
                                }
                            });
                        },
                        onClose: function(){
                            console.log('Payment modal closed');
                        }
                    });
                    handler.openIframe();
                }
            });
        },
        error: function(xhr, status, error) {
            var errorMessage = "An error occurred.";
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            }
            Swal.fire({
                title: 'Error',
                text: errorMessage,
                icon: 'error'
            });
        }
    });
});


$(".cancelBook").on("click", function (event) {
  event.preventDefault();

  var bookingID = $(this).data("booking-id");

  Swal.fire({
    title: "Confirm Cancellation",
    text: "Are you sure you want to cancel this booking?",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Yes, Cancel it!",
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        type: "DELETE",
        url: HOST + "booking/" + bookingID,
        contentType: "application/json",
        success: function (response) {
          console.log("Cancellation successful:", response);
          Swal.fire({
            title: "Success!",
            text: "Booking cancelled successfully.",
            icon: "success",
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: "OK",
          }).then(() => {

            location.reload();
          });
        },
        error: function (xhr, status, error) {
          var errorMessage = "An error occurred.";
          if (xhr.responseJSON && xhr.responseJSON.error) {
            errorMessage = xhr.responseJSON.error;
          }

          Swal.fire({
            title: "Error!",
            text: errorMessage,
            icon: "error",
            showCancelButton: false,
            confirmButtonColor: "#d33",
            confirmButtonText: "OK",
          });
        },
      });
    }
  });
});
