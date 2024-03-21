import API_ENDPOINTS from './apiEndpoint.js';
$(document).ready(function() {
    var HOST = API_ENDPOINTS;
  $("#setConfig").on("click", function(event) {
    event.preventDefault();

    var startDate = new Date($("#startDate").val());
    var expiryDate = new Date($("#endDate").val());
    var currentDate = new Date();
    var sixMonthsLater = new Date(startDate);
    sixMonthsLater.setMonth(sixMonthsLater.getMonth() + 6);

    if (!startDate || !expiryDate) {
      Swal.fire({
        title: "Error!",
        text: "Please select both start and expiry dates.",
        icon: "error",
        confirmButtonText: "OK"
      });
      return;
    } else if (startDate < currentDate) {
      Swal.fire({
        title: "Error!",
        text: "Start date should not be less than today's date.",
        icon: "error",
        confirmButtonText: "OK"
      });
      return;
    } else if (expiryDate <= sixMonthsLater) {
      Swal.fire({
        title: "Error!",
        text: "Expiry date should be at least 6 months greater than start date.",
        icon: "error",
        confirmButtonText: "OK"
      });
      return;
    }

    var formData = {
      "start_date": $("#startDate").val(),
      "expiry_date": $("#endDate").val(),
      "created_by": $("#setConfig").data("user-id")
    };

    Swal.fire({
      title: "Are you sure?",
      text: "Do you want to set the configuration?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, set it!"
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: HOST + "configure",
          type: "POST",
          contentType: "application/json",
          data: JSON.stringify(formData),
          success: function(response) {
            Swal.fire({
              title: "Success!",
              text: "Configuration set successfully.",
              icon: "success",
              confirmButtonText: "OK"
            }).then(function() {
              location.reload();
            });
          },
          error: function(xhr, status, error) {
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
          }
        });
      }
    });
  });
});
