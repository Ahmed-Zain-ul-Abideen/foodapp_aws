$("#kt_account_profile_details_form").submit(function(e) {
  $(".modal-response-messages").html('');
  var formData = new FormData(this);
  e.preventDefault();
  $.ajax({
    url: 'create-user',
    type: 'POST',
    data : formData,
    processData: false,
    contentType: false,
    success: function(response) {
      $(".modal-response-messages").append("<p class='alert alert-success'>" +response.message+"</p>");
      Swal.fire({
        text: "User Added Successfully!",
        icon: "success",
        buttonsStyling: false,
        confirmButtonText: "Ok, got it!",
        customClass: {
            confirmButton: "btn btn-primary"
        }
      }).then(function (result) {
        if (result.isConfirmed) {
            $('#kt_modal_add_user').hide();
            $(".modal-backdrop").removeClass("show");
            window.location.reload();
        }
      });
      
    },
    error: function(data) {
      console.log(data.responseJSON.error);
        $(".modal-response-messages").append("<p class='alert alert-warning'>" +data.responseJSON.error+"</p>");
    }
});
  });
  $(".cancel-button-icon").click(function(e){ 
    const element = document.getElementById('kt_modal_add_user');
    const form = element.querySelector('#kt_account_profile_details_form');
    const modal = new bootstrap.Modal(element);
        Swal.fire({
            text: "Are you sure you would like to cancel?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, cancel it!",
            cancelButtonText: "No, return",
            customClass: {
                confirmButton: "btn btn-primary",
                cancelButton: "btn btn-active-light"
            }
        }).then(function (result) {
            if (result.value) {
                form.reset(); // Reset form		
                $(".modal-backdrop").removeClass("show");
                $("#kt_modal_add_user").hide();
                window.location.reload();
                
            } else if (result.dismiss === 'cancel') {
              
                Swal.fire({
                    text: "Your form has not been cancelled!.",
                    icon: "error",
                    buttonsStyling: false,
                    confirmButtonText: "Ok, got it!",
                    customClass: {
                        confirmButton: "btn btn-primary",
                    }
                });
            }
        });

  });
  
$(document).ready(function(){ 


  $(".delete_tagi").click(function(e){   
    var  tagId = $(this).data("tagid");  
    var  tagtitle = $(this).data("tagtitle");  
    $.ajax({
      url: "delete-tag",
      type: "GET",
      data: {"tag_id": tagId,"tag_title":tagtitle},
      success: function(response){
        Swal.fire({
          text: response.message,
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

  $('#kt_docs_maxlength_custom_text_add').maxlength({
    threshold: 30,
    warningClass: "badge badge-success",
    limitReachedClass: "badge badge-danger",
    separator: ' of ',
    preText: 'You have entered ',
    postText: ' characters.',
    validate: true
  });

  $('#kt_docs_maxlength_custom_text_edit_theme_title').maxlength({
    threshold: 30,
    warningClass: "badge  badge-success-theme-title",
    limitReachedClass: "badge badge-danger",
    separator: ' of ',
    preText: 'You have entered ',
    postText: ' characters.',
    validate: true
  });

  var followform = $("#follow_this_user");
  followform.submit(function (e) {
      e.preventDefault();
      $(".modal-response-messages").html('');
      var formData = new FormData(this);
      $.ajax({
          url: "user-follow-dashboard",
          type: 'POST',
          data: formData,
          success: function (response) {
            $(".modal-response-messages").append("<p class='alert alert-success'>" +response.message+"</p>");
          },
          cache: false,
          contentType: false,
          processData: false
      });
  }); 

  var unfollowform = $("#unfollow_this_user");
  unfollowform.submit(function (e) {
      e.preventDefault();
      $(".modal-response-messages").html('');
      var formData = new FormData(this);
      $.ajax({
          url: "user-follow-dashboard",
          type: 'POST',
          data: formData,
          success: function (response) {
            $(".modal-response-messages").append("<p class='alert alert-success'>" +response.message+"</p>");
          },
          cache: false,
          contentType: false,
          processData: false
      });
  });

  // $(".edit_user_modal_button").click(function(e){
  //   var userId = $(this).data("userid");
  //   $.ajax({
  //     url: "get_user_data",
  //     type: "GET",
  //     data: {"user_id": userId},
  //     success: function(response){
  //       var role = response.role;
  //       $("#edit_username").val(response.user_name);
  //       $("#edit_id").val(response.user_id);
  //       $("#edit_email").val(response.email);
  //       $("#edit_phone_number").val(response.phone_number);
  //       $(".edit_dob").val(response.dob);
  //       $(".edit_user_profile_image").attr("style", "background-image: url( "+response.profile_picture+" )");
  //       if(response.drop_size_id){
  //         if(response.drop_size_id == 1){
  //           $(".edit_drop_size_id_1").attr('checked', 'checked');
  //         }
  //         else if(response.drop_size_id == 2)
  //         {
  //           $(".edit_drop_size_id_2").attr('checked', 'checked');
  //         }
  //         else if(response.drop_size_id == 3)
  //         {
  //           $(".edit_drop_size_id_3").attr('checked', 'checked');
  //         }
  //         else if(response.drop_size_id == 4)
  //         {
  //           $(".edit_drop_size_id_4").attr('checked', 'checked');
  //         }
  //         else if(response.drop_size_id == 5)
  //         {
  //           $(".edit_drop_size_id_5").attr('checked', 'checked');
  //         }
  //         else if(response.drop_size_id == 6)
  //         {
  //           $(".edit_drop_size_id_6").attr('checked', 'checked');
  //         }
  //       }
  //       if(role){
  //         if(role== 1){
            
            
  //           $(".role-1").attr('selected', 'selected');
  //           $(".role-1").attr('value', "1");
  //         }
  //         else if(role== 2){
           
  //           $(".role-2").attr('selected', 'selected');
  //           $(".role-2").attr('value', "2");
  //         }else if(role== 3){
            
  //           $(".role-3").attr('selected', 'selected');
  //           $(".role-3").attr('value', "3");
  //         }
  //       }
  //     },
  //     error: function(xhr, status, error){
  //         alert(xhr.responseText);
  //         console.log(xhr.responseText);
  //     }
  //   });
  // });
  
  $("#edit_user_modal_form").submit(function(e) {
    $(".edit-modal-response-messages").html('');
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
      url: 'update-user-account',
      type: 'POST',
      data : formData,
      processData: false,
      contentType: false,
      success: function(response) {
        $(".edit-modal-response-messages").append("<p class='alert alert-success'>User Updated Succesfully</p>");
        Swal.fire({
          text: "User Updated Successfully!",
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
  "use strict";
});