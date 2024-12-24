"use strict";
$(document).ready(function(){  
  $(".edit_logs_modal").click(function(e){
    var userId = $(this).data("user-id"); 
    $("#edit_username").append(userId); 
  });

  $(".logs-cancel-button").click(function(e){  
    $('#edit_logs_modal').hide();
    window.location.reload();
  });  

  $(".edit_notification_modal").click(function(e){
    var userId = $(this).data("user-id");  
    $("#edit_id").val(userId); 
    var text = $(this).data("notif-textmsj"); 
    var type = $(this).data("notif-type"); 
    $("#edit_username").val(text); 
    $("#edit_email").val(type); 
  });

  $(".notif-cancel-button").click(function(e){  
    $('#edit_notification_modal').hide();
    window.location.reload();
  }); 

  $(".add-notif-cancel-button").click(function(e){  
    $('#add_notification_modal').hide();
    window.location.reload();
  }); 

  $(".delete-notification-text").click(function(e){  
    var notiftextid = $(this).data("notiftext-id"); 
    // e.preventDefault(); 
    $.ajax({
      url: "delete_notification_data",
      type: "GET",
      data: {"notiftext-id": notiftextid},
      success: function(response){
        Swal.fire({
          text: "Notification Deleted Successfully!",
          icon: "success",
          buttonsStyling: false,
          confirmButtonText: "Ok, got it!",
          customClass: {
              confirmButton: "btn btn-primary"
          }
        }).then(function (result) {
          if (result.isConfirmed) { 
            window.location.reload();
          }
        });

      },
    }); 
  }); 


  $(".delete-user-account").click(function(e){  
    var user_id = $(this).data("user-id");  
    $.ajax({
      url: "delete-user-account",
      type: "GET",
      data: {"user-id": user_id},
      success: function(response){
        Swal.fire({
          text: "User Deleted Successfully!",
          icon: "success",
          buttonsStyling: false,
          confirmButtonText: "Ok, got it!",
          customClass: {
              confirmButton: "btn btn-primary"
          }
        }).then(function (result) {
          if (result.isConfirmed) { 
            window.location.reload();
          }
        });

      },
    }); 
  });

  $("#edit_notification_modal_form").submit(function(e) {
    $(".edit-modal-response-messages").html('');
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
      url: 'update-notification',
      type: 'POST',
      data : formData,
      processData: false,
      contentType: false,
      success: function(response) {
        $(".edit-modal-response-messages").append("<p class='alert alert-success'>Notification Updated Succesfully</p>");
        Swal.fire({
          text: "Notification Updated Successfully!",
          icon: "success",
          buttonsStyling: false,
          confirmButtonText: "Ok, got it!",
          customClass: {
              confirmButton: "btn btn-primary"
          }
        }).then(function (result) {
          if (result.isConfirmed) {
              $('#edit_user_modal').hide();
              $(".modal-backdrop").removeClass("show");
                // $("#kt_modal_add_user").hide();
              window.location.reload();
          }
        });
      },
      error: function(data) {
        console.log(data.responseJSON.error);
          $(".edit-modal-response-messages").append("<p class='alert alert-warning'>" +data.responseJSON.error+"</p>");
      }
    });
  });


  $("#add_notification_modal_form").submit(function(e) {
    $(".edit-modal-response-messages").html('');
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
      url: 'add-notification',
      type: 'POST',
      data : formData,
      processData: false,
      contentType: false,
      success: function(response) {
        if (response.success == true){
          $(".edit-modal-response-messages").append("<p class='alert alert-success'>Notification Added Succesfully</p>");
          Swal.fire({
            text: "Notification Added Successfully!",
            icon: "success",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
          }).then(function (result) {
            if (result.isConfirmed) {
                $('#add_notification_modal').hide();
                $(".modal-backdrop").removeClass("show");
                  // $("#kt_modal_add_user").hide();
                window.location.reload();
            }
          });

        }
        if (response.success == false){
          $(".edit-modal-response-messages").append("<p class='alert alert-success'>Unable to Add Notification</p>");
          Swal.fire({
            text: "Empty Field not allowed!",
            icon: "warning",
            buttonsStyling: false,
            confirmButtonText: "Ok, got it!",
            customClass: {
                confirmButton: "btn btn-primary"
            }
          }).then(function (result) {
            if (result.isConfirmed) {
                $('#add_notification_modal').hide();
                $(".modal-backdrop").removeClass("show");
                  // $("#kt_modal_add_user").hide();
                window.location.reload();
            }
          });

        } 
        
      },
      error: function(data) {
        console.log(data.responseJSON.error);
          $(".edit-modal-response-messages").append("<p class='alert alert-warning'>" +data.responseJSON.error+"</p>");
      }
    });
  });



});