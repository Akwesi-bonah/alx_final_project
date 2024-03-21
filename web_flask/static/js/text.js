$(document).ready(function() {
  // Function to show validation errors using SweetAlert
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
  $('.createNewButton').on('click', function() {
      // Hide the "updateBlock" button and show the "AddBlock" button
      $('#updateBlock').hide();
      $('#AddBlock').show();
  });
   // Initially hide the "updateBlock" button
    $('#updateBlock').hide();
   var blockId = null;
  // Event listener for form submission
  $('#AddBlock').on('click', function(event) {
    event.preventDefault();
    var form = $('#FormPost')[0];
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
  
    var formData = {
      campus: $('#campus').val(),
      name: $('#name').val(),
      description: $('#description').val(),
      status: $('#status').val()
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
          url: 'http://127.0.0.1:5003/api/v1/block',
          type: 'POST',
          data: JSON.stringify(formData),
          contentType: 'application/json',
          success: function(response) {
  
            Swal.fire({
              title: 'Form Submitted!',
              text: 'New Block Added successfully.',
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
             var errorMessage = "An error occurred.";
      if (xhr.responseJSON && xhr.responseJSON.error) {
        errorMessage = xhr.responseJSON.error;
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
  
  $('.blockEditBtn').on('click', function(event) {
    event.preventDefault();
  
    blockId = $(this).data('block-id');
    $('#updateBlock').show();
     $('#AddBlock').hide();
    $.get({
      url: 'http://127.0.0.1:5003/api/v1/block/' + blockId,
      success: function(block) {
  
        $('#campus').val(block.campus);
        $('#name').val(block.name);
        $('#description').val(block.name);
        $('#status').val(block.status)
  
  
        $('#createUpdate').modal('show');
      },
      error: function(xhr, status, error) {
        console.error('Error fetching block:', error);
      }
    });
  });
  
  
  // Delete button click event
  $('.blockDeleteBtn').on('click', function(event) {
   event.preventDefault();
      var blockId = $(this).data("block-id");
      Swal.fire({
        title: "Are you sure?",
        text: "You are about to delete this block. This action cannot be undone.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!",
      }).then((result) => {
        if (result.isConfirmed) {
          $.ajax({
            url: "http://127.0.0.1:5003/api/v1/block/" + blockId,
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
                     error: function(xhr, status, error) {
             var errorMessage = "An error occurred.";
      if (xhr.responseJSON && xhr.responseJSON.error) {
        errorMessage = xhr.responseJSON.error;
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
  ,
          });
        }
      });
    });
  });