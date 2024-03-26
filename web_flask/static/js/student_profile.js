import API_ENDPOINTS from './apiEndpoint.js';
$(document).ready(function () {
  let HOST = API_ENDPOINTS;
   let studentId = $("#student-id").val();
   console.log(studentId)
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

  $("#updateSelf").on("click", function (event) {
    event.preventDefault();

    let isValid = validateForm();
    if (!isValid) {
      return false;
    }

    let studentId = $(this).data("student-id");

    let formData = {
      first_name: $("#first_name").val(),
      last_name: $("#last_name").val(),
      other_name: $("#other_name").val(),
      email: $("#email").val(),
      phone: $("#phone").val(),
      date_of_birth: $("#date_of_birth").val(),
      gender: $("#gender").val(),
      address: $("#address").val(),
      disability: $("#disability").val(),
      password: $("#password").val(),
      guardian_name: $("#guardian_name").val(),
      guardian_phone: $("#guardian_phone").val(),
      student_number: $("#student_number").val(),
      program: $("#program").val(),
      level: $("#level").val(),
    };
    console.log(formData);

    Swal.fire({
      title: "Confirm Update",
      text: "Are you sure you want to update student information?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, update it!",
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: HOST + 'student/' + studentId,
          type: "PUT",
          contentType: "application/json",
          data: JSON.stringify(formData),
          success: function (response) {
            Swal.fire({
              title: "Success!",
              text: "Student information updated successfully.",
              icon: "success",
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
            Swal.fire({
              title: "Error!",
              text: "Failed to update student information. Please try again.",
              icon: "error",
              confirmButtonColor: "#d33",
              confirmButtonText: "OK",
            });
          },
        });
      }
    });
  });

  function validateForm() {
  let isValid = true;

  // Validation for first_name
  if ($("#first_name").val().trim() === "") {
    showValidationErrors(["First Name is required"]);
    isValid = false;
  }

  // Validation for last_name
  if ($("#last_name").val().trim() === "") {
    showValidationErrors(["Last Name is required"]);
    isValid = false;
  }

  // Validation for email
  let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if ($("#email").val().trim() === "" || !emailPattern.test($("#email").val().trim())) {
    showValidationErrors(["Email is invalid"]);
    isValid = false;
  }

  // Validation for phone
  let phonePattern = /^\d{10}$/;
  if ($("#phone").val().trim() === "" || !phonePattern.test($("#phone").val().trim())) {
    showValidationErrors(["Phone number is invalid"]);
    isValid = false;
  }

  // Validation for date_of_birth (You may need a different validation pattern)
  if ($("#date_of_birth").val().trim() === "") {
    showValidationErrors(["Date of Birth is required"]);
    isValid = false;
  }

  // Validation for gender (If gender is a select input, ensure it's selected)
  if ($("#gender").val() === "") {
    showValidationErrors(["Gender is required"]);
    isValid = false;
  }

  // Validation for address
  if ($("#address").val().trim() === "") {
    showValidationErrors(["Address is required"]);
    isValid = false;
  }

  // Validation for disability
  if ($("#disability").val().trim() === "") {
    showValidationErrors(["Disability is required"]);
    isValid = false;
  }

  // Validation for password (You may need a different validation pattern)
  if ($("#password").val().trim() === "") {
    showValidationErrors(["Password is required"]);
    isValid = false;
  }

  // Validation for guardian_name
  if ($("#guardian_name").val().trim() === "") {
    showValidationErrors(["Guardian Name is required"]);
    isValid = false;
  }

  // Validation for guardian_phone
  let guardianPhonePattern = /^\d{10}$/;
  if ($("#guardian_phone").val().trim() === "" || !guardianPhonePattern.test($("#guardian_phone").val().trim())) {
    showValidationErrors(["Guardian Phone number is invalid"]);
    isValid = false;
  }

  // Validation for student_number
  if ($("#student_number").val().trim() === "") {
    showValidationErrors(["Student Number is required"]);
    isValid = false;
  }

  // Validation for program
  if ($("#program").val().trim() === "") {
    showValidationErrors(["Program is required"]);
    isValid = false;
  }

  // Validation for level
  if ($("#level").val().trim() === "") {
    showValidationErrors(["Level is required"]);
    isValid = false;
  }

  return isValid;
}

});
