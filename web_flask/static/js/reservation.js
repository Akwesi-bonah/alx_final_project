import API_ENDPOINTS from "./apiEndpoint.js";


 const showloader = () => {
    Swal.fire({
      title: "Processing...Please wait!",
      onBeforeOpen: () => {
        Swal.showLoading();
      },
    });
  };


$(document).ready(function () {
  let HOST = API_ENDPOINTS;

  let selectedRoomID;
  let selectedStudentID;
  let numberOfBeds;

  $("#reserve").on("click", function (event) {
    event.preventDefault();

    let jsonData = {
      room_id: $("#room_name").val(),
      no_of_beds: $("#no_of_beds").val(),
    };

    Swal.fire({
      title: "Confirm Reservation",
      text: "Are you sure you want to make this reservation?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, reserve it!",
    }).then((result) => {
      if (result.isConfirmed) {
        showloader()
        $.ajax({
          type: "POST",
          url: HOST + "reserve",
          contentType: "application/json",
          data: JSON.stringify(jsonData),
          success: function (response) {
            Swal.fire({
              icon: "success",
              title: "Reservation Successful",
              text: "Room successfully reserved!",
              confirmButtonColor: "#3085d6",
            });
          },
          error: function (xhr, status, error) {
            let errorMessage = "An error occurred.";
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

  $(".assign-room").on("click", function () {
    selectedRoomID = $(this).data("room-id");
    $("#assignModal").modal("show");
  });

  $("#studentName").on("change", function () {
    selectedStudentID = $(this).val();
  });

  $("#no_of_beds").on("change", function () {
    numberOfBeds = $(this).val();
  });

  $(".drop-room").on("click", function () {
    selectedRoomID = $(this).data("room-id");
    $("#deleteModal").modal("show");
  });

  $(".proceed").on("click", function (event) {
    event.preventDefault();
    if (!selectedStudentID) {
      Swal.fire({
        title: "Select a Student",
        text: "Please select a student before proceeding.",
        icon: "warning",
        confirmButtonColor: "#3085d6",
        confirmButtonText: "OK",
      });
      return;
    }

    let bookingData = {
      room_id: selectedRoomID,
      student_id: selectedStudentID,
    };

    Swal.fire({
      title: "Confirm Booking",
      text: "Are you sure you want to book this room?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, Book it!",
    }).then((result) => {
      if (result.isConfirmed) {
        showloader()
        $.ajax({
          type: "POST",
          url: HOST + "booking",
          contentType: "application/json",
          data: JSON.stringify(bookingData),
          success: function (response) {
            console.log("Booking successful:", response);
            Swal.fire({
              title: "Success!",
              text: "Room booked successfully.",
              icon: "success",
              showCancelButton: false,
              confirmButtonColor: "#3085d6",
              confirmButtonText: "OK",
            }).then(() => {
              form.reset();
              $("#assignModal").modal("hide");

              location.reload();
            });
          },
          error: function (xhr, status, error) {
            let errorMessage = "You have already booked a room.";

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

  $(".confirmDelete").on("click", function (event) {
    event.preventDefault();
    if (!numberOfBeds) {
      Swal.fire({
        title: "Enter number of beds",
        text: "Please Enter Number of Beds to drop.",
        icon: "warning",
        confirmButtonColor: "#3085d6",
        confirmButtonText: "OK",
      });
      return;
    }

    let bookingData = {
      room_id: selectedRoomID,
      no_of_beds: numberOfBeds,
    };

    Swal.fire({
      title: "Confirm Dropping",
      text: "Are you sure you want to drop this Rooms?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, Book it!",
    }).then((result) => {
      if (result.isConfirmed) {
        showloader()
        $.ajax({
          type: "POST",
          url: HOST + "cancel",
          contentType: "application/json",
          data: JSON.stringify(bookingData),
          success: function (response) {
            console.log("Booking successful:", response);
            Swal.fire({
              title: "Success!",
              text: "Room dropped successfully.",
              icon: "success",
              showCancelButton: false,
              confirmButtonColor: "#3085d6",
              confirmButtonText: "OK",
            }).then(() => {
              form.reset();
              location.reload();
              $("#deleteModal").modal("hide");

            });
          },
          error: function (xhr, status, error) {
            let errorMessage = "An error occurred.";
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

  selectedRoomID = null;
  selectedStudentID = null;
  numberOfBeds = null;
});
