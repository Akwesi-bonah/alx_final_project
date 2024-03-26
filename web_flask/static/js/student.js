import API_ENDPOINTS from "./apiEndpoint.js";
$(document).ready(function () {
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
  $("#AddStudent").on("click", function (event) {
    event.preventDefault();
    let form = $("#studentForm")[0];
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    // Create FormData object to store form data including the image file
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
          url: API_ENDPOINTS + "student",
          type: "POST",
          data: formData,
          processData: false, // Prevent jQuery from processing the data
          contentType: false, // Prevent jQuery from setting contentType
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
                location.reload();
              }
            });
          },
          error: function (xhr, status, error) {
            let errorMessage = "An error occurred. Please try again.";

            if (xhr.responseJSON && xhr.responseJSON.message) {
              errorMessage = xhr.responseJSON.message;
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

  // Event listener for editing student data
  $(".edit-student").on("click", function (event) {
    event.preventDefault();
    let studentId = $(this).data("student-id");

    Swal.fire({
      title: "Please wait",
      text: "Fetching student data...",
      icon: "info",
      showConfirmButton: false,
      allowOutsideClick: false,
    });

    setTimeout(() => {
      Swal.close();
    }, 5000);

    // Get student data from API
    $.ajax({
      url: API_ENDPOINTS + "student/" + studentId,
      type: "GET",
      success: function (studentData) {
        // Update the form fields with student data
        $("#first_name").val(studentData.first_name);
        $("#last_name").val(studentData.last_name);
        $("#other_name").val(studentData.other_name);
        $("#email").val(studentData.email);
        $("#phone").val(studentData.phone);
        $("#date_of_birth").val(studentData.date_of_birth);
        $("#address").val(studentData.address);
        $("#student_number").val(studentData.student_number);
        $("#program").val(studentData.program);
        $("#address").val(studentData.address);
        $("#level").val(studentData.level);
        $("#gender").val(studentData.gender);
        $("#guardian_name").val(studentData.guardian_name);
        $("#guardian_phone").val(studentData.guardian_phone);
        $("#disability").val(studentData.disability);

        $("#StudentUpdate").modal("show");
        Swal.close();
      },
      error: function (xhr, status, error) {
        Swal.close();
        Swal.fire({
          title: "Error!",
          text: "Failed to fetch student data. Please try again.",
          icon: "error",
          confirmButtonColor: "#d33",
        });
      },
    });
  });

  $("#updateStudent").on("click", function (event) {
    event.preventDefault();
    let studentId = student_id;
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
      level : $("#level").val()
    };

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
          url: API_ENDPOINTS + "student/" + studentId,
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
});
