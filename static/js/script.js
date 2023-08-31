$("form[name=signup_form").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden")
        }

    });
    e.preventDefault();

});

$("form[name=login_form").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden")
        }

    });
    e.preventDefault();

});

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$("form[name=update_user_form]").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    var userId = $form.data("user-id"); // Assuming you have added a data attribute to store the user ID

    $.ajax({
        url: "/user/update_user/${_id}",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            // Handle success, maybe display a success message
            console.log("User data updated successfully");
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }

    });
    e.preventDefault();

});


