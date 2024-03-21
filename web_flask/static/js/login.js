import API_ENDPOINTS from './apiEndpoint.js';
$(document).ready(function () {
var HOST = API_ENDPOINTS;
  function validateDOB(dateString) {

    var dob = new Date(dateString);
    if (isNaN(dob)) {
      return false;
    }


    var today = new Date();
    var age = today.getFullYear() - dob.getFullYear();
    var monthDiff = today.getMonth() - dob.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
      age--;
    }
    return age < 10;
  }


  function showValidationErrors(errors) {
    var errorMessage = 'Please check the following fields:\n\n';
    for (var i = 0; i < errors.length; i++) {
      errorMessage += '- ' + errors[i] + '\n';
    }
    Swal.fire({
      title: 'Validation Error',
      text: errorMessage,
      icon: 'error',
      confirmButtonColor: '#d33',
      confirmButtonText: 'OK'
    });
  }

  // Event listener for form submission
  $('#registerStudent').on('click', function(event) {
    event.preventDefault();

    var form = $('#registerForm')[0];
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    // Validate Date of Birth
    var dobValid = validateDOB($('#date_of_birth').val());
    if (dobValid) {
      showValidationErrors(['Please Validate your date of birth.']);
      return;
    }

    var formData = {
      first_name: $('#first_name').val(),
      last_name: $('#last_name').val(),
      other_name: $('#other_name').val(),
      email: $('#email').val(),
      phone: $('#phone').val(),
      date_of_birth: $('#date_of_birth').val(),
      gender: $('#gender').val(),
      address: $('#address').val(),
      disability: $('#disability').val(),
      password: $('#password').val(),
      guardian_name: $('#guardian_name').val(),
      guardian_phone: $('#guardian_phone').val(),
      student_number: $('#student_number').val(),
      program: $('#program').val(),
      level: $('#level').val()
    };

    Swal.fire({
      title: 'Are you sure?',
      text: 'Do you want to submit the form?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, submit it!'
    }).then((result) => {
      if (result.isConfirmed) {

        $.ajax({
          url: HOST + 'student',
          type: 'POST',
          data: JSON.stringify(formData),
          contentType: 'application/json',
          success: function(response) {
            Swal.fire({
              title: 'Form Submitted!',
              text: 'Your form has been submitted successfully.',
              icon: 'success',
              showCancelButton: false,
              confirmButtonColor: '#3085d6',
              confirmButtonText: 'OK'
            }).then((result) => {
              if (result.isConfirmed) {
                            form.reset();

                location.reload();
              }
            });
          },
          error: function(xhr, status, error) {
    var errorMessage = "An error occurred.";
    if (xhr.responseJSON && xhr.responseJSON.error) {
        errorMessage = xhr.responseJSON.error;
    } else {
        errorMessage = xhr.statusText;
    }

    Swal.fire({
        title: 'Error!',
        text: errorMessage,
        icon: 'error',
        showCancelButton: false,
        confirmButtonColor: '#d33',
        confirmButtonText: 'OK'
    });
}

        });
      }
    });
  });


});
