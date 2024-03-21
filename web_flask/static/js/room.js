import API_ENDPOINTS from './apiEndpoint.js';

$(document).ready(function() {
    var HOST = API_ENDPOINTS;
    var roomID = null;
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


    $('.createNewRoom').on('click', function(event) {
    $('#AddRoomData').show();
    $('#UpdateRoomData').hide();
    })

    // Event listener for form submission
    $('#AddRoomData').on('click', function(event) {
      event.preventDefault();


      var form = $('#RoomForm')[0];
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var formData = {
      room_name: $("#roomNo").val(),
      room_type_id: $("#roomType").val(),
      block_id: $("#blockId").val(),
      gender: $("#gender").val(),
      floor: $("#floor").val(),
      no_of_beds: $("#noOfBeds").val(),
      booked_beds: $("#noOfBeds").val()
      };


      Swal.fire({
        title: 'Are you sure?',
        text: 'Do you want Add this room?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, submit it!'
      }).then((result) => {
        if (result.isConfirmed) {
          console.log('Form data:', formData);

          $.ajax({
            url: HOST + "room",
            type: 'POST',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            success: function(response) {
              console.log('Success:', response);

              Swal.fire({
                title: 'Form Submitted!',
                text: 'New Room Added successfully.',
                icon: 'success',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'OK'
              }).then((result) => {
                if (result.isConfirmed) {
                 location.reload();
                }
              });
            },
            error: function(xhr, status, error) {
              Swal.fire({
                title: 'Error!',
                text: "Room name already exists",
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

    $('.edit-room').on('click', function(event) {
      event.preventDefault();

      roomID = $(this).data('room-id');

      $.get({
        url:  HOST + "room/" + roomID,
        success: function(room) {
          $('#roomNo').val(room.room_name);
          $('#gender').val(room.gender);
          $('#noOfBeds').val(room.no_of_beds);
          $('#floor').val(room.floor);
          $('#roomType').val(room.room_type_id);
          $('#blockId').val(room.block_id);

            $('#AddRoomData').hide();
            $('#UpdateRoomData').show();
          $('#roomCreateUpdate').modal('show');
        },
        error: function(xhr, status, error) {
            Swal.fire({
                title: "Error!",
                text: error,
                icon: "error",
                confirmButtonColor: "#d33",
                confirmButtonText: "OK",
              });
        }
      });
    });
    $('#updateRoomData').on('click', function(event) {
      event.preventDefault();


      var form = $('#RoomForm')[0];
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var formData = {
      room_name: $("#roomNo").val(),
      room_type_id: $("#roomType").val(),
      block_id: $("#blockId").val(),
      gender: $("#gender").val(),
      floor: $("#floor").val(),
      no_of_beds: $("#noOfBeds").val(),
      booked_beds: $("#noOfBeds").val()
      };


      Swal.fire({
        title: 'Are you sure?',
        text: 'Do you want update this room?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, submit it!'
      }).then((result) => {
        if (result.isConfirmed) {
          console.log('Form data:', formData);

          $.ajax({
            url: HOST + "room/" + roomID,
            type: 'PUT',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            success: function(response) {
              console.log('Success:', response);

              Swal.fire({
                title: 'Form Submitted!',
                text: 'Room updated successfully.',
                icon: 'success',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'OK'
              }).then((result) => {
                if (result.isConfirmed) {
                 location.reload();
                }
              });
            },
            error: function(xhr, status, error) {
              Swal.fire({
                title: 'Error!',
                text: "Room name already exists",
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


    // Delete button click event
    $('.delete-type').on('click', function(event) {
     event.preventDefault();
        var blockId = $(this).data("type-id");
        Swal.fire({
          title: "Are you sure?",
          text: "You are about to delete this room Type. This action cannot be undone.",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#d33",
          cancelButtonColor: "#3085d6",
          confirmButtonText: "Yes, delete it!",
        }).then((result) => {
          if (result.isConfirmed) {
            $.ajax({
              url: HOST + "room_type/" + blockId,
              method: "DELETE",
              success: function (response) {
                Swal.fire({
                  title: "Deleted!",
                  text: "The block has been deleted.",
                  icon: "success",
                  confirmButtonColor: "#3085d6",
                  confirmButtonText: "OK",
                }).then(() => {
                  location.reload();
                });
              },
              error: function (xhr, status, error) {
                console.error("Error deleting block:", error);
                Swal.fire({
                  title: "Error!",
                  text: error,
                  icon: "error",
                  confirmButtonColor: "#d33",
                  confirmButtonText: "OK",
                });
              },
            });
          }
        });
      });

      roomID = null;
    });