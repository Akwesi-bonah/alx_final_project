import API_ENDPOINTS from "./apiEndpoint.js";
$(document).ready(function () {
  let HOST = API_ENDPOINTS;

  function validateDOB(dateString) {
    let dob = new Date(dateString);
    if (isNaN(dob)) {
      return false;
    }

    let today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    let monthDiff = today.getMonth() - dob.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
      age--;
    }
    return age < 10;
  }

  function showValidationErrors(errors) {
    let errorMessage = "Please check the following fields:\n\n";
    for (let i = 0; i < errors.length; i++) {
      errorMessage += "- " + errors[i] + "\n";
    }
    Swal.fire({
      title: "Validation Error",
      text: errorMessage,
      icon: "error",
      confirmButtonColor: "#d33",
      confirmButtonText: "OK",
    });
  }

  // Event listener for form submission
  $("#registerStudent").on("click", function (event) {
    event.preventDefault();

    let form = $("#registerForm")[0];
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    // Validate Date of Birth
    let dobValid = validateDOB($("#date_of_birth").val());
    if (dobValid) {
      showValidationErrors(["Please Validate your date of birth."]);
      return;
    }
    let pass = $("#password").val();
    let confirmpass = $("#confirm-password").val();

    let message = "Invalid Input";
    if (pass == "") {
      Swal.fire(message, "Invalid password", "warning");
      $("#password").focus();
      return;
    }
    if (pass != confirmpass) {
      Swal.fire(message, "passwords do not match!", "warning");
      $("#password").focus();
      return;
    }

    if (checkStrength(pass) != "Strong") {
      Swal.fire(
        message,
        "You password is weak. consider adding lower, upper and numeric cases",
        "warning"
      );
      return;
    }

    let formData = new FormData();
    formData.append("first_name", $("#first_name").val());
    formData.append("last_name", $("#last_name").val());
    formData.append("other_name", $("#other_name").val());
    formData.append("email", $("#email").val());
    formData.append("phone", $("#phone").val());
    formData.append("date_of_birth", $("#date_of_birth").val());
    formData.append("gender", $("#gender").val());
    formData.append("address", $("#address").val());
    formData.append("disability", $("#disability").val());
    formData.append("password", $("#password").val());
    formData.append("guardian_name", $("#guardian_name").val());
    formData.append("guardian_phone", $("#guardian_phone").val());
    formData.append("student_number", $("#student_number").val());
    formData.append("program", $("#program").val());
    formData.append("level", $("#level").val());

    // Get the image file input element
    let imageInput = $("#profile_picture")[0];
    // Check if there's a file selected
    if (imageInput.files.length > 0) {
      // Append the image file to the FormData object
      formData.append("profile_picture", imageInput.files[0]);
    }

    Swal.fire({
      title: "Are you sure?",
      text: "Do you want to submit the form?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, submit it!",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: HOST + "student",
          type: "POST",
          data: formData,
          processData: false,
          contentType: false,
          success: function (response) {
            Swal.fire({
              title: "Form Submitted!",
              text: "Your form has been submitted successfully.",
              icon: "success",
              showCancelButton: false,
              confirmButtonColor: "#3085d6",
              confirmButtonText: "OK",
            }).then((result) => {
              if (result.isConfirmed) {
                form.reset();

                location.reload();
              }
            });
          },
          error: function (xhr, status, error) {
            console.log(error);
            let errorMessage = "An error occurred.";
            if (xhr.responseJSON && xhr.responseJSON.error) {
              errorMessage = xhr.responseJSON.error;
            } else {
              errorMessage = xhr.statusText;
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

  function checkStrength(password) {
    let strength = 0;
    if (password.length < 6) {
      return "Too short";
    }
    if (password.length > 7) strength += 1;
    // If password contains both lower and uppercase characters, increase strength value.
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1;
    // If it has numbers and characters, increase strength value.
    if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/))
      strength += 1;
    // If it has one special character, increase strength value.
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1;
    // If it has two special characters, increase strength value.
    if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/))
      strength += 1;
    // Calculated strength value, we can return messages
    // If value is less than 2
    if (strength <= 2) {
      return "Weak";
    } else {
      return "Strong";
    }
  }
});
